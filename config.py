import os
from pymongo import MongoClient

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rsvaditya:VZNMJGOZiI8ktmUk@claims-management.cdyjh.mongodb.net/?retryWrites=true&w=majority&appName=Claims-management")

def get_db():
    client = MongoClient(MONGO_URI)
    return client['claims_management_system']
