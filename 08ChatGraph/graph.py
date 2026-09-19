# flake8: noqa
from typing import TypedDict
from typing import Annotated,List
from langgraph.graph import StateGraph,add_messages



class State(TypedDict):
    messages: Annotated[List,add_messages]