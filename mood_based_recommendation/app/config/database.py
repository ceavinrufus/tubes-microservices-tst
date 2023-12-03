from pymongo import MongoClient
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

database_url = os.getenv("DATABASE_URL")
client = MongoClient(database_url)

db = client.movie_db

moods_collection = db["moods"]
users_collection = db["users"]