#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run black on the src directory
black src/

# Also format any Python files in the root directory, if they exist
if ls *.py 1> /dev/null 2>&1; then
    black *.py
fi

echo "Black formatting completed." 