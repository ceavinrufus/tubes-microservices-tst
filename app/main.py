from fastapi import FastAPI
from app.routes.movie import router as movie_router
from app.routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(movie_router)