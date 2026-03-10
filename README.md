🌤️ Live Weather ETL Pipeline
An automated data pipeline that fetches real-time weather data for 5 major Indian cities every hour, transforms and enriches it, and loads it into a MySQL database — fully orchestrated using Apache Airflow and containerised with Docker.

------------------------------------------------------------------------
📌 Overview
This project was built to eliminate manual weather data collection by automating the entire process — from API extraction to a structured MySQL reporting table — using a modern data engineering stack.
Instead of manually pulling and storing weather data, this pipeline runs automatically every hour across 10 major Indian cities, cleans the data, adds business-level insights like heat safety warnings and UV advice, and stores everything in MySQL for querying and analysis. The pipeline is fault-tolerant — if one city's API call fails, the remaining cities continue processing without interruption.

-------------------------------------------------------------------------
Open-Meteo API → extract_weather() → transform_and_load() → MySQL Database

⏳ Pipeline Flow
1. Fetch weather data for 10 Indian cities via Open-Meteo API
2. Transform and enrich data with derived columns
3. Load to MySQL weather_reports table
4. Runs automatically every hour

Orchestrated by: Apache Airflow (TaskFlow API)
Containerised with: Docker + Docker Compose
Schedule: Every hour (0 * * * *)

-------------------------------------------------------------------------

🛠️ Tech Stack

Tool                       Purpose
Python                Core pipeline logic
Apache Airflow        DAG orchestration and scheduling
Pandas                Data transformation and enrichment
MySQL                 Data storage and analytics layer
SQLAlchemy            Python to MySQL connection 
Docker & Docker       Compose Containerised deployment
Open-Meteo API        Free real-time weather data source 


-------------------------------------------------------------------------

📍 Cities Tracked

Delhi, Mumbai, Bangalore, Gurgaon, Noida, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad

-------------------------------------------------------------------------

📊 Data Collected

For each city every hour, the pipeline collects:
.Temperature (°C)
.Apparent / Feels Like Temperature (°C)
.Relative Humidity (%)
.Wind Speed (km/h)
.Precipitation (mm)
.UV Index
.Surface Pressure (hPa)

-------------------------------------------------------------------------

Derived / Enriched Columns:--

 Column              Logic

1)Heat_safety_level-- WARNING - HOT DAY if apparent temp > 45°C, else    NORMAL TEMPERATURE
2)uv_advice--         Wear Sunscreen if UV index > 3, else No sun protection needed
3)ingested_at--       Timestamp of when the pipeline ran

--------------------------------------------------------------------------

💡 Key Concepts Demonstrated

.TaskFlow API — modern @dag and @task decorator style, cleaner than traditional PythonOperator
.Automatic XCom — data passed between tasks via return values, no manual xcom_push/pull needed
.Fault-tolerant extraction — try/except per city means one failed API call never crashes the pipeline
.Data enrichment — derived business logic columns added during transformation
.Idempotent loading — duplicate detection on city, timestamp, and temperature before load
.Dockerised Airflow — full local deployment using Docker Compose with no manual Airflow setup