from openai import OpenAI

from dotenv import load_dotenv

from datetime import datetime
import requests
import json
import os


load_dotenv()

client = OpenAI()


def runCommand(command: str):
    res = os.system(command)
    return res


def getWheather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    else:
        return "some error occured"


available_tools = {
    "getWheather": getWheather,
    "runCommand": runCommand
    }

SYSTEM_PROMPT = f"""
    Yor are a Helpfull AI assistant.
    You work on start, plan, action, observe mode.
    
    For the gievn user query and available tools, plan the step by step execution, based on planning,
    select the relevant tools from the aviable tools, and based on the tools selection you perform an action to call the tool.
    
    wait for the observation and based on the obervation from the tool call resolve the query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query.
    
    Output JSON Format:
    {{
        "step":"string",
        "content":"string",
        "function":"The name of the function if the step is function",
        "input":"The input parameter for the function"
    }}
    
    
    Available Tools:
    -"getWheather": Takes a city name as an input and returns the current weather for the city.
    -"runCommand": Takes a windows(Or which ever os) command as an string and executes the command and returns the output after executing it.
    Example:
    User Query: What is the wheather in New York?
    Output:{{"step":"plan","content":"The user is interested in weather data of New York"}}
    Output:{{"step":"plan","content":"From the available tool i should call getWheather"}}
    Output:{{"step":"action","function":"getWheather","input":"New York"}}
    Output:{{"step":"observer","output":"12 Degree Cel"}}
    Output:{{"step":"output","content":"The weather for new york seems to be 12 degrees."}}
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# query=input("Enter your query: \n\n")

# messages.append({"role":"user","content":query})
# response=client.chat.completions.create(
#     model="gpt-4.1",
#     messages=[
#         {"role":"system","content":SYSTEM_PROMPT},
#         {"role":"user","content":"What is the wheather of Delhi?"},
#         {"role":"assistant","content":json.dumps({"step":"plan","content":"The user is interested in the weather data of Delhi."})},
#         {"role":"assistant","content":json.dumps({"step": "plan", "content": "From the available tools, I should call getWheather to retrieve the weather data for Delhi."})},
#         {"role":"assistant","content":json.dumps({"step":"action","function":"getWheather","input":"Delhi"})},
#         {"role":"user","content":json.dumps({"step":"observer","output":"-10"})},

#     ]
# )
# messages.append({"role":"user","content":query})


while True:
    query = input("> Enter your query: \n\n")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1", response_format={"type": "json_object"}, messages=messages
        )

        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(response.choices[0].message.content),
            }
        )
        parsed_response = json.loads(response.choices[0].message.content)
        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            continue
        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            print(f" Calling {tool_name} with input: {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append(
                    {
                        "role": "user",
                        "content": json.dumps({"step": "observer", "output": output}),
                    }
                )
                continue
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
