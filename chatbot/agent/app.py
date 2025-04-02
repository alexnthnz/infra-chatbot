import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

from config.settings import settings

app = FastAPI(title="Agent Model Inference Service")

# Initialize a sentiment-analysis pipeline for basic analysis.
analyzer = pipeline("sentiment-analysis", model=settings.sentiment_model)

# Initialize a zero-shot classification pipeline to dynamically decide if internet access is needed.
# We use the "facebook/bart-large-mnli" model as an example.
classifier = pipeline("zero-shot-classification", model=settings.internet_classifier_model)

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
    
    # Use the sentiment-analysis pipeline for basic analysis.
    result = analyzer(request.prompt)[0]
    
    # Use zero-shot classification to decide if the prompt needs internet access.
    classification = classifier(request.prompt, candidate_labels=settings.candidate_labels)
    score_requires = classification["scores"][0] if classification["labels"][0] == "requires internet access" else classification["scores"][1]
    score_does_not = classification["scores"][0] if classification["labels"][0] == "does not require internet access" else classification["scores"][1]

    # Example threshold logic: if difference is less than 0.1, decide it does not require internet.
    requires_internet = (score_requires - score_does_not) > 0.1 and classification["labels"][0] == "requires internet access"
    
    return AnalysisResponse(
        analysis=request.prompt,
        score=result["score"],
        label=result["label"],
        requires_internet=requires_internet
    )

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
