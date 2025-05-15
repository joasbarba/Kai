from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

class MeditationSession(BaseModel):
    duration: int  # em minutos
    type: str  # tipo de meditação
    music: Optional[str] = None
    guidance: Optional[str] = None
    created_at: datetime = datetime.now()

class MeditationService:
    def __init__(self):
        self.sessions: List[MeditationSession] = []
        self.meditation_types = {
            "confucian": {
                "name": "Meditação Confucionista",
                "description": "Foco na harmonia e virtude",
                "duration_options": [10, 20, 30, 45, 60]
            },
            "rastafari": {
                "name": "Meditação Rastafari",
                "description": "Conexão com Jah e natureza",
                "duration_options": [15, 30, 45, 60]
            },
            "hybrid": {
                "name": "Meditação Híbrida",
                "description": "Combinação de práticas",
                "duration_options": [20, 40, 60]
            }
        }

    async def create_session(self, session: MeditationSession) -> MeditationSession:
        """
        Cria uma nova sessão de meditação
        """
        self.sessions.append(session)
        return session

    async def get_recommendation(self, user_preferences: Dict) -> Dict:
        """
        Gera recomendações personalizadas de meditação
        """
        meditation_type = user_preferences.get("type", "hybrid")
        duration = user_preferences.get("duration", 20)
        
        recommendation = {
            "type": self.meditation_types[meditation_type],
            "duration": duration,
            "music": self._get_music_recommendation(meditation_type),
            "guidance": self._get_guidance(meditation_type)
        }
        
        return recommendation

    def _get_music_recommendation(self, meditation_type: str) -> str:
        """
        Recomenda música baseada no tipo de meditação
        """
        music_recommendations = {
            "confucian": "Música tradicional chinesa",
            "rastafari": "Reggae roots",
            "hybrid": "Fusão de sons tradicionais"
        }
        return music_recommendations.get(meditation_type, "Silêncio")

    def _get_guidance(self, meditation_type: str) -> str:
        """
        Fornece orientações específicas para cada tipo de meditação
        """
        guidance = {
            "confucian": "Foque na harmonia interior e virtude",
            "rastafari": "Conecte-se com a energia de Jah",
            "hybrid": "Equilibre as práticas orientais e ocidentais"
        }
        return guidance.get(meditation_type, "Respire profundamente") 