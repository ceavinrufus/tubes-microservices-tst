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
import pandas as pd

# from app.utils import user_modeling

router = APIRouter(tags=["Movies"])
router_2 = APIRouter(tags=["Core Service", "Movies"])

# Get all movies
@router.get('')
async def get_all_movies():
    movies = list_serial(movies_collection.find().limit(100))
    return {"results":movies}

# Get a movie by its ID
@router.get('/{movie_id}')
async def get_movie_by_id(movie_id: int):
    movie = movies_collection.find_one({"id": movie_id})
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"results":individual_serial(movie)}

# Create a movie
@router.post('')
async def create_movie(movie: Movie, current_user: User = Depends(check_admin)):
    existing_movie = movies_collection.find_one({"id": movie.id})
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")

    genres_as_dict = [dict(genre) for genre in movie.genres]
    movie.genres = genres_as_dict

    movie.release_date = movie.release_date.isoformat()
    movies_collection.insert_one(dict(movie))
    movie.release_date = date.fromisoformat(movie.release_date)

    return {"data":movie}

# Update a movie
@router.put('/{id}')
async def put_movie(id: int, movie: Movie, current_user: User = Depends(check_admin)):
    existing_movie = movies_collection.find_one({"id": id})
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if id != movie.id:
        existing_movie = movies_collection.find_one({"id": movie.id})
        if existing_movie:
            raise HTTPException(status_code=400, detail="Movie with this ID already exists")

    genres_as_dict = [dict(genre) for genre in movie.genres]
    movie.genres = genres_as_dict

    movie.release_date = movie.release_date.isoformat()
    movies_collection.find_one_and_update({"id": id}, {"$set": dict(movie)})
    movie.release_date = date.fromisoformat(movie.release_date)

    return {"data":movie}

# Delete a movie
@router.delete('/{id}')
async def delete_movie(id: int, current_user: User = Depends(check_admin)):
    existing_movie = movies_collection.find_one({"id": id})
    
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movies_collection.find_one_and_delete({"id": id})

    return {"message": "Movie deleted successfully"}

# Recommendation
@router_2.get("/recommendation/")
async def recommendation(movie_id: int, max_amount: int, current_user: User = Depends(get_current_active_user)):
    if max_amount > 20:
        raise HTTPException(status_code=400, detail="The max_amount of recommendation should lower than or equal to 20")
    existing_movie = movies_collection.find_one({"id": movie_id})
    if not existing_movie:
        raise HTTPException(status_code=400, detail="Movie with this ID not exists")
    
    movies = pd.DataFrame(list_serial(movies_collection.find()))
    movies = movies[['movie_id', 'title', 'overview', 'genres']]
    # movies['tags'] = movies['overview'] + ' ' + ' '.join(movies['genres'])
    movies['tags'] = movies.apply(lambda row: row['overview'] + ' ' + ' '.join([mov['name'] for mov in row['genres']]), axis=1)


    new_data  = movies.drop(columns=['overview', 'genres'])
    cv=CountVectorizer(max_features=10000, stop_words='english')
    vector=cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
    similarity=cosine_similarity(vector)
    
    index=movies[movies['title']==individual_serial(existing_movie)["title"]].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    for i in distance[1:max_amount+1]:
        # movies_id=movies.iloc[i[0]].movie_id
        recommend_movie.append({"movie_id":int(movies.iloc[i[0]].movie_id),"title":movies.iloc[i[0]].title})

    # rec = recommend(individual_serial(existing_movie)["title"], max_amount)
    return {"recommendations": recommend_movie}

@router_2.get("/recommendation/mood/")
async def mood_recommendation(mood: str, max_amount: int, current_user: User = Depends(get_current_active_user)):
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

    if max_amount > len(recommend_movie):
        max_amount = len(recommend_movie)
        
    result=[]
    for i in range(max_amount):
        result.append({"movie_id":int(recommend_movie[i]["id"]),"title":recommend_movie[i]["title"]})

    return {"recommendations": result}
    # return {"recommendations": list_serial(recommend_movie)}

# Search
@router.get("/search/")
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
