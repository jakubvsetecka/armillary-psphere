FROM python:3.9-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Git LFS
RUN git lfs install

# Clone llama.cpp repository
RUN git clone https://github.com/ggerganov/llama.cpp && \
    git lfs clone https://huggingface.co/Snowflake/snowflake-arctic-embed-s

# Build llama.cpp
WORKDIR /app/llama.cpp
RUN make

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# convert
RUN python3 convert_hf_to_gguf.py ../snowflake-arctic-embed-s/ --outfile model-f16.gguf

EXPOSE 8080

# Start the server (adjust as needed)
CMD ["./llama-server", "-m", "model-f16.gguf", "--embeddings",  "-c", "512", "-ngl", "99", "--host", "0.0.0.0"]
