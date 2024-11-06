# Mood-Based Song Recommendation App

This project is a mood-based music recommendation application that analyzes a user's inputted text, detects the emotion conveyed, and recommends a song tailored to the identified mood. The app utilizes IBM Watson for emotion detection, Google Cloud Translate for language translation, and Spotify's API for music recommendations.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

## Features

- Detects emotions from user input using IBM Watson Natural Language Understanding API.
- Automatically translates text input to English if necessary using Google Cloud Translate API.
- Recommends a song from Spotify based on detected emotion and mapped energy/valence levels.
- Handles various edge cases, such as error handling for API failures and short or ambiguous input.

## Technologies

- **Python** - Programming language
- **IBM Watson Natural Language Understanding API** - For emotion detection
- **Google Cloud Translate** - For translating text to English when needed
- **Spotify API** - For retrieving song recommendations based on emotion
- **Unittest and Mock** - For automated testing

## Setup

### Prerequisites

- Python 3.6+
- Access to the IBM Watson Natural Language Understanding, Google Cloud Translate, and Spotify APIs.
- Install dependencies from `requirements.txt`:
  
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root of the project with the following keys and fill in the appropriate values`:

```dotenv
# IBM Watson
WATSON_API_URL=your_watson_api_url
WATSON_API_KEY=your_watson_api_key

# Google Cloud Translate
GOOGLE_PROJECT_PARENT=projects/your_project_id/locations/global

# Spotify
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

## Usage

Run the application:

```bash
python project.py
```

You will be prompted to describe your current mood. Based on the analysis, the app will recommend a song that matches the mood. Type "quit" to exit the program.

Example Usage

```plaintext
Describe your current mood in a sentence (or type 'quit' to exit): I am feeling happy and excited!
Translating text to English...
Watson API response: {'joy': 0.85, 'anger': 0.05, 'sadness': 0.1}
Recommended song: Happy by Pharrell Williams
Thank you for using the mood-based song recommendation!

```

## Testing

Automated tests are provided to validate functionality. Run the tests with:

```bash
python -m unittest test_project.py
```

## Test Coverage

The tests cover:

- Basic functionality (e.g., detecting joy in text).
- Translation functionality for non-English text.
- Handling of short text and neutral/ambiguous inputs.
- Error handling for both Watson and Google Translate API failures.
- Exit condition upon entering "quit".
- 
## Future Improvements

- Expand emotion mapping to more diverse genres and song characteristics.
- Enhance error handling to provide more specific feedback to users.
- Implement a front-end interface for easier user interaction.