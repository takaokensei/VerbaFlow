"""
Definições das tasks do sistema VerbaFlow.
"""
from crewai import Task


def create_classification_task(agent, text: str):
    """
    Cria a Task 1: Classificação do texto com Chain of Thought explícito.
    
    Args:
        agent: Agente Analista
        text: Texto a ser classificado
    
    Returns:
        Task configurada com CoT
    """
    return Task(
        description=f"""
        Analise o seguinte texto usando a metodologia Chain of Thought (CoT). Siga EXATAMENTE estes 4 passos:
        
        **TEXTO A CLASSIFICAR:**
        {text}
        
        ---
        
        **PASSO 1: ANÁLISE DE ENTIDADES**
        Identifique e liste:
        - Organizações mencionadas (ex: IBM, Apple, Microsoft, NASA)
        - Termos técnicos específicos (ex: "encryption", "hardware", "software")
        - Domínios de conhecimento (ex: medicina, ciência espacial, criptografia)
        - Contexto temporal (anos 90 - tecnologia da época)
        
        **PASSO 2: RACIOCÍNIO CONTEXTUAL**
        Conecte as entidades identificadas às definições das 20 categorias:
        - alt.atheism: Discussões sobre ateísmo
        - comp.graphics: Computação gráfica, visualização
        - comp.os.ms-windows.misc: Windows (geral)
        - comp.sys.ibm.pc.hardware: Hardware PC IBM-compatível
        - comp.sys.mac.hardware: Hardware Macintosh
        - comp.windows.x: Sistema X Window
        - misc.forsale: Anúncios de venda
        - rec.autos: Automóveis
        - rec.motorcycles: Motocicletas
        - rec.sport.baseball: Beisebol
        - rec.sport.hockey: Hóquei
        - sci.crypt: Criptografia
        - sci.electronics: Eletrônica
        - sci.med: Medicina
        - sci.space: Espaço/astronomia
        - soc.religion.christian: Cristianismo
        - talk.politics.guns: Política sobre armas
        - talk.politics.mideast: Política do Oriente Médio
        - talk.politics.misc: Política geral
        - talk.religion.misc: Religião geral
        
        **PASSO 3: HIPÓTESE COM EXCLUSÕES**
        Liste 2-3 categorias candidatas e explique por que você EXCLUI as outras:
        - Categoria candidata 1: [razão]
        - Categoria candidata 2: [razão]
        - Por que NÃO é [categoria similar]: [diferença chave]
        
        **PASSO 4: CONCLUSÃO FINAL**
        Após sua análise, forneça a classificação final no formato EXATO:
        
        Category: <nome_da_categoria>
        
        Onde <nome_da_categoria> é UMA das 20 categorias listadas acima, escrita EXATAMENTE como mostrado.
        """,
        agent=agent,
        expected_output="Análise completa em 4 passos (Entidades, Raciocínio, Hipótese, Conclusão) terminando com 'Category: <nome_da_categoria>' em linha separada."
    )


def create_enrichment_task(agent, classification_task):
    """
    Cria a Task 2: Enriquecimento com contexto web estruturado.
    
    Args:
        agent: Agente Pesquisador
        classification_task: Task de classificação (para usar como contexto)
    
    Returns:
        Task configurada
    """
    return Task(
        description="""
        Com base na classificação realizada na task anterior, realize uma pesquisa web estruturada:
        
        **PASSO 1: EXTRAÇÃO DA CATEGORIA**
        Identifique a categoria classificada no resultado da task anterior.
        
        **PASSO 2: PESQUISA WEB ESTRATÉGICA**
        Use a ferramenta Tavily para buscar informações sobre:
        - Evolução do tópico desde os anos 90 até hoje
        - Notícias recentes (últimos 2 anos) relacionadas
        - Tendências atuais e desenvolvimentos modernos
        - Contexto histórico e relevância contemporânea
        
        **PASSO 3: SÍNTESE**
        Organize as informações encontradas em:
        - **Contexto Histórico:** Como o tópico era visto nos anos 90
        - **Evolução:** Principais mudanças desde então
        - **Relevância Atual:** Por que o tópico ainda importa hoje
        - **Fontes:** Principais descobertas ou notícias encontradas
        
        Forneça um resumo estruturado e informativo que enriqueça a classificação.
        """,
        agent=agent,
        context=[classification_task],
        expected_output="Resumo estruturado do contexto web com histórico, evolução, relevância atual e fontes encontradas."
    )


def create_reporting_task(agent, classification_task, enrichment_task):
    """
    Cria a Task 3: Compilação do relatório executivo final.
    
    Args:
        agent: Agente Editor Chefe
        classification_task: Task de classificação
        enrichment_task: Task de enriquecimento
    
    Returns:
        Task configurada
    """
    return Task(
        description="""
        Compile um relatório executivo elegante e profissional em Markdown, escrito em português brasileiro (pt-BR).
        
        **ESTRUTURA DO RELATÓRIO:**
        
        # Relatório de Classificação e Enriquecimento
        
        ## 1. Resumo Executivo
        Um parágrafo conciso (3-4 linhas) resumindo a classificação e sua relevância.
        
        ## 2. Análise de Classificação
        - **Categoria Identificada:** [nome da categoria]
        - **Metodologia:** Resuma os 4 passos da análise CoT realizada
        - **Confiança:** Avalie a confiança na classificação (alta/média/baixa) e justifique
        
        ## 3. Contexto e Enriquecimento Web
        - **Evolução Histórica:** Como o tópico evoluiu desde os anos 90
        - **Relevância Contemporânea:** Por que o tópico ainda importa hoje
        - **Descobertas Principais:** Principais informações encontradas na pesquisa web
        
        ## 4. Conclusões
        - Síntese final
        - Implicações da classificação
        - Valor do enriquecimento contextual
        
        **REQUISITOS:**
        - Escrito totalmente em português brasileiro (pt-BR)
        - Formatação Markdown profissional e elegante
        - Linguagem clara, acessível mas técnica
        - Use títulos, listas e formatação para melhorar a legibilidade
        """,
        agent=agent,
        context=[classification_task, enrichment_task],
        expected_output="Relatório executivo completo em Markdown, em português brasileiro, com estrutura profissional e elegante."
    )

