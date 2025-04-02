import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agent Model Inference Service")


# Lazy-load models with error handling
def get_analyzer():
    try:
        return pipeline("sentiment-analysis", model=settings.sentiment_model)
    except Exception as e:
        logger.error(f"Failed to load sentiment model: {e}")
        raise


def get_classifier():
    try:
        return pipeline("zero-shot-classification", model=settings.internet_classifier_model)
    except Exception as e:
        logger.error(f"Failed to load classifier model: {e}")
        raise


analyzer = get_analyzer()
classifier = get_classifier()


# Request model for incoming prompts.
class PromptRequest(BaseModel):
    prompt: str


# Response model that includes analysis details.
class AnalysisResponse(BaseModel):
    analysis: str
    score: float
    label: str
    requires_internet: bool


@app.post("/invocations", response_model=AnalysisResponse)
async def analyze_prompt(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")

    try:
        # Sentiment analysis
        result = analyzer(request.prompt)[0]

        # Zero-shot classification
        classification = classifier(request.prompt, candidate_labels=settings.candidate_labels)
        score_requires = classification["scores"][classification["labels"].index("requires internet access")]
        score_does_not = classification["scores"][classification["labels"].index("does not require internet access")]

        # Configurable threshold
        threshold = getattr(settings, "internet_threshold", 0.1)
        requires_internet = (score_requires - score_does_not) > threshold

        return AnalysisResponse(
            analysis=request.prompt,
            score=result["score"],
            label=result["label"],
            requires_internet=requires_internet
        )
    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
