# Data Engineer by Ghazian Hanafi

This repository contains a hands-on Jupyter notebook and a DuckDB database supporting a demonstration of foundational data engineering skills, centered on **data ingestion, storage, and analytical exploration** using a real dataset.

## 📁 Repository Contents

| File | Description |
|------|-------------|
| `database.ipynb` | Main Jupyter notebook demonstrating database creation, exploration, and simple queries. |
| `climate.duckdb` | DuckDB database file used by the notebook to store and query climate and emissions data. |
| `image.png`, `image-1.png`, `output.png` | Visuals/plots produced by the notebook for documentation or demonstration purposes. |
| `.gitignore` | Standard git ignore file to exclude environment and build artifacts. |

---

## 📘 Purpose of the Repository

This repository is designed as a **learning resource for data engineering students and practitioners** to understand how to load, store, and query large datasets using an embedded analytical database (DuckDB). It also serves as a starting point for building basic analytics, demonstrating how the data engineer’s role spans from storage mechanics to simple analytical queries.

---

## 📒 What `database.ipynb` Does

The main notebook walks through the following steps:

### ✅ 1. Dataset Ingestion  
The notebook reads a CSV dataset containing global CO₂ and emissions data. This data includes metrics such as:

- `country`
- `year`
- `ghg_per_capita`
- other climate emission indicators

The notebook loads this dataset into DuckDB for efficient querying and storage.

---

### ✅ 2. DuckDB Database Creation  
It demonstrates how to:

- Create a **DuckDB database file** (`climate.duckdb`)
- Insert the raw dataset into a persistent table
- Perform multiple SQL queries on the dataset

This shows how an analytical embedded database can support both interactive and batch analytics.

---

### ✅ 3. Schema Inspection and Data Exploration  
The notebook includes SQL commands for:

- Listing tables
- Inspecting table schema
- Verifying column types
- Exploring table contents with sample queries

This helps illustrate how to understand a database’s structure before deeper analysis.

---

### ✅ 4. Simple Data Analysis Queries  
Examples include:

- Selecting top emitters in specific years
- Filtering data by country
- Ranking and aggregating CO₂ metrics

This illustrates how to use SQL for analytical tasks within a data engineering workflow.

---

### ✅ 5. Visual Outputs  
The notebook includes generated images (`image.png`, `image-1.png`, `output.png`) that show:

- Sample query results
- Visual snapshots of the DuckDB UI
- Graphical insights from the dataset

These visuals support explanations in the notebook and help non-technical readers understand results.

---

## 🧠 What You Learn From This Repo

This repository helps you understand:

- How to ingest and store data in DuckDB using Python and SQL
- How to inspect and explore database schema and contents
- How to perform analytical queries on real world datasets
- How DuckDB can be used as an efficient analytical backend for data pipelines

It is ideal for beginners learning:

- Data Engineering fundamentals
- SQL for analytics
- Lightweight analytical database deployment

---

## 🧪 Prerequisites to Run

To run the notebook yourself:

1. Install Python 3.8+
2. Install required packages:
   ```bash
   pip install duckdb pandas matplotlib jupyterlab
