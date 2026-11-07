from datetime import datetime
import requests

def get_current_time():
    """
    Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def get_city_Weather(city):
    url = f"http://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    return response.text

def get_jokes():
    url = "https://official-joke-api.appspot.com/jokes/random"
    try:
        ResponseJoke = requests.get(url, timeout=10)
        
        if ResponseJoke.status_code == 200:
            try:
                joke_data = ResponseJoke.json()
                setup = joke_data.get("setup", "")
                punchline = joke_data.get("punchline", "")
                
                if setup and punchline:
                    return f"{setup} ... {punchline}"
                return "I found a joke structure, but it was missing the text fields."
            except (requests.exceptions.JSONDecodeError, ValueError):
                return f"Server Error: API did not return valid JSON data. Response: {ResponseJoke.text[:100]}"
        else:
            return f"Joke API Error: Received HTTP status code {ResponseJoke.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Network Error: Unable to reach the joke service. Details: {str(e)}"

TOOLS = [
    {
        "type": "function",
        "function": {
        "name": "get_current_time",
        "description": "Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.",
        "parameters": {
            "type":"object",
            "properties": {

            }
        },
        "return_type": "str"
        }
        
    }
    ,{
        "type": "function",
        "function": {
        "name": "get_city_Weather",
        "description": "Returns the current weather for a given city.",
        "parameters": {
            "type":"object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get the weather for."
                }
            }
        }
        }
    }
    ,{
        "type": "function",
        "function": {
        "name": "get_jokes",
        "description": "Returns a random joke.",
        "parameters": {
            "type":"object",
            "properties": {
            }
        }
        }
    }
]
Functions_Name_To_Function_Map = {
    "get_current_time": get_current_time,
    "get_city_Weather": get_city_Weather,
    "get_jokes": get_jokes
}