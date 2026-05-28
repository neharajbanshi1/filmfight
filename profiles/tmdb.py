import os
from functools import lru_cache

import requests

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

_CREDITS_CACHE = {}


def _api_key():
    key = os.getenv("TMDB_API_KEY", "")
    if not key:
        try:
            from django.conf import settings
            key = settings.TMDB_API_KEY
        except Exception:
            pass
    return key


@lru_cache(maxsize=500)
def search_movie(title, year=None):
    api_key = _api_key()
    if not api_key:
        return None

    params = {"api_key": api_key, "query": title}
    if year:
        params["year"] = year

    resp = requests.get(f"{TMDB_BASE}/search/movie", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("results"):
        return None

    movie = data["results"][0]
    movie_id = movie["id"]

    genres, director = _get_details(movie_id)

    return {
        "tmdb_id": movie_id,
        "title": movie["title"],
        "year": movie.get("release_date", "")[:4] if movie.get("release_date") else year,
        "genres": genres,
        "director": director,
        "poster_url": (
            f"{TMDB_IMAGE_BASE}{movie['poster_path']}"
            if movie.get("poster_path") else ""
        ),
    }


def _get_details(movie_id):
    api_key = _api_key()
    genres = []
    director = ""

    if movie_id in _CREDITS_CACHE:
        return _CREDITS_CACHE[movie_id]

    try:
        resp = requests.get(
            f"{TMDB_BASE}/movie/{movie_id}",
            params={"api_key": api_key},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        genres = [g["name"] for g in data.get("genres", [])]

        credits = requests.get(
            f"{TMDB_BASE}/movie/{movie_id}/credits",
            params={"api_key": api_key},
            timeout=10,
        )
        credits.raise_for_status()
        crew = credits.json().get("crew", [])
        for member in crew:
            if member.get("job") == "Director":
                director = member.get("name", "")
                break
    except Exception:
        pass

    _CREDITS_CACHE[movie_id] = (genres, director)
    return genres, director
