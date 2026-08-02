from openai import OpenAI

from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are a helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyze the input and break down the problem step by step.
    
    The steps are you get a user input, you analyze, you think, you think again, and think for several times and then returns the output with an expert explanation.
    
    Follow the steps in squence that is "analyse", "think", "output", "validate" and finally "results".
    
    Rules:
    1. Follow the stricy JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the use query.
    
    Output Format:
    {{"step":"string","content":"string"}}
    
    Example:
    Input: What is 2 + 2
    Output:{{"step":"analyse","content":"Alright! The user is interest in maths query and he is asking a basic arthematic operation."}}
    Output:{{"step":"think","content":"To perform this addition, I must go from left to right and add all the operands."}}
    Output:{{"step":"output","content":"4"}}
    Output:{{"step":"validate","content":"Seems like 4 is correct ans for 2 + 2"}}
    Output:{{"step":"result","content":"2 + 2 = 4 and this is calculated by adding all numbers"}}
    
"""

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     response_format={"type":"json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content":"What is 5 / 2 * 3 to the power 4"},
#         {"role":"assistant","content":json.dumps({"step":"analyse","content":"The user has provided a mathematical expression: 5 / 2 * 3 to the power 4. They want the result of this calculation."})},
#         {"role":"assistant","content":json.dumps({"step": "think", "content": "The expression is 5 divided by 2, then multiplied by 3 raised to the power 4. According to the order of operations (PEMDAS/BODMAS), exponentiation should be done first, then division and multiplication from left to right."} )},
#         {"role":"assistant","content":json.dumps({"step": "output", "content": "First, calculate 3 to the power 4: 3^4 = 81. Then calculate 5 / 2 = 2.5. Finally, multiply 2.5 * 81 = 202.5."} )},
#         {"role":"assistant","content":json.dumps({"step": "validate", "content": "Checking the steps: 3^4 = 81 is correct, 5 / 2 = 2.5 is correct, and 2.5 * 81 = 202.5 is correct. The calculations are consistent and logical."} )},
#         {"role":"assistant","content":json.dumps({"step": "result", "content": "5 / 2 * 3^4 = 202.5, obtained by first calculating the exponentiation 3^4 = 81, then dividing 5 by 2 to get 2.5, and finally multiplying 2.5 by 81."} )},
#     ],
# )

# print("\n\n🤖:", response.choices[0].message.content ,"\n\n")


messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
]

query=input("Enter your query: \n\n")
messages.append({"role": "user", "content":query})

while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type":"json_object"},
        messages=messages,
    )
    
    messages.append({"role":"assistant","content":response.choices[0].message.content})
    parsed_response=json.loads(response.choices[0].message.content)
    
    if(parsed_response.get("step")!="result"):
        print("    🧠",parsed_response.get("content"))
        continue
    
    print("    🤖",parsed_response.get("content"))
    break