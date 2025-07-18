import openai
from flask import current_app

def get_chat_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key is not configured in the application.")
    
    openai.api_key = api_key
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        current_app.logger.error(f"An error occurred with OpenAI API: {e}")
        raise

def generate_image(prompt: str, size: str = "1024x1024", n: int = 1) -> str:
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key is not configured.")
    
    openai.api_key = api_key

    try:
        response = openai.Image.create(prompt=prompt, n=n, size=size)
        return response['data'][0]['url']
    except Exception as e:
        current_app.logger.error(f"An error occurred during image generation: {e}")
        raise