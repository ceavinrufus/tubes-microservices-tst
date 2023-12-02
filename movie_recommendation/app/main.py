from fastapi import FastAPI
from app.routes.movie import router as movie_router
from app.routes.user import router as auth_router

app = FastAPI()

@app.get("/")
async def root():
    return {"Microservice":"Movie Recommendation","Created by": {"Nama":"Ceavin Rufus De Prayer Purba", "NIM": "18221162"}}

app.include_router(auth_router, prefix="/users")
app.include_router(movie_router, prefix="/movies")
