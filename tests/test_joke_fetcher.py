import requests
from unittest.mock import patch
from src.joke_fetcher import getRandomJoke

#test successful api call returns a valid joke
def testGetRandomJokeSuccess():
    #mock response to simulate a valid joke
    mock_response = {
        "type" : "general",
        "setup" : "I could tell you a joke about UDP...",
        "punchline" : "...but I don't know if you'd get it."
    }

    #patch requests.get to simulate a successful api response
    with patch('requests.get') as mock_get:
        #simulating successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = getRandomJoke()

        #assertion to check if expected joke data is returned
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["setup"] == mock_response["setup"]
        assert result["data"]["punchline"] == mock_response["punchline"]

#test a 404 error (not found)
def testGetRandomJokeNotFound():
    with patch('requests.get') as mock_get:
        #simulating a 404 not found error from api
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {}

        result = getRandomJoke()

        #assertion to check if func handles 404 error code correctly
        assert result["success"] is False
        assert result["error"] == "HTTP 404"

#test a 500 error (internal server error)
def testGetRandomJokeServerError():
    with patch('requests.get') as mock_get:
        #simulating a 500 internal server error
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {}

        result = getRandomJoke()
        assert result["success"] is False
        assert result["error"] == "HTTP 500"


#test a timeout error
def testGetRandomJokeTimeout():
    with patch('requests.get', side_effect=requests.Timeout):
        result = getRandomJoke()

        assert result["success"] is False
        assert result["error"] == "Request timed out"