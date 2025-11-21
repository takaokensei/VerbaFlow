"""
Definições das tasks do sistema VerbaFlow.
"""
from crewai import Task


def create_classification_task(agent, text: str):
    """
    Cria a Task 1: Classificação do texto.
    
    Args:
        agent: Agente Analista
        text: Texto a ser classificado
    
    Returns:
        Task configurada
    """
    return Task(
        description=f"""
        Analise o seguinte texto e classifique-o em UMA das 20 categorias do dataset 20 Newsgroups.
        
        Texto a classificar:
        {text}
        
        IMPORTANTE: Seu output DEVE conter exatamente a seguinte linha:
        Category: <nome_da_categoria>
        
        Onde <nome_da_categoria> é uma das seguintes categorias:
        - alt.atheism
        - comp.graphics
        - comp.os.ms-windows.misc
        - comp.sys.ibm.pc.hardware
        - comp.sys.mac.hardware
        - comp.windows.x
        - misc.forsale
        - rec.autos
        - rec.motorcycles
        - rec.sport.baseball
        - rec.sport.hockey
        - sci.crypt
        - sci.electronics
        - sci.med
        - sci.space
        - soc.religion.christian
        - talk.politics.guns
        - talk.politics.mideast
        - talk.politics.misc
        - talk.religion.misc
        
        Seja preciso e justifique brevemente sua escolha.
        """,
        agent=agent,
        expected_output="Output contendo 'Category: <nome_da_categoria>' seguido de uma breve justificativa."
    )


def create_enrichment_task(agent, classification_task):
    """
    Cria a Task 2: Enriquecimento com contexto web.
    
    Args:
        agent: Agente Pesquisador
        classification_task: Task de classificação (para usar como contexto)
    
    Returns:
        Task configurada
    """
    return Task(
        description="""
        Com base na classificação realizada na task anterior, extraia o nome da categoria identificada 
        e busque informações atualizadas e contexto moderno sobre esse tópico na web.
        
        Use a ferramenta Tavily para encontrar:
        - Notícias recentes relacionadas ao tópico
        - Tendências atuais
        - Contexto adicional relevante
        
        Forneça um resumo conciso das informações encontradas.
        """,
        agent=agent,
        context=[classification_task],
        expected_output="Resumo do contexto web encontrado sobre a categoria identificada, incluindo informações atualizadas."
    )


def create_reporting_task(agent, classification_task, enrichment_task):
    """
    Cria a Task 3: Compilação do relatório final.
    
    Args:
        agent: Agente Editor Chefe
        classification_task: Task de classificação
        enrichment_task: Task de enriquecimento
    
    Returns:
        Task configurada
    """
    return Task(
        description="""
        Compile um relatório completo em Markdown, escrito em português brasileiro (pt-BR), que inclua:
        
        1. **Classificação Realizada:**
        Use os resultados da task de classificação anterior.
        
        2. **Contexto Web Encontrado:**
        Use os resultados da task de enriquecimento anterior.
        
        3. **Análise Final:**
        - Resumo da classificação
        - Relevância do contexto encontrado
        - Conclusões
        
        O relatório deve ser profissional, bem formatado em Markdown e totalmente em português brasileiro.
        """,
        agent=agent,
        context=[classification_task, enrichment_task],
        expected_output="Relatório completo em Markdown, em português brasileiro, contendo classificação, contexto web e análise final."
    )

