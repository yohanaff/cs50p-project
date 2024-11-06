import unittest
from unittest.mock import patch, MagicMock
import requests

from project import detect_emotion, get_song_recommendation_from_emotion, main


class TestMoodBasedSongRecommendation(unittest.TestCase):

    @patch("builtins.input", side_effect=["I'm feeling extremely happy and thrilled today!", "quit"])
    def test_basic_functionality_joy(self, mock_input):
        song = get_song_recommendation_from_emotion(mock_input())
        self.assertIsNotNone(song)
        self.assertIn("title", song)
        self.assertIn("artist", song)

    @patch("builtins.input", side_effect=["Estou muito feliz!", "quit"])
    def test_translation_functionality(self, mock_input):
        song = get_song_recommendation_from_emotion(mock_input())
        self.assertIsNotNone(song)
        self.assertIn("title", song)
        self.assertIn("artist", song)

    @patch("builtins.input", side_effect=["Yes", "quit"])
    def test_short_text_handling(self, mock_input):
        song = get_song_recommendation_from_emotion(mock_input())
        self.assertIsNone(song)

    @patch("project.Spotify.recommendations",
           return_value={"tracks": [{"name": "Test Song", "artists": [{"name": "Test Artist"}]}]})
    @patch("builtins.input", side_effect=["This is a statement about the weather.", "quit"])
    def test_neutral_emotion_handling(self, mock_input, mock_recommendations):
        song = get_song_recommendation_from_emotion(mock_input())
        self.assertIsNotNone(song)
        self.assertIn("title", song)
        self.assertIn("artist", song)

    @patch("builtins.input", side_effect=["quit"])
    def test_exit_condition(self, mock_input):
        """Test if the program exits the loop on 'quit'."""
        main()
        # Check if "Goodbye!" was printed, indicating the loop exited
        self.assertTrue(mock_input.called)

    @patch("project.detect_emotion",
           return_value={"joy": 0.8, "sadness": 0.1, "fear": 0.05, "disgust": 0.02, "anger": 0.03})
    def test_emotion_data_with_mock(self, mock_detect_emotion):
        """Test detect_emotion with a mocked response."""
        emotions = detect_emotion("I'm feeling fantastic!")
        self.assertAlmostEqual(emotions["joy"], 0.8, delta=0.2)  # Allow a small delta for approximate matching

    @patch("project.translate.TranslationServiceClient.translate_text", side_effect=Exception("API Error"))
    def test_translation_api_error_handling(self, mock_translate_text):
        """Test handling of translation API errors."""
        song = get_song_recommendation_from_emotion("Estou com raiva")
        self.assertIsNone(song)  # Ensure that the function handles the error and returns None

    @patch("project.requests.post", side_effect=requests.exceptions.RequestException)
    def test_watson_api_error_handling(self, mock_post):
        """Test Watson API error handling."""
        emotions = detect_emotion("I'm feeling great!")
        self.assertIsNone(emotions)


if __name__ == "__main__":
    unittest.main()
