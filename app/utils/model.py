from pathlib import Path
import pickle 

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Open the pickle files using the `with` statement to ensure they are properly closed.
with open(f"{BASE_DIR}\\data\\movies_list.pkl", "rb") as f1:
    movies = pickle.load(file=f1)

with open(f"{BASE_DIR}\\data\\similarity.pkl", "rb") as f2:
    similarity = pickle.load(file=f2)

movies_list=movies['title'].values

def recommend(movie, amount):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    for i in distance[1:amount+1]:
        # movies_id=movies.iloc[i[0]].id
        recommend_movie.append({"movie_id":int(movies.iloc[i[0]].id),"title":movies.iloc[i[0]].title})
    return recommend_movie
