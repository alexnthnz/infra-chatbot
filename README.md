# Infra Chatbot

An intelligent infrastructure chatbot system that integrates RAG (Retrieval-Augmented Generation) with a fine-tunable language model to answer infrastructure and deployment related queries.

![Architecture](./assets/image.png)

## Overview

This repository implements a comprehensive chatbot solution designed to assist with infrastructure questions. The system combines:

- A modern web interface built with Next.js
- A RAG pipeline for retrieving relevant context
- LangChain Agent for orchestrating the pipeline
- Fine-tuning capabilities to continuously improve responses

## Components

### Frontend Application (`/app`)
- Next.js web interface
- Responsive UI components
- API integration with the backend

### Chatbot Backend (`/chatbot`)
- **Core**: Central processing engine
- **Agent**: LangChain implementation for query handling
- **Handler**: Request processing and response generation

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- Docker and Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/infra-chatbot.git
   cd infra-chatbot
   ```

2. Set up the frontend:
   ```bash
   cd app
   npm install
   cp .env.example .env  # Configure environment variables
   ```

3. Set up the chatbot backend:
   ```bash
   # Set up core
   cd chatbot/core
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Set up agent
   cd ../agent
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Docker setup (alternative):
   ```bash
   docker-compose up -d
   ```

## Usage

### Starting the application

1. Run the frontend:
   ```bash
   cd app
   npm run dev
   ```

2. Run the backend services:
   ```bash
   # Using Docker
   docker-compose up

   # Or run services individually
   cd chatbot/core
   # Start core service
   
   cd ../agent
   # Start agent service
   ```

3. Access the web interface at `http://localhost:3000`

## Development

### Project Structure
```
infra-chatbot/
├── app/                 # Next.js frontend
│   ├── src/             # Application source code
│   │   ├── components/  # UI components
│   │   ├── app/         # Next.js app router pages
│   │   └── lib/         # Utility functions
├── chatbot/             # Backend services
│   ├── core/            # Core processing engine
│   ├── agent/           # LangChain agent implementation
│   └── handler/         # Request handler service
├── assets/              # Project assets and documentation
└── deploy/              # Deployment configurations
```

### Contributing

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git commit -m "Add your feature description"
   ```

3. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## License

This project is licensed under the MIT License.
