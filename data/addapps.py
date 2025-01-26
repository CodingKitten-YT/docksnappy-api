import json
from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "appstore"
COLLECTION_NAME = "apps"

# Load the JSON data
with open("output.json", "r") as file:
    apps = json.load(file)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Insert apps into the collection
try:
    result = collection.insert_many(apps)
    print(f"Inserted {len(result.inserted_ids)} apps into the database.")
except Exception as e:
    print(f"Error inserting apps: {e}")
finally:
    client.close()