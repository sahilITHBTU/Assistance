from dotenv import load_dotenv
import os
import json
from tools import Functions_Name_To_Function_Map, TOOLS
load_dotenv()
from openai import OpenAI
client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)
#safeguard to prevent infinite loops
MAX_STEPS = 10;

messages = [{"role": "system", "content": os.getenv("SYSTEM_MESSAGE_FORMAT")}]

while True:
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the assistant. Goodbye!")
        break
    
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools = TOOLS
           
        )
        print("LLM response(raw):" + str(response))
        msg = response.choices[0].message
        if not msg.tool_calls:
            break
        messages.append({"role": "assistant", "content": msg.content})
        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            function_args = {}
            try:
              function_args = json.loads(tool_call.function.arguments or
               "{}")
              fn = Functions_Name_To_Function_Map[function_name]
              result = fn(**function_args)
            except Exception as e:
                result = f"Error executing function '{function_name}': {str(e)}"

        
            messages.append({
                "role":"tool",
                "tool_id": tool_call.id,
                "content": str(result)
            })
    else:
        fallback = "Maximum steps reached without a final response. Please try again."
        messages.append({"role": "assistant", "content": fallback})
        print("Assistant: " + fallback)
        continue
    
    messages.append({"role": "assistant", "content": msg.content})
    

   # print("LLM response:" + response.choices[0].message.content)
    print("Assistant: " + msg.content)

    print("Send exit to quit the chat")