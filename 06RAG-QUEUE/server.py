from fastapi import FastAPI, Query
from message_queue.connection import queue
from message_queue.worker import process_query


app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "server is running",
    }


@app.post("/chat")
def chat(query: str = Query( description="Chat Message")):
    job = queue.enqueue(process_query, query)
    return {"status": "Success", "job_id": job.id}
