from airflow.sdk import dag, task
import pendulum
import requests
import pandas as pd
from sqlalchemy import create_engine


MYSQL_CONN = "mysql+pymysql://USERNAME:PASSWORD@host.docker.internal:3306/weather_details"
API_URL = "https://api.open-meteo.com/v1/forecast"

LOCATIONS = [
    {"city": "Delhi",     "lat": 28.6139, "lon": 77.2090},
    {"city": "Mumbai",    "lat": 19.0760, "lon": 72.8777},
    {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"city": "Gurgaon",   "lat": 28.4595, "lon": 77.0266},
    {"city": "Noida",     "lat": 28.5355, "lon": 77.3910},
    {"city": "Chennai",   "lat": 13.0827, "lon": 80.2707},
    {"city": "Kolkata",   "lat": 22.5726, "lon": 88.3639},
    {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"city": "Pune",      "lat": 18.5204, "lon": 73.8567},
    {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714}
]


@dag(
    dag_id="taskflow_weather_pipeline",
    schedule="0 * * * *",
    start_date=pendulum.datetime(2026, 3, 1, tz="Asia/Kolkata"),
    catchup=False,
    tags=["taskflow", "learning"]
)
def weather_etl():

   
    @task()
    def extract_weather():
        all_results = []
        for loc in LOCATIONS:
            params = {
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m,precipitation,apparent_temperature,surface_pressure,uv_index",
                "timezone": "Asia/Kolkata",
                "forecast_days": 1
            }
            try :
             response = requests.get(API_URL, params=params)
             response.raise_for_status()
             data = response.json()
            
             h = data["hourly"]
             all_results.append({
                "city": loc["city"],
                "timestamp": h["time"][0],
                "temperature": h["temperature_2m"][0],
                "apparent_temp":h["apparent_temperature"][0],
                "humidity": h["relative_humidity_2m"][0],
                "wind_speed": h["windspeed_10m"][0],
                "precipitation": h["precipitation"][0],
                "uv_index":h["uv_index"][0],
                "pressure":h["surface_pressure"][0]
                })
            except Exception as e:
               print(f"WARNINIG : ERROR {loc['city']}")
               continue
        return all_results

    @task()
    def transform_and_load(ti=None):
        raw_weather_data = ti.xcom_pull(task_ids='extract_weather')
        
        df = pd.DataFrame(raw_weather_data) 
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['temperature']=df['temperature'].fillna(0.0)
        df['temperature'] = pd.to_numeric(df['temperature']).round(1)
        df['city']=df['city'].fillna('unknown_city')
        df['apparent_temp'] = pd.to_numeric(df['apparent_temp']).round(2)
        df['uv_index'] = pd.to_numeric(df['uv_index']).round(2)
        df = df.drop_duplicates(subset=['city','timestamp','temperature'],keep='first')
        df['ingested_at'] = pendulum.now().to_datetime_string()
        df['heat_safety_level'] = df['apparent_temp'].apply(lambda x :'WARNING - HOT DAY' if x > 45 else "NORMAL TEMPERATURE ")
        df['uv_advice'] = df['uv_index'].apply(lambda x : "Wear Sunscreen" if x > 3 else 'no sun protection needed ')

        engine = create_engine(MYSQL_CONN)
        df.to_sql('weather_reports', con=engine, if_exists='append', index=False)
        print(f"✅ Loaded {len(df)} rows to MySQL via TaskFlow.")

   
    extract_weather() >> transform_and_load()


weather_dag = weather_etl()