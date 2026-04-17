from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Get your free token from https://huggingface.co/settings/tokens
TOKEN = os.getenv("HF_TOKEN", "")

class Message(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Running"}

@app.post("/generate")
def generate(msg: Message):
    if not TOKEN:
        return {"error": "No token"}
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/cognitivecomputations/dolphin-3.0-mistral-7b",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"inputs": msg.text}
    )
    
    try:
        result = response.json()
        if isinstance(result, list):
            return {"response": result[0]["generated_text"]}
        return {"response": str(result)}
    except:
        return {"error": str(response.text)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
