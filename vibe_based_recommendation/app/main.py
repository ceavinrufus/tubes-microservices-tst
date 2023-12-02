from fastapi import FastAPI
from app.routes.vibe import router as vibe_router
from app.routes.user import router as auth_router
from app.routes.recommendation import router as recommedation_router

app = FastAPI()

@app.get("/")
async def root():
    return {"Microservice":"Vibe Based Recommendation","Created by": {"Nama":"Ceavin Rufus De Prayer Purba", "NIM": "18221162"}}

app.include_router(auth_router, prefix="/users")
app.include_router(vibe_router, prefix="/vibes")
app.include_router(recommedation_router, prefix="/recommendations")
