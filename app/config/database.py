from pymongo import MongoClient
import os

database_url = os.environ.get("DATABASE_URL", "localhost:5432")
client = MongoClient("mongodb+srv://ceavinrufus:mongodb123tst@cluster0.ld80c2r.mongodb.net/?retryWrites=true&w=majority")

db = client.movie_db

movies_collection = db["movies"]
users_collection = db["users"]