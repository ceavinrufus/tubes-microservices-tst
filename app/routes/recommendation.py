from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.movie import Movie
from app.models.user import User
from app.config.database import movies_collection
from app.schema.movie_schemas import list_serial, individual_serial
from app.middleware.auth import get_current_active_user, check_admin
from datetime import date
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv, find_dotenv
from app.middleware.service2auth import Service2AuthMiddleware
import pandas as pd
import json
import os

# from app.utils import user_modeling
load_dotenv(find_dotenv())

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD") 

router = APIRouter(tags=["Recommendation"])
service2_auth = Service2AuthMiddleware('https://bevbuddy.up.railway.app/login', USERNAME, PASSWORD)


# Make authenticated requests to Service 2 endpoints using the middleware with different methods
# service2_auth.make_authenticated_request('https://service2.com/endpoint2', method='POST', payload={"key": "value"})
# Add more requests as needed with different HTTP methods and payloads

@router.get("/beverages")
async def beverage_recommendation():
    request_body = {
        "activity": "lightly_active",
        "age": 20,
        "gender": "Male",
        "height": 171,
        "max_rec": 5,
        "mood": "happy",
        "weather": "yes",
        "weight": 63
    }

    response = service2_auth.make_authenticated_request('https://bevbuddy.up.railway.app/recommendations', method='POST', data=request_body)

    if response.status_code == 200:
        return {"results": response.json()}
    else:
        return json.loads(response.text)  # Retrieve the response text for error details


@router.get("/movies/")
async def movie_recommendation(mood: str, max_amount: int, current_user: User = Depends(get_current_active_user)):
    if max_amount > 20:
        raise HTTPException(status_code=400, detail="The max_amount of recommendation should lower than or equal to 20")

    if (mood.lower() == "tired"):
        recommend_movie = list(movies_collection.find({"genres.name":{ "$in" : ["Action", "Adventure"] }}))
    elif (mood.lower() == "sad"):
        recommend_movie = list(movies_collection.find({"genres.name":{ "$in" : ["Drama", "Romance"] }}))
    elif (mood.lower() == "bored"):
        recommend_movie = list(movies_collection.find({
            "$and": [
                {"genres.name":{ "$in" : ["Crime", "Adventure"] }},
                {"vote_average":{ "$gt": 7 }}
            ]
        }))
    elif (mood.lower() == "happy"):
        recommend_movie = list(movies_collection.find({"genres.name":{ "$in" : ["Music", "Animation"] }}))
    elif (mood.lower() == "chill"):
        recommend_movie = list(movies_collection.find({"genres.name":{ "$in" : ["Drama", "Family", "Comedy"] }}))
    elif (mood.lower() == "tense"):
        recommend_movie = list(movies_collection.find({"genres.name":{ "$in" : ["Crime", "War", "Action"] }}))
    elif (mood.lower() == "humorous"):
        recommend_movie = list(movies_collection.find({"genres.name":"Comedy"}))
    else:
        raise HTTPException(status_code=400, detail="Can't detect mood")

    if max_amount > len(recommend_movie):
        max_amount = len(recommend_movie)
        
    result=[]
    for i in range(max_amount):
        result.append({"movie_id":int(recommend_movie[i]["id"]),"title":recommend_movie[i]["title"]})

    return {"recommendations": result}
    # return {"recommendations": list_serial(recommend_movie)}