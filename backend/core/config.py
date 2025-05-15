from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Configurações Básicas
    APP_NAME: str = "Templo Híbrido"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Configurações de Segurança
    SECRET_KEY: str = "sua_chave_secreta_aqui"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias
    
    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql://usuario:senha@localhost:5432/templo_hibrido"
    
    # Configurações da IA
    MODEL_PATH: str = "./models/sacred_model"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Configurações de Mídia
    ALLOWED_EXTENSIONS: List[str] = ["mp3", "wav", "pdf", "txt"]
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    
    class Config:
        case_sensitive = True

settings = Settings() 