from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.movie import Movie
from app.models.user import User
from app.config.database import movies_collection
from app.schema.schemas import list_serial, individual_serial
from app.models.model import recommend
from bson import ObjectId
from app.routes.auth import get_current_active_user
from datetime import date
from fuzzywuzzy import fuzz

# from app.utils import user_modeling

router = APIRouter()

# Get all movies
@router.get('/movies')
async def get_all_movies():
    movies = list_serial(movies_collection.find().limit(100))
    return {"results":movies}

# Get a movie by its ID
@router.get('/movies/{movie_id}')
async def get_movie_by_id(movie_id: int):
    return {"results":individual_serial(movies_collection.find_one({"id": movie_id}))}

# Create a movie
@router.post('/movies')
async def create_movie(movie: Movie, current_user: User = Depends(get_current_active_user)):
    existing_movie = movies_collection.find_one({"id": movie.id})
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")

    movie.release_date = movie.release_date.isoformat()
    movies_collection.insert_one(dict(movie))
    movie.release_date = date.fromisoformat(movie.release_date)

    return {"data":movie}

# Update a movie
@router.put('/movies/{id}')
async def put_movie(id: str, movie: Movie, current_user: User = Depends(get_current_active_user)):
    movies_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(movie)})
    return {"data":movie}

# Delete a movie
@router.delete('/movies/{id}')
async def delete_movie(id: str, current_user: User = Depends(get_current_active_user)):
    movies_collection.find_one_and_delete({"_id": ObjectId(id)})

# Recommendation
@router.get("/recommendation/")
async def recommendation(movie_id: int, amount: int, current_user: User = Depends(get_current_active_user)):
    if amount > 20:
        raise HTTPException(status_code=400, detail="The amount of recommendation should lower than or equal to 20")
    existing_movie = movies_collection.find_one({"id": movie_id})
    if not existing_movie:
        raise HTTPException(status_code=400, detail="Movie with this ID not exists")
    rec = recommend(individual_serial(existing_movie)["title"], amount)
    return {"recommendations": rec}

# Search
@router.get("/search-movie/")
async def search_movie(title: str = Query(..., description="Search for movies by title")):
    # Use a regex pattern to match titles that contain the query
    regex_pattern = f".*{title}.*"

    # Search for movies with titles that match the regex pattern
    matching_movies = list(movies_collection.find({"title": {"$regex": regex_pattern, "$options": "i"}}))

    # Calculate similarity scores for each movie title and the query
    similarity_scores = [(movie, fuzz.token_set_ratio(title, movie['title'])) for movie in matching_movies]

    # Sort the results by similarity score in descending order
    sorted_results = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    sorted_movies = [result[0] for result in sorted_results]

    if matching_movies:
        return {"data": list_serial(sorted_movies)}
    else:
        return {"message": "No matching movies found"}