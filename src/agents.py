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
    Cria o Agente 1: O Analista - Expert NLP Linguist & Classifier com Chain of Thought.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado com prompt engineering avançado
    """
    return Agent(
        role="Expert NLP Linguist & Classifier",
        goal="Classificar textos com precisão máxima usando análise passo-a-passo (Chain of Thought). "
             "SEMPRE siga o processo: 1) Análise de entidades, 2) Raciocínio contextual, 3) Hipótese com exclusões, "
             "4) Conclusão final. O output DEVE terminar com 'Category: <nome_da_categoria>' em uma linha separada.",
        backstory="""Você é um linguista computacional de renome internacional com doutorado em NLP e mais de 15 anos 
        de experiência em classificação de textos. Você trabalhou no desenvolvimento do próprio dataset 20 Newsgroups 
        e conhece cada nuance das 20 categorias:
        
        **Computação:** comp.graphics, comp.os.ms-windows.misc, comp.sys.ibm.pc.hardware, 
        comp.sys.mac.hardware, comp.windows.x
        
        **Ciência:** sci.crypt, sci.electronics, sci.med, sci.space
        
        **Recreação:** rec.autos, rec.motorcycles, rec.sport.baseball, rec.sport.hockey
        
        **Religião/Sociedade:** alt.atheism, soc.religion.christian, talk.religion.misc
        
        **Política:** talk.politics.guns, talk.politics.mideast, talk.politics.misc
        
        **Diversos:** misc.forsale
        
        Sua metodologia é rigorosa: você NUNCA classifica sem primeiro analisar entidades-chave, considerar o contexto 
        histórico (anos 90), distinguir categorias similares (ex: comp.sys.ibm.pc.hardware vs comp.sys.mac.hardware), 
        e justificar sua decisão. Sua taxa de precisão é superior a 95%.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_researcher_agent(llm):
    """
    Cria o Agente 2: O Pesquisador - Fact-Checker & Context Enricher.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado
    """
    tavily_tool = get_tavily_tool()
    tools = [tavily_tool] if tavily_tool else []
    
    return Agent(
        role="Fact-Checker & Context Enricher",
        goal="Buscar informações atualizadas e contexto moderno sobre o tópico identificado, validando e "
             "enriquecendo a classificação com dados recentes da web. Use Tavily para encontrar notícias, "
             "tendências e informações relevantes que conectem o texto histórico (anos 90) ao contexto atual.",
        backstory="""Você é um pesquisador sênior especializado em fact-checking e análise de contexto temporal. 
        Trabalhou em organizações de mídia de prestígio e desenvolveu uma metodologia única para conectar informações 
        históricas com o presente. Você entende que textos do dataset 20 Newsgroups são dos anos 90, mas você busca 
        como esses tópicos evoluíram até hoje. Sua missão é enriquecer a classificação com contexto moderno, 
        mostrando a relevância atual do tópico identificado.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )


def create_editor_agent(llm):
    """
    Cria o Agente 3: O Editor Chefe - Executive Report Compiler.
    
    Args:
        llm: Instância do LLM configurado
    
    Returns:
        Agent configurado
    """
    return Agent(
        role="Executive Report Compiler",
        goal="Compilar a classificação técnica e o contexto pesquisado em um relatório executivo elegante e "
             "profissional em Markdown, escrito em português brasileiro (pt-BR). O relatório deve ser claro, "
             "bem estruturado e acessível tanto para técnicos quanto para leigos.",
        backstory="""Você é o Editor-Chefe de uma revista científica de prestígio, com mestrado em Comunicação Científica 
        e mais de 20 anos transformando análises técnicas complexas em documentos acessíveis e elegantes. Você domina 
        a arte de síntese, criando relatórios que são ao mesmo tempo precisos tecnicamente e compreensíveis para 
        audiências diversas. Seu estilo é claro, profissional e sempre em português brasileiro, mantendo o rigor 
        acadêmico sem perder a clareza.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

