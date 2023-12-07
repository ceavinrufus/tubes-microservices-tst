from fastapi import APIRouter, Depends, HTTPException
from app.schemas.mood_schemas import list_serial, individual_serial
from app.config.database import moods_collection
from datetime import date as d, datetime, timedelta
from app.models.mood import MoodInDB, MoodReq
from app.middleware.authorization import JWTBearer
from app.utils.calculate_age import calculate_age
from dotenv import load_dotenv
from app.middleware.service2auth import Service2AuthMiddleware
import json
import os
from app.middleware.authorization import JWTBearer
from app.middleware.mood_detection import mood_detection, mood_mapping

router = APIRouter(tags=["Moods"])
load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD") 


@router.post("/recommendations/")
async def recommendations(input: str, max_amount: int, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "admin", "superadmin"]))):
    result = mood_detection(input)[0]

    result_label = result[0]["label"]
    mood = mood_mapping[result_label]

    retval = {"results": {"mood":mood}}

    try:
        movie_rec_auth = Service2AuthMiddleware('https://movie-rec-18221162.azurewebsites.net/users/login', USERNAME, PASSWORD, "access_token")
        movie_response = movie_rec_auth.make_authenticated_request('https://movie-rec-18221162.azurewebsites.net/movies/recommendations/', method='POST', params={"mood": mood, "max_amount": max_amount})
        if movie_response.status_code == 200:
            retval["results"].update({"movie_recommendations": movie_response.json()["recommendations"]})
    except Exception as e:
        retval["results"].update({"movie_recommendations": []})
        print(str(e))

    try:
        request_body = {
            "activity": "moderately_active",
            "age": calculate_age(current_user.birthdate.isoformat()),
            "gender": current_user.gender,
            "height": current_user.height,
            "mood": mood,
            "weather": "yes",
            "weight": current_user.weight,
            "max_rec": max_amount
        }
        beverage_rec_auth = Service2AuthMiddleware('https://bevbuddy.up.railway.app/login', USERNAME, PASSWORD, "token")
        beverage_response = beverage_rec_auth.make_authenticated_request('https://bevbuddy.up.railway.app/recommendations', method='POST', data=request_body)
        if beverage_response.status_code == 200:
            retval["results"].update({"beverage_recommendations": beverage_response.json()})
    except Exception as e:
        retval["results"].update({"beverage_recommendations": []})
        print(str(e))
        
    return retval

@router.get("/detect/")
async def recommendations(input: str):
    result = mood_detection(input)[0]
    total = 0
    for item in result:
        result_label = item["label"]
        item["label"] = mood_mapping[result_label]
        total += item["score"]

    label_scores = {}

    for item in result:
        label = item['label']
        score = item['score']
        if label in label_scores:
            label_scores[label].append(score)
        else:
            label_scores[label] = [score]
    result = [{"label": label, "score": sum(scores)} for label, scores in label_scores.items()]

    return result

@router.get('')
async def get_all_moods(current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "admin", "superadmin"]))):
    if (current_user.role == "customer"):
        moods = list_serial(moods_collection.find({"username": current_user.username}).limit(100))
    else:
        moods = list_serial(moods_collection.find().limit(100))
    
    return {"results": moods}

@router.get('/user/{username}')
async def get_user_moods(username: str, current_user: JWTBearer = Depends(JWTBearer(roles=["admin", "superadmin"]))):
    moods = list_serial(moods_collection.find({"username": username}).limit(100))
    
    return {"results": moods}


@router.get('/date/{date}')
async def get_mood_by_date(date: d, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "admin", "superadmin"]))):
    if (current_user.role == "customer"):
        mood = moods_collection.find({
            "$and": [
                {"datetime": {"$gte": date.isoformat()}},
                {"datetime": {"$lt": (date + timedelta(days=1)).isoformat()}},  # Assuming you want to query within a day
                {"username": current_user.username}  
            ]
        })
    else:
        mood = moods_collection.find({
            "$and": [
                {"datetime": {"$gte": date.isoformat()}},
                {"datetime": {"$lt": (date+ timedelta(days=1)).isoformat()}}  # Assuming you want to query within a day
            ]
        })
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    return {"results":list_serial(mood)}

@router.get('/datetime/{datetime}')
async def get_mood_by_datetime(datetime: datetime, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "superadmin"]))):
    if (current_user.role == "customer"):
        mood = moods_collection.find_one({
            "$and": [
                {"datetime": datetime.isoformat()},
                {"username": current_user.username}  
            ]
        })
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    return {"results":individual_serial(mood)}


@router.put('/{datetime}')
async def update_mood(datetime: datetime, mood: MoodReq, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "superadmin"]))):
    existing_mood = moods_collection.find_one({
        "$and": [
            {"datetime": datetime.isoformat()},
            {"username": current_user.username}  
        ]
    })
    if not existing_mood:
        raise HTTPException(status_code=404, detail="Mood not found")
    
    if datetime.isoformat() != mood.datetime.isoformat():
        existing_mood = moods_collection.find_one({"datetime": mood.datetime.isoformat()})
        if existing_mood:
            raise HTTPException(status_code=400, detail="Mood with specified datetime already exists")

    mood.datetime = mood.datetime.isoformat()
    moods_collection.find_one_and_update({
        "$and": [
            {"datetime": datetime.isoformat()},
            {"username": current_user.username}  
        ]
    }, {"$set": dict(mood)})

    return {"data": mood}


@router.post('')
async def create_mood(mood: MoodReq, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "superadmin"]))):
    existing_mood = moods_collection.find_one({"datetime": mood.datetime.isoformat()})
    existing_mood = moods_collection.find_one({
        "$and": [
            {"datetime": mood.datetime.isoformat()},
            {"username": current_user.username}
        ]
    })
    if existing_mood:
        raise HTTPException(status_code=400, detail="Mood with specified datetime already exists, try PUT method instead")
    
    mood_dict = MoodInDB(
        **dict(mood),
        username=current_user.username
    )

    mood_dict.datetime = mood_dict.datetime.isoformat()
    moods_collection.insert_one(dict(mood_dict))
    return {"data": mood_dict}


@router.delete('/{datetime}')
async def delete_mood(datetime: datetime, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "superadmin"]))):
    existing_mood = moods_collection.find_one({
        "$and": [
            {"datetime": datetime.isoformat()},
            {"username": current_user.username}  
        ]
    })
    if not existing_mood:
        raise HTTPException(status_code=404, detail="Mood not found")
    
    moods_collection.find_one_and_delete({
        "$and": [
            {"datetime": datetime.isoformat()},
            {"username": current_user.username}  
        ]
    })

    return {"message": "Mood deleted successfully"}