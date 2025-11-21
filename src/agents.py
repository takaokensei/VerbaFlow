"""
Definições dos agentes do sistema VerbaFlow.
"""
import os
from langchain_groq import ChatGroq
from crewai import Agent
from crewai.llm import LLM
from src.tools import get_tavily_tool


def get_llm():
    """
    Configura e retorna o LLM usando Groq via API compatível com OpenAI.
    O CrewAI usa o LLM wrapper que aceita base_url para usar Groq.
    
    Returns:
        LLM configurado para Groq
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada nas variáveis de ambiente")
    
    # Usar o LLM do CrewAI configurado para Groq via API compatível com OpenAI
    # Groq oferece uma API compatível em https://api.groq.com/openai/v1
    # Modelo atualizado: llama-3.3-70b-versatile (substituto do llama-3.1-70b-versatile descontinuado)
    return LLM(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1
    )


def create_analyst_agent(llm):
    """
    Cria o Agente 1: O Analista - Especialista em classificação NLP.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado
    """
    return Agent(
        role="Analista Sênior em Classificação de Textos",
        goal="Classificar textos em uma das 20 categorias do dataset 20 Newsgroups com precisão máxima. "
             "O output DEVE conter exatamente 'Category: <nome_da_categoria>' para permitir parsing automático.",
        backstory="Você é um especialista em Processamento de Linguagem Natural (NLP) com anos de experiência "
                 "em classificação de textos. Você conhece profundamente as 20 categorias do dataset Newsgroups: "
                 "alt.atheism, comp.graphics, comp.os.ms-windows.misc, comp.sys.ibm.pc.hardware, "
                 "comp.sys.mac.hardware, comp.windows.x, misc.forsale, rec.autos, rec.motorcycles, "
                 "rec.sport.baseball, rec.sport.hockey, sci.crypt, sci.electronics, sci.med, sci.space, "
                 "soc.religion.christian, talk.politics.guns, talk.politics.mideast, talk.politics.misc, "
                 "talk.religion.misc. Sua precisão é crucial para o sucesso do sistema.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_researcher_agent(llm):
    """
    Cria o Agente 2: O Pesquisador - Busca contexto moderno.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado
    """
    tavily_tool = get_tavily_tool()
    tools = [tavily_tool] if tavily_tool else []
    
    return Agent(
        role="Pesquisador Especializado em Contexto Web",
        goal="Buscar informações atualizadas e contexto moderno sobre o tópico identificado pelo Analista, "
             "usando a ferramenta Tavily para enriquecer a classificação com dados recentes da web.",
        backstory="Você é um pesquisador experiente que utiliza ferramentas de busca avançadas para encontrar "
                 "informações relevantes e atualizadas na web. Você complementa a classificação do Analista "
                 "com contexto moderno e informações adicionais que ajudam a entender melhor o tópico.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )


def create_editor_agent(llm):
    """
    Cria o Agente 3: O Editor Chefe - Compila relatório final.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado
    """
    return Agent(
        role="Editor Chefe de Relatórios Técnicos",
        goal="Compilar a classificação do Analista e o contexto pesquisado pelo Pesquisador em um relatório "
             "formatado em Markdown, escrito em português brasileiro (pt-BR), de forma clara e profissional.",
        backstory="Você é um editor experiente que transforma análises técnicas em relatórios bem estruturados. "
                 "Você tem a responsabilidade de criar documentos finais que sejam claros, informativos e "
                 "profissionais, sempre em português brasileiro.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

