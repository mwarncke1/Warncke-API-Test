import requests

#fetch random joke from API
def getRandomJoke():
    try:
        #send request to joke API with 5 second timeout
        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout = 5)
        #if response is successful return json
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except requests.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}