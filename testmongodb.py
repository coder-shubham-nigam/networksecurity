from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# 1. Replace these with your actual database username and password
username = quote_plus("shubhamnigam")
password = quote_plus("Mongodbatlas@123")

# 2. Your specific MongoDB Atlas connection string
uri = f"mongodb+srv://{username}:{password}@cluster0.gz0iu0x.mongodb.net/?appName=Cluster0&retryWrites=true&w=majority"

# 3. Initialize the client
client = MongoClient(uri, server_api=ServerApi('1'))

# Test the connection (Optional, just to verify it works)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)