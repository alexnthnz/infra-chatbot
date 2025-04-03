from transformers import pipeline

from src.config.settings import settings
from src.utils.logger import logger


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



