from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

# Path where model will be saved
MODEL_PATH = "/data/model.gguf"

# Create folder if it doesn't exist
os.makedirs("/data", exist_ok=True)

print("🔄 Loading Dolphin 1B model...")

try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=256,      # Keep small
        n_threads=2,    # Use 2 threads
        n_batch=64,     # Small batch
        use_mlock=False,
        verbose=False
    )
    print("✅ Model loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    llm = None

# Define request format
class Prompt(BaseModel):
    text: str

# Test endpoint
@app.get("/")
def home():
    return {"message": "Dolphin 1B is running!"}

# Main AI endpoint
@app.post("/generate")
def generate(prompt: Prompt):
    if not llm:
        return {"error": "Model not loaded"}
    
    response = llm(
        prompt.text,
        max_tokens=120,
        temperature=0.8,
        top_p=0.95
    )
    
    return {"response": response["choices"][0]["text"]}

# For Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
