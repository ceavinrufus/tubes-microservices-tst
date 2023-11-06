from pathlib import Path
import pickle 
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

def recommend(movie, amount):
    # Training model
    movies = pd.read_csv(f'{BASE_DIR}\\data\\dataset.csv')
    movies=movies[['id', 'title', 'overview', 'genre']]
    movies['tags'] = movies['overview'] + movies['genre']
    new_data  = movies.drop(columns=['overview', 'genre'])
    
    cv=CountVectorizer(max_features=10000, stop_words='english')
    
    vector=cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
    similarity=cosine_similarity(vector)
    
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    for i in distance[1:amount+1]:
        # movies_id=movies.iloc[i[0]].id
        recommend_movie.append({"movie_id":int(movies.iloc[i[0]].id),"title":movies.iloc[i[0]].title})
    return recommend_movie
