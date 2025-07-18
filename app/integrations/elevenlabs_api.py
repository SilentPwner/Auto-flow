import requests
from flask import current_app

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/"

def convert_text_to_audio_stream(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    api_key = current_app.config.get('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError("ElevenLabs API key is not configured.")

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = { "text": text, "model_id": "eleven_multilingual_v2" }

    try:
        response = requests.post(f"{API_URL}{voice_id}", json=data, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"An error occurred with ElevenLabs API: {e}")
        raise