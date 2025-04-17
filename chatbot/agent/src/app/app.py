from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.utils.logger import logger
from src.config.settings import settings

from .inference import categorize_prompt, analyze_sentiment, check_internet_requirement

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


class AnalysisResponse(BaseModel):
    processed_prompt: str = Field(
        description="The normalized prompt (no generation in this version)"
    )
    sentiment: SentimentAnalysis = Field(description="Sentiment analysis of the prompt")
    requires_internet: bool = Field(description="Whether the prompt requires internet access")
    category: PromptCategory = Field(description="Category classification of the prompt")


# API endpoints
@app.get("/ping")
async def read_main():
    return {"message": "Pong"}


@app.post("/invocations", response_model=AnalysisResponse)
async def inference(request: PromptRequest):
    """
    Process a user prompt and return an analysis response.

    Args:
        request: PromptRequest containing the user's prompt.

    Returns:
        AnalysisResponse with the processed prompt, sentiment, internet requirement, and category.

    Raises:
        HTTPException: If the prompt is empty or an error occurs during processing.
    """
    # Validate the prompt
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")

    try:
        # Normalize the prompt
        prompt = request.prompt.lower().strip()

        # Step 1: Categorize the prompt
        category_result = categorize_prompt(prompt)
        prompt_category = PromptCategory(
            category=category_result["category"], score=category_result["score"]
        )

        # Step 2: Perform sentiment analysis
        sentiment_result = analyze_sentiment(prompt)
        sentiment = SentimentAnalysis(
            label=sentiment_result["label"], score=sentiment_result["score"]
        )

        # Step 3: Determine if internet access is required
        requires_internet = check_internet_requirement(prompt)

        # Return the structured response
        return AnalysisResponse(
            processed_prompt=prompt,  # No generation, just return the normalized prompt
            sentiment=sentiment,
            requires_internet=requires_internet,
            category=prompt_category,
        )

    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
