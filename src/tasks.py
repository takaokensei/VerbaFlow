"""
Definições das tasks do sistema VerbaFlow.
Usa Structured Output com Pydantic para garantir formato consistente.
"""
from crewai import Task
from src.models import ClassificationOutput, EnrichmentOutput, ReportOutput


def create_classification_task(agent, text: str, few_shot_examples: list = None):
    """
    Cria a Task 1: Classificação do texto com Chain of Thought e Structured Output.
    
    Args:
        agent: Agente Analista
        text: Texto a ser classificado
        few_shot_examples: Lista de exemplos para few-shot prompting (opcional)
    
    Returns:
        Task configurada com CoT e structured output
    """
    # Few-shot examples (se fornecidos)
    few_shot_section = ""
    if few_shot_examples:
        few_shot_section = "\n\n**EXEMPLOS DE CLASSIFICAÇÃO (Few-Shot Learning):**\n"
        for i, example in enumerate(few_shot_examples[:3], 1):  # Máximo 3 exemplos
            few_shot_section += f"""
**Exemplo {i}:**
Texto: "{example['text'][:200]}..."
Categoria Correta: {example['category']}
Raciocínio: {example.get('reasoning', 'Análise de entidades técnicas de hardware PC')}
---
"""
    
    return Task(
        description=f"""
        Analise o seguinte texto usando a metodologia Chain of Thought (CoT) e retorne um JSON estruturado.
        
        **TEXTO A CLASSIFICAR:**
        {text}
        
        {few_shot_section}
        
        **METODOLOGIA (4 PASSOS OBRIGATÓRIOS):**
        
        **PASSO 1: ANÁLISE DE ENTIDADES**
        Identifique e liste:
        - Organizações mencionadas (ex: IBM, Apple, Microsoft, NASA)
        - Termos técnicos específicos (ex: "encryption", "hardware", "software")
        - Domínios de conhecimento (ex: medicina, ciência espacial, criptografia)
        - Contexto temporal (anos 90 - tecnologia da época)
        
        **PASSO 2: RACIOCÍNIO CONTEXTUAL**
        Conecte as entidades identificadas às definições das 20 categorias Newsgroups:
        - alt.atheism, comp.graphics, comp.os.ms-windows.misc, comp.sys.ibm.pc.hardware,
        - comp.sys.mac.hardware, comp.windows.x, misc.forsale, rec.autos, rec.motorcycles,
        - rec.sport.baseball, rec.sport.hockey, sci.crypt, sci.electronics, sci.med,
        - sci.space, soc.religion.christian, talk.politics.guns, talk.politics.mideast,
        - talk.politics.misc, talk.religion.misc
        
        **PASSO 3: HIPÓTESE COM EXCLUSÕES**
        Liste 2-3 categorias candidatas e explique por que você EXCLUI as outras.
        
        **PASSO 4: CONCLUSÃO FINAL**
        Selecione a categoria final e avalie sua confiança (alta/média/baixa).
        
        **FORMATO DE SAÍDA (JSON ESTRUTURADO):**
        Você DEVE retornar um JSON válido seguindo este schema:
        {{
            "entity_analysis": {{
                "organizations": ["lista de organizações"],
                "technical_terms": ["lista de termos técnicos"],
                "knowledge_domains": ["lista de domínios"]
            }},
            "contextual_reasoning": "explicação do raciocínio contextual",
            "candidate_categories": ["cat1", "cat2", "cat3"],
            "exclusion_reasoning": "por que outras categorias foram excluídas",
            "final_category": "categoria_final_exata",
            "confidence": "alta|média|baixa",
            "reasoning_steps": [
                {{"step_number": 1, "step_name": "Análise", "reasoning": "..."}},
                {{"step_number": 2, "step_name": "Raciocínio", "reasoning": "..."}},
                {{"step_number": 3, "step_name": "Hipótese", "reasoning": "..."}},
                {{"step_number": 4, "step_name": "Conclusão", "reasoning": "..."}}
            ]
        }}
        
        IMPORTANTE: A "final_category" DEVE ser EXATAMENTE uma das 20 categorias listadas acima.
        """,
        agent=agent,
        expected_output="JSON estruturado com ClassificationOutput contendo entity_analysis, contextual_reasoning, candidate_categories, exclusion_reasoning, final_category, confidence e reasoning_steps."
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
    Cria a Task 3: Compilação do relatório executivo final com structured output.
    
    Args:
        agent: Agente Editor Chefe
        classification_task: Task de classificação
        enrichment_task: Task de enriquecimento
    
    Returns:
        Task configurada
    """
    return Task(
        description="""
        Compile um relatório executivo elegante e profissional, escrito em português brasileiro (pt-BR).
        
        Use os resultados das tasks anteriores (classificação e enriquecimento) para criar um relatório completo.
        
        **ESTRUTURA DO RELATÓRIO:**
        
        Retorne um JSON estruturado com:
        {{
            "executive_summary": "Resumo executivo conciso (3-4 linhas)",
            "classification_analysis": {{
                "category": "categoria identificada",
                "methodology": "resumo dos 4 passos CoT",
                "confidence": "alta/média/baixa",
                "justification": "justificativa da confiança"
            }},
            "web_context": {{
                "historical_evolution": "evolução desde os anos 90",
                "current_relevance": "relevância contemporânea",
                "key_findings": ["descoberta 1", "descoberta 2"]
            }},
            "conclusions": {{
                "summary": "síntese final",
                "implications": "implicações da classificação",
                "value": "valor do enriquecimento contextual"
            }},
            "full_report_markdown": "Relatório completo formatado em Markdown com todas as seções"
        }}
        
        O "full_report_markdown" deve incluir:
        # Relatório de Classificação e Enriquecimento
        ## 1. Resumo Executivo
        ## 2. Análise de Classificação
        ## 3. Contexto e Enriquecimento Web
        ## 4. Conclusões
        
        **REQUISITOS:**
        - Escrito totalmente em português brasileiro (pt-BR)
        - Formatação Markdown profissional e elegante
        - Linguagem clara, acessível mas técnica
        """,
        agent=agent,
        context=[classification_task, enrichment_task],
        expected_output="JSON estruturado com ReportOutput contendo executive_summary, classification_analysis, web_context, conclusions e full_report_markdown."
    )

