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
]
Functions_Name_To_Function_Map = {
    "get_current_time": get_current_time,
    "get_city_Weather": get_city_Weather
}