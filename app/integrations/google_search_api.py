import requests
from flask import current_app

SERPAPI_URL = "https://serpapi.com/search.json"

def search_google(query: str) -> dict:
    api_key = current_app.config.get('SERPAPI_API_KEY')
    if not api_key:
        raise ValueError("SerpApi API key is not configured.")

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }
    
    try:
        response = requests.get(SERPAPI_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"An error occurred with SerpApi: {e}")
        raise