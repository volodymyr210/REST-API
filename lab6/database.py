from pymongo import MongoClient
import os

MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/books')
client = MongoClient(MONGODB_URL)
db = client.get_default_database()

book_collection = db['books']
