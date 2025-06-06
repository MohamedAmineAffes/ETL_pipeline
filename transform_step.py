from pymongo import MongoClient
import json

# Connect to MongoDB running locally
client = MongoClient("mongodb://localhost:27017/")

db = client["football_db"]
collection = db["my_collection"]
print("connected to DB with success")

########                   add new filed for the contribution                         #########





