#standrad library
import os
import json

#third-party library
from openai import OpenAI
from dotenv import load_dotenv
from Utilities.utilities import log

#Local Modeule
from tools import  TOOLS,tool_run
load_dotenv()


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
        #print("LLM response(raw):" + str(response))
        msg = response.choices[0].message
        if not msg.tool_calls:
            break

        log(f" 🤖 step {step + 1}: Model requested {len(msg.tool_calls)} tool call(s).")

        messages.append({"role": "assistant", "content": msg.content})

        for tool_call in msg.tool_calls:
            result = tool_run(tool_call)
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
    print("Assistant: " + (msg.content or " "))

    print("Send exit to quit the chat")