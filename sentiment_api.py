from fastapi import FastAPI
from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from loguru import logger


logger.add("logs/sentiment_api.log", rotation="500 MB", level="INFO")
app = FastAPI()
sia = SentimentIntensityAnalyzer()


class AnalyseSentimentPayload(BaseModel):
    text: str


@app.post('/analyse_sentiment/')
async def analyse_sentiment(payload: AnalyseSentimentPayload):
    text = payload.text

    logger.info(f"Analyse : {text}")
    try:
        sentiment = sia.polarity_scores(text)
        logger.success(f"Résultat pour : {text}. {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Erreur analyse : {e}")
