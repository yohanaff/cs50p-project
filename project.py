import json
import os
import requests
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from google.cloud import translate

load_dotenv()


def detect_emotion(text):
    url = os.getenv("WATSON_API_URL")
    api_key = os.getenv("WATSON_API_KEY")
    headers = {"Content-Type": "application/json"}

    # Initialize Google Cloud Translate client
    translate_client = translate.TranslationServiceClient()
    parent = os.getenv("GOOGLE_PROJECT_PARENT")

    # Check if the input text is too short
    if len(text.split()) < 3:
        print("The input text is too short for emotion analysis. Please provide a more descriptive sentence.")
        return None

    # Detect language and translate if necessary
    response = translate_client.detect_language(content=text, parent=parent)
    detected_language = response.languages[0].language_code

    if detected_language != "en":
        print("Translating text to English...")
        translation_response = translate_client.translate_text(
            contents=[text],
            target_language_code='en',
            parent=parent
        )
        text = translation_response.translations[0].translated_text

    # Prepare parameters for Watson NLU
    params = json.dumps({
        "text": text,
        "features": {
            "emotion": {}
        }
    })

    try:
        response = requests.post(
            url + "/v1/analyze?version=2021-08-01",
            auth=("apikey", api_key),
            headers=headers,
            data=params
        )
        response.raise_for_status()
        response_data = response.json()

        # Log Watson API response for debugging
        print("Watson API response:", response_data)

        # Extract emotion data directly
        emotions = response_data.get("emotion", {}).get("document", {}).get("emotion", None)
        if emotions:
            return emotions
        else:
            print("No significant emotions detected. Using default neutral emotion.")
            return {"joy": 0.5, "sadness": 0.5, "fear": 0.5, "disgust": 0.5, "anger": 0.5}

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.content)
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None


# Emotion to Spotify parameters mapping
def emotion_to_spotify_params(emotions):
    emotion_map = {
        "joy": {"target_energy": 0.8, "target_valence": 0.9},
        "sadness": {"target_energy": 0.3, "target_valence": 0.2},
        "anger": {"target_energy": 0.7, "target_valence": 0.3},
        "fear": {"target_energy": 0.4, "target_valence": 0.4},
        "disgust": {"target_energy": 0.5, "target_valence": 0.2}
    }
    dominant_emotion = max(emotions, key=emotions.get)
    return emotion_map.get(dominant_emotion, {"target_energy": 0.5, "target_valence": 0.5})


# Spotify client setup
def initialize_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return Spotify(auth_manager=auth_manager)


# Get song recommendation
def get_song_recommendation_from_emotion(text):
    emotions = detect_emotion(text)
    if emotions is None:
        print("Emotion detection failed. Please try again with a different input.")
        return None

    spotify_params = emotion_to_spotify_params(emotions)
    spotify = initialize_spotify_client()

    results = spotify.recommendations(
        seed_genres=["pop"],
        limit=1,
        target_energy=spotify_params["target_energy"],
        target_valence=spotify_params["target_valence"]
    )

    if results["tracks"]:
        track = results["tracks"][0]
        return {"title": track["name"], "artist": track["artists"][0]["name"]}
    return None


# Main function
def main():
    while True:
        user_text = input("Describe your current mood in a sentence (or type 'quit' to exit): ")

        if user_text.lower() == "quit":
            print("Goodbye!")
            break

        song = get_song_recommendation_from_emotion(user_text)

        if song:
            print(f"Recommended song: {song['title']} by {song['artist']}")
            # Exit after a successful recommendation
            print("Thank you for using the mood-based song recommendation!")
            break
        else:
            print("No song recommendation found. Try a different input.")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
