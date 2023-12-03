import requests, os

API_URL = "https://api-inference.huggingface.co/models/arpanghoshal/EmoRoBERTa"
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

mood_mapping = {
  "gratitude": "happy",
  "admiration": "loved",
  "curiosity": "focus",
  "neutral": "neutral",
  "confusion": "chill",
  "excitement": "happy",
  "caring": "loved",
  "approval": "loved",
  "joy": "happy",
  "annoyance": "angry",
  "disappointment": "sad",
  "relief": "chill",
  "amusement": "happy",
  "anger": "angry",
  "surprise": "happy",
  "desire": "happy",
  "disgust": "angry",
  "remorse": "sad",
  "love": "loved",
  "optimism": "happy",
  "grief": "sad",
  "disapproval": "sad",
  "sadness": "sad",
  "fear": "scared",
  "pride": "loved",
  "embarrassment": "chill",
  "realization": "focus",
  "nervousness": "scared"
}

def mood_detection(input: str):
    payload = {
        "inputs": input,
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    return response.json()
	