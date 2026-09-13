from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "server is running",
    }


@app.post("/chat")
def chat():
    pass
