# flake8: noqa
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

client = OpenAI()


class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class ValidateQueryResponse(BaseModel):
    accuracy_percentage:str

class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None


def classify_message(state: State):
    print("⚠️ classify_message")
    query = state["user_query"]

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
    Return the response in specified JSON boolean only    
    """
    # Structured Output/Responses using pydentic
    response = client.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ], 
    )

    is_coding_question = response.choices[0].message.parsed.is_coding_question
    state["is_coding_question"] = is_coding_question
    
    return state


def route_query(state: State) -> Literal["general_query", "coding_query"]:
    print("⚠️ route_query")
    is_coding = state["is_coding_question"]
    if is_coding:
        return "coding_query"
    else:
        return "general_query"


def general_query(state: State):
    print("⚠️ general_query ")

    user_query = state["user_query"]
    
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to simply talk and have chat with the user query.  
    """
    
    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ], 
        )
    state["llm_result"]=response.choices[0].message.content
    
    return state
     

def coding_query(state: State):
    print("⚠️ coding_query")

    user_query = state["user_query"]
        
    SYSTEM_PROMPT = """
        You are an Coding expert agent. Your job is to solve is the user query related to coding only if the query is not realated to coding kindly roste the user also if the query is related to query make sure that the user gets his ans properly and simple and understandable way with proper coding  example.  
        """
        
    response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query},
                ], 
            )
    state["llm_result"]=response.choices[0].message.content
        
    return state
       

def coding_validate_query(state: State):
    print("⚠️ coding_validate_query ")
    user_query = state["user_query"]
    llm_result = state["llm_result"]
     
    SYSTEM_PROMPT = f"""
        You are expert in calculating the accuracy of the code according to the question.
        Return the percentage of the accuracy
        User Query:{user_query}
        code:{llm_result}
    """
    response = client.chat.completions.parse(
        model="gpt-4.1",
        response_format=ValidateQueryResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ]
    )
    state["accuracy_percentage"]=response.choices[0].message.parsed.accuracy_percentage
    
    return state

    
    
graph_builder = StateGraph(State)

graph_builder.add_node("classify_message", classify_message)

graph_builder.add_node("route_query", route_query)

graph_builder.add_node("general_query", general_query)

graph_builder.add_node("coding_query", coding_query)

graph_builder.add_node("coding_validate_query", coding_validate_query)

graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "coding_validate_query")
graph_builder.add_edge("coding_validate_query", END)

graph=graph_builder.compile()


def main():
    user_query=input("Please enter your query: \n\n")
    
    _state={
        "user_query": user_query,
        "llm_result": None,
        "accuracy_percentage": None,
        "is_coding_question":  False
    }
    
    graph_result=graph.invoke(_state)
    print(graph_result)



main()