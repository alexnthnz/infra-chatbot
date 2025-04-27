from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import logging

from langchain_ollama import ChatOllama
from src.config.settings import settings
from src.app.rag_service import RAGService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama chat model via LangChain
chat_model = ChatOllama(
    model="llama3.2:1b",
    max_tokens=settings.code_model_max_length,
    temperature=settings.code_model_default_temperature,
    top_p=settings.code_model_default_top_p,
)


# Pydantic models for request validation
class ToolResult(BaseModel):
    result: str
    metadata: Dict[str, str] = {}


class InvocationRequest(BaseModel):
    prompt: str
    tool_result: Optional[ToolResult] = None


# Initialize services
rag_service = RAGService()


@app.post("/invocations")
async def sagemaker_invocations(request: InvocationRequest):
    """
    SageMaker-compatible endpoint for RAG-based generation.
    Accepts a user prompt and optional tool results for embedding.
    Returns a non-streaming response.
    """
    try:
        # Extract query
        query = request.prompt
        if not query:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Embed tool result if provided
        if request.tool_result:
            logger.info(f"Embedding tool result: {request.tool_result.result}")
            rag_service.embed_tool_result(
                tool_result=request.tool_result.result, metadata=request.tool_result.metadata
            )

        # Retrieve documents and build RAG prompt
        formatted_rag_prompt, sources = await rag_service.build_rag_prompt(query=query)

        # Non-streaming response
        response = chat_model.invoke(formatted_rag_prompt)
        generated_text = response.content

        return {"generated_code": generated_text.strip(), "sources": sources}

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Invocation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/ping")
async def sagemaker_ping():
    return {"status": "healthy"}
