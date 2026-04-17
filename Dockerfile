FROM python:3.11-slim

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY main.py .

# Create data folder for model
RUN mkdir -p /data

# Download the 1B model (this will take 2-3 minutes)
RUN wget -O /data/model.gguf \
    "https://huggingface.co/Novaciano/DOLPHIN3.0-L3.2-1B_RP_UNCENSORED-GGUF/resolve/main/DOLPHIN3.0-L3.2-1B_RP_UNCENSORED.gguf"

# Start the app
CMD ["python", "main.py"]
