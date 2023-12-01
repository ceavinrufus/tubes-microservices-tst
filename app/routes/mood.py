from fastapi import APIRouter, Depends, HTTPException, Query
from app.schema.mood_schemas import list_serial, individual_serial
from app.config.database import moods_collection
from datetime import date
from app.models.mood import Mood
from app.middleware.auth import get_current_active_user, check_admin
from app.models.user import User

router = APIRouter(tags=["Mood"])

@router.get('')
async def get_all_moods(current_user: User = Depends(get_current_active_user)):
    moods = list_serial(moods_collection.find().limit(100))
    return {"results": moods}

@router.get('/{mood_id}')
async def get_mood_by_id(mood_id: int, current_user: User = Depends(get_current_active_user)):
    mood = moods_collection.find_one({"id": mood_id})
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    return {"results":individual_serial(mood)}

@router.get('/date/')
async def get_mood_by_date(date: str, current_user: User = Depends(get_current_active_user)):
    mood = moods_collection.find({"date": date})
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood not found")

    return {"results":list_serial(mood)}

@router.post('')
async def create_mood(mood: Mood, current_user: User = Depends(get_current_active_user)):
    existing_mood = moods_collection.find_one({"id": mood.id})
    if existing_mood:
        raise HTTPException(status_code=400, detail="Mood with this ID already exists")

    mood.date = mood.date.isoformat()
    mood.time = mood.time.isoformat()
    moods_collection.insert_one(dict(mood))

    return {"data": mood}

@router.delete('/{id}')
async def delete_mood(id: int, current_user: User = Depends(get_current_active_user)):
    existing_mood = moods_collection.find_one({"id": id})
    
    if not existing_mood:
        raise HTTPException(status_code=404, detail="Mood not found")
    
    moods_collection.find_one_and_delete({"id": id})

    return {"message": "Mood deleted successfully"}