from transformers import pipeline

from src.config.settings import settings
from src.utils.logger import logger
from src.utils.utilities import is_question  # Import is_question

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

def categorize_prompt(prompt: str) -> dict:
    """
    Classify the prompt into a category using zero-shot classification.

    Args:
        prompt: The user's prompt.

    Returns:
        Dict with the category and confidence score.
    """
    try:
        classification = classifier(
            prompt,
            candidate_labels=settings.prompt_categories,
            multi_label=False  # Single category per prompt
        )
        category = classification["labels"][0]  # Most likely category
        score = classification["scores"][0]  # Confidence score for the top category
        return {"category": category, "score": score}
    except Exception as e:
        logger.error(f"Error categorizing prompt: {e}")
        return {"category": "Unknown", "score": 0.0}

def analyze_sentiment(prompt: str) -> dict:
    """
    Analyze the sentiment of the prompt.

    Args:
        prompt: The user's prompt.

    Returns:
        Dict with the sentiment label and score.
    """
    if is_question(prompt):
        return {"label": "NEUTRAL", "score": 0.5}
    result = analyzer(prompt)[0]
    return {"label": result["label"], "score": result["score"]}

def check_internet_requirement(prompt: str) -> bool:
    """
    Determine if the prompt requires internet access.

    Args:
        prompt: The user's prompt.

    Returns:
        Boolean indicating if internet access is required.
    """
    classification = classifier(prompt, candidate_labels=settings.candidate_labels)
    score_requires = classification["scores"][classification["labels"].index("requires internet access")]
    score_does_not = classification["scores"][classification["labels"].index("does not require internet access")]
    threshold = getattr(settings, "internet_threshold", 0.3)
    return (score_requires - score_does_not) > threshold
