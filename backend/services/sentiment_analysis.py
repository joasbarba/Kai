from typing import List, Dict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import json

class SentimentAnalysisService:
    def __init__(self):
        # Download recursos necessários do NLTK
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        self.sentiment_history = []

    async def analyze_text(self, text: str) -> Dict:
        """
        Analisa o sentimento de um texto
        """
        scores = self.sia.polarity_scores(text)
        
        analysis = {
            "text": text,
            "scores": scores,
            "timestamp": datetime.now().isoformat(),
            "overall_sentiment": self._get_sentiment_label(scores['compound'])
        }
        
        self.sentiment_history.append(analysis)
        return analysis

    async def analyze_community_mood(self, time_period: str = "day") -> Dict:
        """
        Analisa o sentimento geral da comunidade em um período
        """
        if not self.sentiment_history:
            return {"message": "Sem dados suficientes para análise"}

        # Filtra histórico pelo período
        cutoff = self._get_cutoff_date(time_period)
        recent_sentiments = [
            s for s in self.sentiment_history 
            if datetime.fromisoformat(s['timestamp']) > cutoff
        ]

        if not recent_sentiments:
            return {"message": "Sem dados no período especificado"}

        # Calcula médias
        avg_compound = sum(s['scores']['compound'] for s in recent_sentiments) / len(recent_sentiments)
        
        return {
            "period": time_period,
            "average_sentiment": self._get_sentiment_label(avg_compound),
            "sentiment_score": avg_compound,
            "sample_size": len(recent_sentiments),
            "timestamp": datetime.now().isoformat()
        }

    def _get_sentiment_label(self, compound_score: float) -> str:
        """
        Converte score numérico em label de sentimento
        """
        if compound_score >= 0.05:
            return "Positivo"
        elif compound_score <= -0.05:
            return "Negativo"
        else:
            return "Neutro"

    def _get_cutoff_date(self, time_period: str) -> datetime:
        """
        Calcula data de corte baseada no período
        """
        now = datetime.now()
        if time_period == "day":
            return now - timedelta(days=1)
        elif time_period == "week":
            return now - timedelta(weeks=1)
        elif time_period == "month":
            return now - timedelta(days=30)
        else:
            return now - timedelta(days=1)  # default para um dia 