import os
from pymongo import MongoClient


mongodb_uri = os.environ.get('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client.quotes_db
collection = db.quotes_collection
