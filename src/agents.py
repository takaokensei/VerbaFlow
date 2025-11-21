"""
Definições dos agentes do sistema VerbaFlow.
Suporta Groq (primário) e Gemini (fallback).
"""
import os
from typing import Optional
from langchain_groq import ChatGroq
from crewai import Agent
from crewai.llm import LLM
from src.tools import get_tavily_tool
from src.config import get_config

# Import opcional do Gemini (pode não estar instalado)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Import LiteLLM para verificar disponibilidade
try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


def get_llm(model_name: Optional[str] = None, provider: str = "groq") -> LLM:
    """
    Configura e retorna o LLM com suporte a múltiplos provedores.
    
    Args:
        model_name: Nome do modelo a usar. Se None, usa o padrão do provider.
        provider: "groq" (padrão) ou "gemini" (fallback)
    
    Returns:
        LLM configurado
    
    Raises:
        ValueError: Se as credenciais necessárias não estiverem disponíveis
    """
    config = get_config()
    
    if provider == "groq":
        api_key = config.groq_api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            # Verificar se há chave do Gemini disponível para fallback
            gemini_key = (
                config.google_api_key or 
                os.getenv("GOOGLE_API_KEY") or 
                os.getenv("GEMINI_API_KEY")
            )
            if config.use_gemini_fallback and gemini_key:
                # Fallback automático para Gemini
                return get_llm(model_name=config.gemini_model, provider="gemini")
            raise ValueError("GROQ_API_KEY não encontrada e fallback Gemini não configurado")
        
        model = model_name or config.groq_model
        
        return LLM(
            model=model,
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=config.temperature
        )
    
    elif provider == "gemini":
        if not LITELLM_AVAILABLE:
            raise ValueError("LiteLLM não está disponível. Instale: pip install litellm")
        
        # Aceitar tanto GOOGLE_API_KEY quanto GEMINI_API_KEY
        api_key = config.google_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY ou GEMINI_API_KEY não encontrada nas variáveis de ambiente")
        
        model = model_name or config.gemini_model
        
        # Definir a chave do Google como variável de ambiente para LiteLLM
        os.environ["GEMINI_API_KEY"] = api_key
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # IMPORTANTE: O CrewAI tenta usar o provider nativo do Gemini primeiro
        # Para forçar o uso do LiteLLM, precisamos usar um formato que o CrewAI não reconheça como nativo
        # Solução: Usar formato LiteLLM com prefixo explícito que força LiteLLM
        # Formato: "gemini/<modelo>" - mas o CrewAI ainda tenta o provider nativo primeiro
        # Alternativa: Usar um nome de modelo que force LiteLLM diretamente
        
        # Tentar usar formato que força LiteLLM
        # O LiteLLM aceita "gemini/gemini-1.5-pro" ou apenas "gemini-1.5-pro" com GEMINI_API_KEY
        gemini_model_name = f"gemini/{model}" if not model.startswith("gemini/") else model
        
        # O problema: CrewAI detecta "gemini" e tenta usar provider nativo
        # Solução: Usar LangChain LLM diretamente em vez do CrewAI LLM wrapper
        # Mas o CrewAI precisa do seu próprio LLM wrapper...
        
        # Tentar criar LLM do CrewAI - se falhar com provider nativo, o erro será claro
        try:
            return LLM(
                model=gemini_model_name,
                api_key=api_key,
                temperature=config.temperature
            )
        except ImportError as e:
            if "google-genai" in str(e).lower() or "gemini" in str(e).lower():
                # Provider nativo não disponível - mas o CrewAI deveria usar LiteLLM como fallback
                # O problema é que o CrewAI tenta o provider nativo ANTES do LiteLLM
                raise ValueError(
                    f"O CrewAI está tentando usar o provider nativo do Gemini, mas ele não está instalado. "
                    f"O CrewAI deveria usar o LiteLLM automaticamente quando o provider nativo falha, "
                    f"mas isso não está funcionando. "
                    f"\n\nSoluções possíveis:\n"
                    f"1. Instale o provider nativo: pip install 'crewai[google-genai]' (pode falhar)\n"
                    f"2. Use uma versão do CrewAI que suporte LiteLLM como fallback automático\n"
                    f"3. Aguarde o reset do rate limit do Groq\n"
                    f"\nErro original: {e}"
                )
            raise
    
    else:
        raise ValueError(f"Provider '{provider}' não suportado. Use 'groq' ou 'gemini'")


def get_llm_with_fallback(model_name: Optional[str] = None) -> LLM:
    """
    Obtém LLM com fallback automático para Gemini se Groq falhar.
    
    Args:
        model_name: Nome do modelo (opcional)
    
    Returns:
        LLM configurado (Groq ou Gemini)
    """
    config = get_config()
    
    try:
        return get_llm(model_name=model_name, provider="groq")
    except (ValueError, Exception) as e:
        if config.use_gemini_fallback:
            try:
                return get_llm(model_name=config.gemini_model, provider="gemini")
            except Exception as gemini_error:
                raise ValueError(
                    f"Falha ao usar Groq: {e}. "
                    f"Falha ao usar Gemini (fallback): {gemini_error}"
                )
        raise


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

