🌤️ Live Weather ETL Pipeline
An automated data pipeline that fetches real-time weather data for 5 major Indian cities every hour, transforms and enriches it, and loads it into a MySQL database — fully orchestrated using Apache Airflow and containerised with Docker.

------------------------------------------------------------------------
📌 Overview
This project was built to eliminate manual weather data collection by automating the entire process — from API extraction to a structured MySQL reporting table — using a modern data engineering stack.
Instead of manually pulling and storing weather data, this pipeline runs automatically every hour across 10 major Indian cities, cleans the data, adds business-level insights like heat safety warnings and UV advice, and stores everything in MySQL for querying and analysis. The pipeline is fault-tolerant — if one city's API call fails, the remaining cities continue processing without interruption.

-------------------------------------------------------------------------
Open-Meteo API (10 cities)
          │
          ▼
┌──────────────────┐
│  extract_weather │   → Fetches weather data for each city via HTTP
│                  │   → Skips failed cities, continues remaining
└──────────────────┘
          │
          ▼
┌──────────────────────┐
│  transform_and_load  │   → Cleans, enriches, and loads to MySQL
└──────────────────────┘
          │
          ▼
┌──────────────────┐
│  MySQL Database  │   → weather_reports table
└──────────────────┘

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

City        Latitude        Longitude
Delhi       28.6139         77.2090
Mumbai      19.0760         72.8777
Bangalore   12.9716         77.5946
Gurgaon     28.4595         77.0266
Noida       28.5355         77.3910
Chennai     13.0827         80.2707
Kolkata     22.5726         88.3639 
Hyderabad   17.3850         78.4867
Pune        18.5204         73.8567
Ahmedabad   23.0225         72.5714

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

.Heat_safety_level-- WARNING - HOT DAY if apparent temp > 45°C, else    NORMAL TEMPERATURE
.uv_advice--         Wear Sunscreen if UV index > 3, else No sun protection needed
.ingested_at--       Timestamp of when the pipeline ran

--------------------------------------------------------------------------

💡 Key Concepts Demonstrated

.TaskFlow API — modern @dag and @task decorator style, cleaner than traditional PythonOperator
.Automatic XCom — data passed between tasks via return values, no manual xcom_push/pull needed
.Fault-tolerant extraction — try/except per city means one failed API call never crashes the pipeline
.Data enrichment — derived business logic columns added during transformation
.Idempotent loading — duplicate detection on city, timestamp, and temperature before load
.Dockerised Airflow — full local deployment using Docker Compose with no manual Airflow setup