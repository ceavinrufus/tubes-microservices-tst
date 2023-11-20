from typing import List

def genre_serial(genres) -> List[dict]:
    return [{"genre_id":int(genre.get("id", "")), "name":genre.get("name", "")} for genre in genres]

def spoken_languages_serial(spoken_languages) -> List[dict]:
    return [{"language_code":spoken_language.get("iso_639_1", ""), "name":spoken_language.get("name", "")} for spoken_language in spoken_languages]


def individual_serial(movie) -> dict:
    return {
        # "id": str(movie.get("_id", "")),  # Provide a default value for missing keys
        "movie_id": int(movie.get("id", "")),  # Provide a default value for missing keys
        "title": movie.get("title", ""),  # Provide a default value for missing keys
        "genres": genre_serial(movie.get("genres", [])),  # Provide a default value for missing keys
        "original_language": movie.get("original_language", ""),  # Provide a default value for missing keys
        "overview": movie.get("overview", ""),  # Provide a default value for missing keys
        "release_date": movie.get("release_date", ""),  # Provide a default value for missing keys
        "popularity": float(movie.get("popularity", "")),  # Provide a default value for missing keys
        "vote_average": float(movie.get("vote_average", "")),  # Provide a default value for missing keys
        "runtime": int(movie.get("runtime", "")),  # Provide a default value for missing keys
        "spoken_languages": spoken_languages_serial(movie.get("spoken_languages", [])),  # Provide a default value for missing keys
    }

def list_serial(movies) -> list:
    return [individual_serial(movie) for movie in movies]