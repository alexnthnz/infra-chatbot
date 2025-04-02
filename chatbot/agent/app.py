import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from config.settings import settings

# Set up logging
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

# Request model for incoming prompts
class PromptRequest(BaseModel):
    prompt: str

# Response model that includes analysis details
class AnalysisResponse(BaseModel):
    analysis: str
    score: float
    label: str
    requires_internet: bool
    additional_info: str | None = None  # Still included in model, but not populated

# Simple heuristic to detect questions
def is_question(prompt: str) -> bool:
    return prompt.strip().endswith("?")

@app.post("/invocations", response_model=AnalysisResponse)
async def analyze_prompt(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")

    try:
        prompt = request.prompt.lower().strip()  # Normalize for consistency

        # Handle questions vs. statements
        if is_question(prompt):
            # Default for questions: neutral, no common knowledge check
            label = "NEUTRAL"
            score = 0.5
        else:
            # Sentiment analysis for statements
            result = analyzer(prompt)[0]
            label = result["label"]
            score = result["score"]

        # Zero-shot classification for internet requirement
        candidate_labels = ["requires internet access", "does not require internet access"]
        classification = classifier(prompt, candidate_labels=candidate_labels)
        score_requires = classification["scores"][classification["labels"].index("requires internet access")]
        score_does_not = classification["scores"][classification["labels"].index("does not require internet access")]

        # Configurable threshold
        threshold = getattr(settings, "internet_threshold", 0.3)  # Kept stricter threshold
        requires_internet = (score_requires - score_does_not) > threshold

        return AnalysisResponse(
            analysis=prompt,
            score=score,
            label=label,
            requires_internet=requires_internet,
            additional_info=None  # Explicitly set to None
        )
    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
