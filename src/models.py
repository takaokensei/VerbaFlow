"""
Modelos Pydantic para Structured Output do VerbaFlow.
Garante que o LLM sempre retorne dados no formato esperado.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class EntityAnalysis(BaseModel):
    """Análise de entidades encontradas no texto."""
    organizations: List[str] = Field(
        default_factory=list,
        description="Organizações mencionadas (ex: IBM, NASA, Microsoft)"
    )
    technical_terms: List[str] = Field(
        default_factory=list,
        description="Termos técnicos específicos identificados"
    )
    knowledge_domains: List[str] = Field(
        default_factory=list,
        description="Domínios de conhecimento (ex: medicina, criptografia, hardware)"
    )


class ReasoningStep(BaseModel):
    """Passo do raciocínio Chain of Thought."""
    step_number: int = Field(description="Número do passo (1-4)")
    step_name: str = Field(description="Nome do passo (Análise, Raciocínio, Hipótese, Conclusão)")
    reasoning: str = Field(description="Conteúdo do raciocínio para este passo")
    excluded_categories: Optional[List[str]] = Field(
        default=None,
        description="Categorias excluídas neste passo (se aplicável)"
    )


class ClassificationOutput(BaseModel):
    """
    Saída estruturada da classificação.
    Garante que o LLM sempre retorne dados no formato correto.
    """
    # Análise de entidades (Passo 1)
    entity_analysis: EntityAnalysis = Field(
        description="Análise de entidades, organizações e termos técnicos"
    )
    
    # Raciocínio contextual (Passo 2)
    contextual_reasoning: str = Field(
        description="Conexão das entidades às definições das 20 categorias Newsgroups"
    )
    
    # Hipótese com exclusões (Passo 3)
    candidate_categories: List[str] = Field(
        description="Lista de 2-3 categorias candidatas"
    )
    exclusion_reasoning: str = Field(
        description="Explicação de por que outras categorias foram excluídas"
    )
    
    # Conclusão final (Passo 4)
    final_category: str = Field(
        description="Categoria final selecionada (deve ser uma das 20 categorias Newsgroups)"
    )
    confidence: str = Field(
        description="Nível de confiança: 'alta', 'média' ou 'baixa'"
    )
    reasoning_steps: List[ReasoningStep] = Field(
        default_factory=list,
        description="Lista de passos do raciocínio Chain of Thought"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "entity_analysis": {
                    "organizations": ["IBM", "Microsoft"],
                    "technical_terms": ["hardware", "PC", "compatibility"],
                    "knowledge_domains": ["computação", "hardware"]
                },
                "contextual_reasoning": "O texto discute hardware de PC IBM-compatível...",
                "candidate_categories": [
                    "comp.sys.ibm.pc.hardware",
                    "comp.sys.mac.hardware"
                ],
                "exclusion_reasoning": "Não é Mac porque menciona IBM-compatível...",
                "final_category": "comp.sys.ibm.pc.hardware",
                "confidence": "alta",
                "reasoning_steps": []
            }
        }


class EnrichmentOutput(BaseModel):
    """Saída estruturada do enriquecimento web."""
    historical_context: str = Field(
        description="Como o tópico era visto nos anos 90"
    )
    evolution: str = Field(
        description="Principais mudanças desde então"
    )
    current_relevance: str = Field(
        description="Por que o tópico ainda importa hoje"
    )
    key_findings: List[str] = Field(
        default_factory=list,
        description="Principais descobertas ou notícias encontradas"
    )
    sources_summary: Optional[str] = Field(
        default=None,
        description="Resumo das fontes encontradas"
    )


class ReportOutput(BaseModel):
    """Saída estruturada do relatório final."""
    executive_summary: str = Field(
        description="Resumo executivo (3-4 linhas)"
    )
    classification_analysis: dict = Field(
        description="Análise detalhada da classificação"
    )
    web_context: dict = Field(
        description="Contexto web encontrado"
    )
    conclusions: dict = Field(
        description="Conclusões e implicações"
    )
    full_report_markdown: str = Field(
        description="Relatório completo formatado em Markdown"
    )

