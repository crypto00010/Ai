FROM python:3.11-slim

WORKDIR /app

# Install system deps for llama-cpp
RUN apt-get update && apt-get install -y wget gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Download model during build (or use persistent volume)
RUN wget -O model.gguf "https://huggingface.co/Novaciano/DOLPHIN3.0-L3.2-1B_RP_UNCENSORED-GGUF"

CMD ["python", "main.py"]
