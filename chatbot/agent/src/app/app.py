from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from src.utils.logger import logger
from src.config.settings import settings

from .inference import analyze_and_enhance_prompt

app = FastAPI(title=settings.app_name)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class PromptRequest(BaseModel):
    prompt: str


class SentimentAnalysis(BaseModel):
    label: str = Field(description="Sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL)")
    score: float = Field(description="Confidence score for the sentiment label (0 to 1)")


class PromptCategory(BaseModel):
    category: str = Field(description="Category of the prompt (e.g., interrogative, imperative)")
    score: float = Field(description="Confidence score for the category (0 to 1)")


class EnhancedAnalysisResponse(BaseModel):
    original_prompt: str = Field(description="The normalized original prompt")
    enhanced_prompt: str = Field(description="The enhanced version of the prompt")
    sentiment: SentimentAnalysis = Field(description="Sentiment analysis of the prompt")
    requires_internet: bool = Field(description="Whether the prompt requires internet access")
    category: PromptCategory = Field(description="Category classification of the prompt")
    use_search: bool = Field(description="Whether to use search to answer this prompt")
    use_rag: bool = Field(description="Whether to use RAG to answer this prompt")
    reasoning: str = Field(description="Reasoning behind the tool decision")
    error: Optional[str] = Field(default=None, description="Error message if processing failed")


# API endpoints
@app.get("/ping")
async def read_main():
    return {"message": "Pong"}


@app.post("/invocations", response_model=EnhancedAnalysisResponse)
async def inference(request: PromptRequest):
    """
    Analyze a user prompt, enhance it, and decide whether to use search or RAG.

    This endpoint:
    1. Analyzes the prompt (category, sentiment, internet requirements)
    2. Enhances the prompt to make it clearer and more specific
    3. Decides whether to use search or RAG for answering

    Args:
        request: PromptRequest containing the user's prompt.

    Returns:
        EnhancedAnalysisResponse with analysis results and tool decisions.

    Raises:
        HTTPException: If the prompt is empty or an error occurs during processing.
    """
    # Validate the prompt
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")

    try:
        # Use the enhanced prompt analyzer
        result = analyze_and_enhance_prompt(request.prompt)

        # Create response models from the result
        sentiment = SentimentAnalysis(
            label=result["sentiment"]["label"], score=result["sentiment"]["score"]
        )

        category = PromptCategory(
            category=result["category"]["category"], score=result["category"]["score"]
        )

        # Return the enhanced response
        return EnhancedAnalysisResponse(
            original_prompt=result["original_prompt"],
            enhanced_prompt=result["enhanced_prompt"],
            sentiment=sentiment,
            requires_internet=result["requires_internet"],
            category=category,
            use_search=result["use_search"],
            use_rag=result["use_rag"],
            reasoning=result["reasoning"],
            error=result.get("error"),
        )

    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
