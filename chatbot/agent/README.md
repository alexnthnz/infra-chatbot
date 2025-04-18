# Agent Model Inference Service

An intelligent prompt processing service that analyzes user prompts, enhances them, and decides whether to use search or RAG for answering.

## Features

- **Prompt Analysis**: Categorizes prompts and performs sentiment analysis
- **Prompt Enhancement**: Improves prompts to be clearer and more specific
- **Tool Decision**: Intelligently decides between Search and RAG based on prompt content
- **AWS Bedrock Integration**: Uses Amazon Bedrock for RAG capabilities
- **Google Search Integration**: Uses Serper API for web search

## Setup

### Prerequisites

- Python 3.10+
- Docker (optional)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
cp .env.example .env
```
Then edit the `.env` file with your API keys and configuration.

### Environment Variables

- `SERPER_API_KEY`: API key for Google Search via Serper
- `OPENAI_API_KEY`: API key for OpenAI models
- `AWS_ACCESS_KEY_ID`: AWS access key with Bedrock permissions
- `AWS_SECRET_ACCESS_KEY`: AWS secret key with Bedrock permissions
- `AWS_REGION_NAME`: AWS region where Bedrock is available
- `AWS_BEDROCK_MODEL_ID`: Bedrock model ID to use for RAG

## Usage

### Running the API Server

Start the FastAPI server:

```
cd src
uvicorn serve_app:app --reload
```

### API Endpoints

- `GET /ping`: Health check endpoint
- `POST /invocations`: Main endpoint for prompt analysis and enhancement

#### Example Request to /invocations

```json
{
    "prompt": "What's the weather in New York?"
}
```

### Example Responses

#### Example 1: When search is recommended (for real-time data)

```json
{
  "original_prompt": "What's the weather in New York?",
  "enhanced_prompt": "What is the current weather forecast for New York City today?",
  "sentiment": {
    "label": "NEUTRAL",
    "score": 0.95
  },
  "requires_internet": true,
  "category": {
    "category": "interrogative",
    "score": 0.98
  },
  "use_search": true,
  "use_rag": false,
  "reasoning": "This question asks about weather conditions which are real-time data that change frequently. Current weather information is not stored in internal documents and requires accessing external weather services or websites."
}
```

#### Example 2: When RAG is recommended (for company-specific information)

```json
{
  "original_prompt": "What is our company's policy on remote work?",
  "enhanced_prompt": "What are the current official policies and guidelines regarding remote work at our company?",
  "sentiment": {
    "label": "NEUTRAL",
    "score": 0.87
  },
  "requires_internet": false,
  "category": {
    "category": "interrogative",
    "score": 0.96
  },
  "use_search": false,
  "use_rag": true,
  "reasoning": "This query asks about internal company policies which would be documented in the company's knowledge base or internal documents. This is domain-specific information that requires access to private company documentation rather than public internet searches."
}
```

## Docker Deployment

Build and run the Docker container:

```
docker build -t agent-inference-service .
docker run -p 8000:8000 --env-file .env agent-inference-service
```

## Testing

Run tests with pytest:

```
pytest
```

## License

[Your License] 