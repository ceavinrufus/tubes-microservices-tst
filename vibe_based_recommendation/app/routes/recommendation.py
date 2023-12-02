from fastapi import APIRouter, Depends, HTTPException
from app.utils.calculate_age import calculate_age
from dotenv import load_dotenv
from app.models.vibe import VibeRecommendation
from app.middleware.service2auth import Service2AuthMiddleware
import json
import os
from app.middleware.authorization import JWTBearer

router = APIRouter(tags=["Recommendations"])

load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD") 

router = APIRouter(tags=["Recommendations"])
service2_auth = Service2AuthMiddleware('https://bevbuddy.up.railway.app/login', USERNAME, PASSWORD)

@router.post("/beverages/")
async def beverage_recommendation(criteria: VibeRecommendation, max_amount: int, current_user: JWTBearer = Depends(JWTBearer(roles=["customer", "admin", "superadmin"]))):
    if max_amount > 20:
        raise HTTPException(status_code=400, detail="The max_amount of recommendation should lower than or equal to 20")
    
    request_body = {
        "activity": criteria.activity,
        "age": calculate_age(current_user.birthdate.isoformat()),
        "gender": current_user.gender,
        "height": current_user.height,
        "mood": criteria.mood,
        "weather": "yes" if criteria.weather else "no",
        "weight": current_user.weight,
        "max_rec": max_amount
    }

    response = service2_auth.make_authenticated_request('https://bevbuddy.up.railway.app/recommendations', method='POST', data=request_body)

    if response.status_code == 200:
        return {"results": response.json()}
    else:
        return json.loads(response.text)  # Retrieve the response text for error details