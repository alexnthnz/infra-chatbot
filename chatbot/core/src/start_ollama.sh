#!/bin/bash

echo "Starting Ollama service..."
ollama serve > /tmp/ollama.log 2>&1 &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start on port 11434..."
for i in {1..30}; do
    if curl -s http://localhost:11434 >/dev/null; then
        echo "Ollama is ready!"
        break
    fi
    sleep 1
done

# Check if Ollama started successfully
if ! curl -s http://localhost:11434 >/dev/null; then
    echo "Error: Ollama failed to start. Check logs:"
    cat /tmp/ollama.log
    exit 1
fi

# Pull the llama3.2:1b model if not already present
echo "Pulling llama3.2:1b model..."
ollama pull llama3.2:1b

echo "Ollama and model are ready. Proceeding with application..."
exec "$@"
