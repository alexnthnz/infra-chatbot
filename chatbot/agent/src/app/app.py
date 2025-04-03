from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.utils.logger import logger
from src.config.settings import settings
from src.utils.utilities import is_question

from .inference import analyzer, classifier

app = FastAPI(title=settings.app_name)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PromptRequest(BaseModel):
    prompt: str


# Response model that includes analysis details
class AnalysisResponse(BaseModel):
    analysis: str
    score: float
    label: str
    requires_internet: bool


@app.get("/ping")
async def read_main():
    return {
        "message": "Pong"
    }


@app.post("/invocations", response_model=AnalysisResponse)
async def inference(request: PromptRequest):
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

