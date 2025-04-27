from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from transformers import pipeline

app = FastAPI(title="Sentiment + GenAI API")

model = joblib.load("app/model/sentiment_model.pkl")
generator = pipeline("text-generation", model="distilgpt2")

class InputMessage(BaseModel):
    message: str

@app.post("/analyze/")
def analyze(input: InputMessage):
    sentiment = model.predict([input.message])[0]
    sentimento = "positivo" if sentiment == 1 else "negativo"
    prompt = f"Cliente: {input.message}\nAtendente ({sentimento}):"
    resposta = generator(prompt, max_length=80)[0]["generated_text"]
    return {"sentimento": sentimento, "resposta": resposta}
