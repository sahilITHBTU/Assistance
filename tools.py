from datetime import datetime

def get_current_time():
    """
    Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
]
Functions_Name_To_Function_Map = {
    "get_current_time": get_current_time,
}