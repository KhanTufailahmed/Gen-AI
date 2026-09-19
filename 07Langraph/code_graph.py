from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

client = OpenAI()


class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool


class State(TypedDict):
    _user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None


def classify_message(state: State):
    query = state["_user_query"]

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
    Return the response in specified JSON boolean only    
    """
    # Structured Output/Responses using pydentic
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    is_coding_question=response.choices[0].message.parsed.
