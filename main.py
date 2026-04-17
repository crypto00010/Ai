from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

# Download model on startup (or use persistent storage)
MODEL_PATH = "model.gguf"
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    os.system('wget -O model.gguf "https://huggingface.co/Novaciano/DOLPHIN3.0-L3.2-1B_RP_UNCENSORED-GGUF"')

print("Loading Dolphin 1B...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=256,
    n_threads=2,
    n_batch=64,
    use_mlock=False
)
print("Ready ✅")

class Prompt(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Dolphin running on Railway"}

@app.post("/generate")
def generate(prompt: Prompt):
    output = llm(
        prompt.text,
        max_tokens=120,
        temperature=0.8,
        top_p=0.95
    )
    return {"response": output["choices"][0]["text"]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
