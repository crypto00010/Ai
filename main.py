from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os
import subprocess

app = FastAPI()

MODEL_PATH = "/data/model.gguf"
os.makedirs("/data", exist_ok=True)

# Download model if missing
if not os.path.exists(MODEL_PATH):
    print("⏳ Downloading model (this takes 3-5 minutes)...")
    result = subprocess.run([
        "wget", "--timeout=600", "-O", MODEL_PATH,
        "https://huggingface.co/cognitivecomputations/dolphin-3.0-mistral-7b-gguf/resolve/main/dolphin-3.0-l3.2-1b-rp_uncensored.gguf?download=true"
    ])
    if result.returncode == 0:
        print("✅ Model downloaded!")
    else:
        print("❌ Download failed")

print("🔄 Loading model into memory...")

try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=256,
        n_threads=2,
        n_batch=64,
        use_mlock=False,
        verbose=False
    )
    print("✅ Model ready!")
except Exception as e:
    print(f"❌ Error: {e}")
    llm = None

class Prompt(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Dolphin 1B running"}

@app.post("/generate")
def generate(prompt: Prompt):
    if not llm:
        return {"error": "Model still loading, try again in 30 seconds"}
    
    response = llm(
        prompt.text,
        max_tokens=120,
        temperature=0.8,
        top_p=0.95
    )
    return {"response": response["choices"][0]["text"]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
