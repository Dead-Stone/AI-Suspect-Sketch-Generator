FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio processing and build tools
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    gcc \
    g++ \
    make \
    libasound2-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for generated sketches
RUN mkdir -p generated_sketches

# Expose port 
EXPOSE 8501

# Create startup script
RUN echo '#!/bin/bash\nstreamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none' > /app/start.sh
RUN chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"] 