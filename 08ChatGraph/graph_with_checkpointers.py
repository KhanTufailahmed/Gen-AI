# flake8: noqa
from typing import TypedDict
from typing import Annotated,List
from langgraph.graph import StateGraph,add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()

class State(TypedDict):
    messages: Annotated[List,add_messages]
    

llm=init_chat_model(model_provider="openai",model="gpt-4.1")

def chat_node(state:State): 
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph_builder=StateGraph(State)

graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START,"chat_node") 
graph_builder.add_edge("chat_node",END)   



def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer=graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer
    


def main():
    # "mongodb://<username>:<password>@<imagename>:port"
    DB_URI="mongodb://admin:admin@mongodb:27017"
    config={"configurable": {"thread_id": "1"}}
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo=compile_graph_with_checkpointer(mongo_checkpointer)

    
        query=input(">")
        graph_result = graph_with_mongo.invoke(
            {"messages":[{"role":"user","content":query}]},config
            )
        print(graph_result)
    
main()
    