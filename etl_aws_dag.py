from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pymongo import MongoClient
import http.client
import json
import boto3
import os
from dotenv import load_dotenv

default_args = {
    'start_date': datetime(2025, 1, 1),
    'catchup': False
}

dag = DAG(
    'football_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    description='Extract football data, store in JSON, insert into MongoDB and transform',
    tags=['football', 'etl'],
)

# ---------------------- STEP 1: Extract from API ----------------------
def extract_data():
    load_dotenv()
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host" : os.getenv("X_RAPIDAPI_HOST"),
        "x-rapidapi-key" : os.getenv("X_RAPIDAPI_KEY")

    }

    # Top Scorers
    conn.request("GET", "/players/topscorers?season=2021&league=61", headers=headers)
    top_scorers_data = conn.getresponse().read()
    top_scorers_json = json.loads(top_scorers_data.decode("utf-8"))
    with open("/tmp/top_scorers.json", "w", encoding='utf-8') as f:
        json.dump(top_scorers_json, f, indent=2, ensure_ascii=False)

    # Top Assists
    conn.request("GET", "/players/topassists?season=2021&league=61", headers=headers)
    top_assists_data = conn.getresponse().read()
    top_assists_json = json.loads(top_assists_data.decode("utf-8"))
    with open("/tmp/top_assists.json", "w", encoding='utf-8') as f:
        json.dump(top_assists_json, f, indent=2, ensure_ascii=False)

    print("Extracted API data and saved to JSON.")

# ---------------------- STEP 2: Load into MongoDB ----------------------
def load_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["football_db"]
    collection = db["my_collection"]
    print("Connected to MongoDB.")

    def insert_json_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                collection.insert_many(data)
            elif isinstance(data, dict):
                existing = collection.find_one({"get": data.get("get")})
                if existing:
                    collection.replace_one({"_id": existing["_id"]}, data)
                else:
                    collection.insert_one(data)
            else:
                print("❌ Invalid JSON structure.")

    insert_json_file("/tmp/top_scorers.json")
    insert_json_file("/tmp/top_assists.json")
    print("Data inserted into MongoDB.")

# ---------------------- STEP 3: Transform Data ----------------------
def transform_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["football_db"]
    collection = db["my_collection"]
    print("Connected to MongoDB for transformation.")

    document = collection.find_one({"get": "players/topscorers"})
    if not document:
        print("❌ No document found for 'players/topscorers'.")
        return

    for player in document['response']:
        stats = player['statistics'][0]
        goals = stats['goals']['total'] or 0
        assists = stats['goals']['assists'] if stats['goals']['assists'] is not None else 0
        stats['contribution'] = goals + assists

    collection.update_one(
        {"_id": document['_id']},
        {"$set": {"response": document['response']}}
    )

    print("Added 'contribution' field to MongoDB document.")

# ---------------------- STEP 4: Upload to AWS S3 ----------------------
def upload_to_s3():
    load_dotenv()
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    try:
        s3.upload_file('/tmp/top_scorers.json', 'footballstorages3', 'top_scorers.json')
        s3.upload_file('/tmp/top_assists.json', 'footballstorages3', 'top_assists.json')
        print("Uploaded files to S3 bucket 'footballstorages3'.")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

# ---------------------- Airflow Task Definitions ----------------------
extract_task = PythonOperator(
    task_id='extract_api_data',
    python_callable=extract_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_json_to_mongodb',
    python_callable=load_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_add_contribution',
    python_callable=transform_data,
    dag=dag
)

upload_task = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_s3,
    dag=dag
)

# ---------------------- Task Dependency Order ----------------------
extract_task >> load_task >> transform_task >> upload_task
