from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import duckdb


BATCH_SIZE = 500
CSV_PATH = "/opt/airflow/data/global_owid-co2-data.csv"


def create_schema():

    hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_country (
        id SERIAL PRIMARY KEY,
        country TEXT UNIQUE,
        iso_code TEXT
    );

    CREATE TABLE IF NOT EXISTS dim_year (
        id SERIAL PRIMARY KEY,
        year INT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS fact_co2 (
        country_id INT REFERENCES dim_country(id),
        year_id INT REFERENCES dim_year(id),
        population FLOAT,
        gdp FLOAT,
        cement_co2 FLOAT,
        cement_co2_per_capita FLOAT,
        co2 FLOAT,
        co2_growth_abs FLOAT,
        co2_growth_prct FLOAT,
        co2_including_luc FLOAT,
        co2_including_luc_growth_abs FLOAT
    );

    CREATE TABLE IF NOT EXISTS ingestion_state (
        id INT PRIMARY KEY DEFAULT 1,
        last_offset INT
    );

    INSERT INTO ingestion_state (id, last_offset)
    VALUES (1, 0)
    ON CONFLICT (id) DO NOTHING;
    """)

    conn.commit()
    cursor.close()


def load_batch_with_duckdb():

    hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Get last processed offset
    cursor.execute("SELECT last_offset FROM ingestion_state WHERE id=1;")
    last_offset = cursor.fetchone()[0]

    # DuckDB staging
    con = duckdb.connect(database=':memory:')

    con.execute(f"""
        CREATE TABLE staging AS
        SELECT *
        FROM read_csv_auto('{CSV_PATH}')
        LIMIT {BATCH_SIZE}
        OFFSET {last_offset}
    """)

    # Insert dimensions
    cursor.execute("""
        INSERT INTO dim_country (country, iso_code)
        SELECT DISTINCT country, iso_code FROM staging
        ON CONFLICT (country) DO NOTHING;
    """)

    cursor.execute("""
        INSERT INTO dim_year (year)
        SELECT DISTINCT year FROM staging
        ON CONFLICT (year) DO NOTHING;
    """)

    # Insert facts
    cursor.execute("""
        INSERT INTO fact_co2 (
            country_id,
            year_id,
            population,
            gdp,
            cement_co2,
            cement_co2_per_capita,
            co2,
            co2_growth_abs,
            co2_growth_prct,
            co2_including_luc,
            co2_including_luc_growth_abs
        )
        SELECT
            dc.id,
            dy.id,
            s.population,
            s.gdp,
            s.cement_co2,
            s.cement_co2_per_capita,
            s.co2,
            s.co2_growth_abs,
            s.co2_growth_prct,
            s.co2_including_luc,
            s.co2_including_luc_growth_abs
        FROM staging s
        JOIN dim_country dc ON s.country = dc.country
        JOIN dim_year dy ON s.year = dy.year;
    """)

    # Update offset
    new_offset = last_offset + BATCH_SIZE
    cursor.execute("""
        UPDATE ingestion_state
        SET last_offset = %s
        WHERE id=1;
    """, (new_offset,))

    conn.commit()
    cursor.close()
    con.close()


with DAG(
    dag_id="co2_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["duckdb", "incremental", "star_schema"]
) as dag:

    create_schema_task = PythonOperator(
        task_id="create_schema",
        python_callable=create_schema
    )

    load_batch_task = PythonOperator(
        task_id="load_batch_with_duckdb",
        python_callable=load_batch_with_duckdb
    )

    create_schema_task >> load_batch_task

