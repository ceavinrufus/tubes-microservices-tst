def individual_serial(movie) -> dict:
    return {
        # "id": str(movie.get("_id", "")),  # Provide a default value for missing keys
        "movie_id": int(movie.get("id", "")),  # Provide a default value for missing keys
        "title": movie.get("title", ""),  # Provide a default value for missing keys
        "genre": movie.get("genre", ""),  # Provide a default value for missing keys
        "original_language": movie.get("original_language", ""),  # Provide a default value for missing keys
        "overview": movie.get("overview", ""),  # Provide a default value for missing keys
        "release_date": movie.get("release_date", ""),  # Provide a default value for missing keys
    }

def list_serial(movies) -> list:
    return [individual_serial(movie) for movie in movies]