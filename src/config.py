"""
Configuração centralizada do VerbaFlow usando Pydantic Settings.
Suporta carregamento de .env, variáveis de sistema e segredos do Streamlit.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class VerbaFlowConfig(BaseSettings):
    """
    Configuração centralizada do VerbaFlow.
    
    Prioridade de carregamento:
    1. Variáveis de ambiente do sistema
    2. Arquivo .env
    3. Valores padrão
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    groq_api_key: Optional[str] = Field(
        default=None,
        description="Groq API Key para modelos Llama/Mixtral"
    )
    
    tavily_api_key: Optional[str] = Field(
        default=None,
        description="Tavily API Key para busca web"
    )
    
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google API Key para Gemini (fallback). Aceita também GEMINI_API_KEY"
    )
    
    # Configurações de Modelo
    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Modelo Groq a ser usado"
    )
    
    gemini_model: str = Field(
        default="gemini-pro",  # Usar gemini-pro como padrão (mais compatível com v1beta)
        description="Modelo Gemini a ser usado como fallback. Opções: gemini-pro, gemini-1.5-flash, gemini-1.5-pro"
    )
    
    # Configurações de Execução
    use_gemini_fallback: bool = Field(
        default=True,
        description="Usar Gemini como fallback se Groq falhar"
    )
    
    max_retries: int = Field(
        default=3,
        description="Número máximo de tentativas em caso de erro"
    )
    
    temperature: float = Field(
        default=0.1,
        description="Temperatura do modelo (0.0-1.0)"
    )
    
    # Configurações de UI
    enable_history: bool = Field(
        default=True,
        description="Habilitar histórico de execuções"
    )
    
    max_history_items: int = Field(
        default=5,
        description="Número máximo de itens no histórico"
    )


# Instância global de configuração
_config: Optional[VerbaFlowConfig] = None


def get_config() -> VerbaFlowConfig:
    """
    Retorna a instância global de configuração (singleton).
    
    Suporta tanto GOOGLE_API_KEY quanto GEMINI_API_KEY como variáveis de ambiente.
    
    Returns:
        VerbaFlowConfig: Configuração carregada
    """
    global _config
    if _config is None:
        _config = VerbaFlowConfig()
        # Se google_api_key não foi definida mas GEMINI_API_KEY existe, usar ela
        if not _config.google_api_key:
            import os
            gemini_key = os.getenv("GEMINI_API_KEY")
            if gemini_key:
                _config.google_api_key = gemini_key
    return _config


def reload_config():
    """
    Recarrega a configuração (útil para testes ou mudanças dinâmicas).
    """
    global _config
    _config = VerbaFlowConfig()

