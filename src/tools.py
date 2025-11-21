"""
Configuração de ferramentas para os agentes.
"""
import os
from crewai_tools import TavilySearchTool


def get_tavily_tool():
    """
    Configura e retorna a ferramenta Tavily Search.
    
    Returns:
        TavilySearchTool configurada ou None se API key não estiver disponível
    """
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        print("AVISO: TAVILY_API_KEY não encontrada nas variáveis de ambiente")
        return None
    
    return TavilySearchTool(api_key=api_key)

