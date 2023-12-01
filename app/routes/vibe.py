from fastapi import APIRouter, Depends, HTTPException, Query
from app.schema.vibe_schemas import list_serial, individual_serial
from app.config.database import vibes_collection
from datetime import date as d
from app.models.vibe import Vibe, VibeInDB
from app.middleware.auth import get_current_active_user, check_admin
from app.models.user import User

router = APIRouter(tags=["Vibes"])

@router.get('')
async def get_all_vibes(current_user: User = Depends(get_current_active_user)):
    vibes = list_serial(vibes_collection.find().limit(100))
    return {"results": vibes}

@router.put('/{date}')
async def update_vibe(date: str, vibe: Vibe, current_user: User = Depends(get_current_active_user)):
    existing_vibe = vibes_collection.find_one({"date": date})
    if not existing_vibe:
        raise HTTPException(status_code=404, detail="Vibe not found")
    
    if date != vibe.date.isoformat():
        existing_vibe = vibes_collection.find_one({"date": vibe.date.isoformat()})
        if existing_vibe:
            raise HTTPException(status_code=400, detail="Vibe with specified date already exists")

    vibe.date = vibe.date.isoformat()
    vibes_collection.find_one_and_update({"date": date}, {"$set": dict(vibe)})
    vibe.date = d.fromisoformat(vibe.date)

    return {"data": vibe}

@router.get('/date/')
async def get_vibe_by_date(date: str, current_user: User = Depends(get_current_active_user)):
    vibe = vibes_collection.find_one({"date": date})
    
    if not vibe:
        raise HTTPException(status_code=404, detail="Vibe not found")

    return {"results":individual_serial(vibe)}

@router.post('')
async def create_vibe(vibe: Vibe, current_user: User = Depends(get_current_active_user)):
    existing_vibe = vibes_collection.find_one({"date": vibe.date.isoformat()})
    if existing_vibe:
        raise HTTPException(status_code=400, detail="Vibe with specified date already exists, try PUT method instead")
    
    vibe_dict = VibeInDB(
        **dict(vibe),
        username=current_user.username
    )

    vibe_dict.date = vibe_dict.date.isoformat()
    vibes_collection.insert_one(dict(vibe_dict))
    return {"data": vibe_dict}


@router.delete('/{date}')
async def delete_vibe(date: str, current_user: User = Depends(get_current_active_user)):
    existing_vibe = vibes_collection.find_one({"date": date})
    
    if not existing_vibe:
        raise HTTPException(status_code=404, detail="Vibe not found")
    
    vibes_collection.find_one_and_delete({"date": date})

    return {"message": "Vibe deleted successfully"}