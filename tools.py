from datetime import datetime
import json
from duckduckgo_search import DDGS
import requests

from Utilities.utilities import log

def get_current_time():
    """
    Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def get_city_Weather(city):
    url = f"http://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
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

def search_web(query):
    """
    Performs a web search using DuckDuckGo and returns the top 5 results.
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({
                "title": r['title'],
                "url": r['href'],
                "snippet": r['body']
            })
    return json.dumps(results)
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
                },
            },
            "required":["city"]
        },
        },
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
    },
    {
        "type": "function",
        "function": {
        "name": "search_web",
        "description": "Performs a web search using DuckDuckGo and returns the top 5 results.",
        "parameters": {
            "type":"object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                },
            },
            "required":["query"]
        },
        },
    }
]
Functions_Name_To_Function_Map = {
    "get_current_time": get_current_time,
    "get_city_Weather": get_city_Weather,
    "get_jokes": get_jokes,
    "search_web": search_web
}


def tool_run(tool_call):
    function_name = tool_call.function.name
    function_args = {}
    
    try:
       
        function_args = json.loads(tool_call.function.arguments or "{}")
        log(f" {function_name}  {function_args}")
        
       
        fn = Functions_Name_To_Function_Map[function_name]
        result = fn(**function_args)
        
    except Exception as e:
        
        result = f"Error executing function '{function_name}': {str(e)}"
    
   
    log(f" 🔍 Result from {function_name}: {result}")
    return str(result)