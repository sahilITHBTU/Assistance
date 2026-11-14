import os
from types import SimpleNamespace

from openai import OpenAI
from dotenv import load_dotenv

from tools import  TOOLS

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

def build_tools_payload(tool_calls):
    """
    convert our collection of tool calls into a list of dictionaries that can be sent to the API.
    """
    payload = []
    for call in tool_calls:
        payload.append({
            "id": call.id,
            "type": "function",
            "function": {
                "name": call.function.name,
                "arguments": call.function.arguments
            }
        })
    return payload


# content streaming 
def stream_chat(history):
    """
    Streams the chat response from the OpenAI API format"""

    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools = TOOLS,
        stream = True,
    )

    full_Response = ""
    calls = {}
    Label_printed = False

    try:
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            # do we have content from llm
            if delta.content:
                if not Label_printed:
                    print("🤖 Assistant: ",end = "",flush=True)
                    Label_printed = True
                print(delta.content,end= "",flush=True)
                full_Response += delta.content

                # 2. tool_calls
            for tc in (delta.tool_calls or []):
                obj = calls.setdefault(
                    tc.index,
                    SimpleNamespace(id=None,function=SimpleNamespace(name="",arguments=""))
                )
                if tc.id:
                    obj.id = tc.id
                if tc.function and tc.function.name:
                    obj.function.name += tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments += tc.function.arguments
    except KeyboardInterrupt:
        print("Stopped by user")
    if Label_printed:
        print()  # Move to the next line after streaming content
    callList = []
    for key in sorted(calls):
        callList.append(calls[key])
    return full_Response, callList
