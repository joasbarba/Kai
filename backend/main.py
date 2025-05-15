from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from services.sacred_texts import SacredTextService
from services.meditation import MeditationService, MeditationSession
from services.sentiment_analysis import SentimentAnalysisService

app = FastAPI(
    title="Templo Híbrido API",
    description="API para o Templo Híbrido Confucionista-Rastafari",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização dos serviços
sacred_texts_service = SacredTextService()
meditation_service = MeditationService()
sentiment_service = SentimentAnalysisService()

# Modelos Pydantic
class SacredQuery(BaseModel):
    question: str
    context: Optional[str] = None

class MeditationRequest(BaseModel):
    duration: int
    type: str
    music: Optional[str] = None

class SentimentRequest(BaseModel):
    text: str

# Rotas da API
@app.get("/")
async def root():
    return {
        "mensagem": "Bem-vindo ao Templo Híbrido Confucionista-Rastafari",
        "status": "online",
        "versao": "1.0.0"
    }

# Rotas para Textos Sagrados
@app.post("/api/sacred/query")
async def query_sacred_texts(query: SacredQuery):
    try:
        results = await sacred_texts_service.search_sacred_texts(query.question)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para Meditação
@app.post("/api/meditation/session")
async def create_meditation_session(session: MeditationRequest):
    try:
        meditation_session = MeditationSession(
            duration=session.duration,
            type=session.type,
            music=session.music
        )
        result = await meditation_service.create_session(meditation_session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/meditation/recommendation")
async def get_meditation_recommendation(preferences: Dict):
    try:
        recommendation = await meditation_service.get_recommendation(preferences)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para Análise de Sentimento
@app.post("/api/sentiment/analyze")
async def analyze_sentiment(request: SentimentRequest):
    try:
        analysis = await sentiment_service.analyze_text(request.text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sentiment/community")
async def get_community_sentiment(time_period: str = "day"):
    try:
        analysis = await sentiment_service.analyze_community_mood(time_period)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 