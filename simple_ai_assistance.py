#standrad library
import os
import json
from types import SimpleNamespace

#third-party library
from dotenv import load_dotenv

#Local Modeule
from Utilities.utilities import build_tools_payload,stream_chat
from Utilities.logger import log
from tools import tool_run
load_dotenv()



#safeguard to prevent infinite loops
MAX_STEPS = 10

messages = [{"role": "system", "content": os.getenv("SYSTEM_MESSAGE_FORMAT")}]


while True:
    user_input = input("👦🏻User: ")
    messages.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the assistant. Goodbye!")
        break
    
    for step in range(MAX_STEPS):
        full_response, tool_calls = stream_chat(messages)
           
        
        if not tool_calls:
             messages.append({"role": "assistant", "content": full_response})
             break

        log(f" 💬 step {step + 1}: Model requested {len(tool_calls)} tool call(s).")

        messages.append({"role": "assistant", "content": full_response,"tool_calls": build_tools_payload(tool_calls)})

        for tool_call in tool_calls:
            result = tool_run(tool_call)
            messages.append({
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
    else:
        fallback = "Maximum steps reached without a final response. Please try again."
        messages.append({"role": "assistant", "content": fallback})
        print("Assistant: " + fallback)
        continue
    
    
