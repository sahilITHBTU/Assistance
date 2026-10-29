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
messages = [{"role": "system", "content": os.getenv("SYSTEM_MESSAGE_FORMAT")}]

while True:
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the assistant. Goodbye!")
        break
    response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=messages,
    tools = TOOLS
   
)
    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append({"role": "assistant", "content": msg.content})
        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}")

            fn = Functions_Name_To_Function_Map[function_name]
            result = fn(**function_args)

            messages.append({
                "role":"tool",
                "tool_id": tool_call.id,
                "content": str(result)
            })

        Response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            
        )   
        msg = Response.choices[0].message
    messages.append({"role": "assistant", "content": msg.content})
    

   # print("LLM response:" + response.choices[0].message.content)
    print("Assistant: " + msg.content)

    print("Send exit to quit the chat")