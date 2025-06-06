from pymongo import MongoClient
import json

# Connect to MongoDB running locally
client = MongoClient("mongodb://localhost:27017/")

db = client["football_db"]
collection = db["my_collection"]
print("connected to DB with success")

# Function to load and insert JSON file
def insert_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Insert one or many depending on structure
        if isinstance(data, list):
            collection.insert_many(data)
        elif isinstance(data, dict):
            collection.insert_one(data)
        else:
            print("error")

# Insert both files
insert_json_file("/home/affes/Desktop/ETL_pipeline/top_scorers.json")
insert_json_file("/home/affes/Desktop/ETL_pipeline/top_assists.json")

print("Data inserted successfully.")
