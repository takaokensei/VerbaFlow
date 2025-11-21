# Prompt para Gamma AI - Apresentação VerbaFlow

## Instruções para Gamma AI

Crie uma apresentação profissional em português brasileiro sobre o projeto **VerbaFlow**, um sistema multi-agente para classificação e enriquecimento de textos usando CrewAI, Groq e Tavily.

---

## Título da Apresentação

**VerbaFlow: Sistema Multi-Agente para Classificação e Enriquecimento de Textos**

---

## Estrutura da Apresentação

### Slide 1: Capa
- Título: **VerbaFlow**
- Subtítulo: Sistema Multi-Agente para Classificação e Enriquecimento de Textos
- Projeto acadêmico - Módulo 15
- Paradigma ReAct (Reason + Act)

### Slide 2: Visão Geral do Projeto
- **Objetivo Principal**: Adaptar o conceito de "Travel Planner" para classificação e enriquecimento de textos
- **Problema**: Classificação de textos do dataset 20 Newsgroups e CSV customizado de 6 classes
- **Solução**: Sistema multi-agente com 3 agentes especializados trabalhando em sequência
- **Paradigma**: ReAct (Reasoning + Acting) aplicado à classificação de textos

### Slide 3: Stack Tecnológico
- **Python 3.12** (obrigatório para compatibilidade)
- **CrewAI**: Framework para sistemas multi-agente
- **Groq (Llama 3.1 70B)**: Modelo de linguagem para os agentes
- **Tavily**: Ferramenta de busca web para enriquecimento
- **Streamlit**: Interface web interativa
- **Scikit-Learn**: Dataset 20 Newsgroups
- **Pandas**: Processamento de dados CSV

### Slide 4: Arquitetura do Sistema
- **3 Agentes Especializados**:
  1. **O Analista**: Classificação NLP (20 categorias Newsgroups)
  2. **O Pesquisador**: Busca contexto moderno na web (Tavily)
  3. **O Editor Chefe**: Compilação de relatório em Markdown (pt-BR)
- **Fluxo Sequencial**: Task 1 → Task 2 → Task 3
- **Validação Automática**: Comparação Ground Truth vs Predicted

### Slide 5: Agente 1 - O Analista
- **Role**: Analista Sênior em Classificação de Textos
- **Responsabilidade**: Classificar textos em uma das 20 categorias Newsgroups
- **Output Formatado**: Deve conter "Category: <nome_da_categoria>" para parsing automático
- **Precisão**: Crítica para validação do sistema
- **Modelo**: Llama 3.1 70B Versatile via Groq

### Slide 6: Agente 2 - O Pesquisador
- **Role**: Pesquisador Especializado em Contexto Web
- **Ferramenta**: TavilySearchTool
- **Responsabilidade**: Buscar informações atualizadas sobre o tópico identificado
- **Objetivo**: Enriquecer a classificação com contexto moderno da web
- **Output**: Resumo de notícias recentes, tendências e contexto adicional

### Slide 7: Agente 3 - O Editor Chefe
- **Role**: Editor Chefe de Relatórios Técnicos
- **Responsabilidade**: Compilar classificação + contexto em relatório Markdown
- **Idioma**: Português brasileiro (pt-BR)
- **Estrutura**: 
  - Classificação realizada
  - Contexto web encontrado
  - Análise final e conclusões

### Slide 8: Pipeline de Processamento
1. **Carregamento**: Dataset 20 Newsgroups ou CSV customizado
2. **Pré-processamento**: Limpeza de texto (lowercase, remoção caracteres especiais)
3. **Task 1 - Classificação**: Analista classifica o texto
4. **Task 2 - Enriquecimento**: Pesquisador busca contexto web
5. **Task 3 - Relatório**: Editor compila relatório final
6. **Validação**: Comparação automática Ground Truth vs Predicted

### Slide 9: Interface Streamlit
- **Sidebar**: Configuração de API Keys (Groq e Tavily)
- **Seleção de Fonte**: 20 Newsgroups ou CSV customizado
- **Visualização**: Texto original + Ground Truth extraído do filename
- **Execução**: Botão "Executar VerbaFlow"
- **Validação Visual**: Indicador grande ✅ ou ❌
- **Relatório**: Exibição completa do relatório enriquecido

### Slide 10: Validação e Ground Truth
- **Formato de Arquivo**: `{categoria}___{numero}.txt`
- **Exemplo**: `rec.sport.hockey___sample1.txt`
- **Extração**: Parser regex para extrair categoria do filename
- **Comparação**: Case-insensitive entre Ground Truth e Predicted
- **Feedback Visual**: Indicadores claros de acerto/erro

### Slide 11: Estrutura do Projeto
```
VerbaFlow/
├── data/
│   ├── samples/          # Amostras 20 Newsgroups
│   └── raw/              # CSV customizado
├── src/
│   ├── agents.py         # Definições dos 3 agentes
│   ├── tasks.py          # 3 tasks sequenciais
│   ├── tools.py          # TavilySearchTool
│   └── utils.py          # Carregamento e pré-processamento
├── notebooks/
│   └── experimentacao_agentes.ipynb
├── app.py                # Interface Streamlit
└── docs/
    └── GAMMA_SLIDES_PROMPT.md
```

### Slide 12: Dataset 20 Newsgroups
- **20 Categorias**:
  - alt.atheism
  - comp.* (graphics, os.ms-windows.misc, sys.ibm.pc.hardware, sys.mac.hardware, windows.x)
  - misc.forsale
  - rec.* (autos, motorcycles, sport.baseball, sport.hockey)
  - sci.* (crypt, electronics, med, space)
  - soc.religion.christian
  - talk.* (politics.guns, politics.mideast, politics.misc, religion.misc)
- **Amostras**: 5 amostras aleatórias salvas com ground truth no filename

### Slide 13: Paradigma ReAct
- **Reasoning (Raciocínio)**: 
  - Analista analisa o texto e raciocina sobre a categoria
  - Pesquisador identifica termos-chave para busca
  - Editor sintetiza informações
- **Acting (Ação)**:
  - Analista produz classificação formatada
  - Pesquisador executa buscas na web
  - Editor gera relatório final
- **Iteração**: Cada agente usa o output do anterior

### Slide 14: Notebook de Experimentação
- **Objetivo**: Testar agentes sem interface Streamlit
- **Conteúdo**: 
  - Importação de módulos
  - Configuração de API Keys
  - Carregamento de dados
  - Criação de agentes e tasks
  - Execução do pipeline
  - Validação de resultados
- **Comentários**: Todos em português brasileiro

### Slide 15: Resultados e Validação
- **Métrica Principal**: Precisão da classificação (Ground Truth vs Predicted)
- **Output Formatado**: Regex parsing para extrair categoria
- **Feedback Imediato**: Indicadores visuais na interface
- **Relatório Enriquecido**: Classificação + contexto web + análise

### Slide 16: Casos de Uso
1. **Classificação de Textos**: Identificar categoria de documentos
2. **Enriquecimento Contextual**: Adicionar informações atualizadas
3. **Validação Automática**: Comparar predições com ground truth
4. **Geração de Relatórios**: Documentos técnicos em Markdown

### Slide 17: Diferenciais do Projeto
- ✅ Sistema multi-agente com especialização por função
- ✅ Validação automática com ground truth
- ✅ Enriquecimento com contexto web moderno
- ✅ Interface interativa Streamlit
- ✅ Suporte a múltiplas fontes de dados
- ✅ Relatórios profissionais em português

### Slide 18: Desafios e Soluções
- **Desafio 1**: Parsing preciso da categoria do output do Analista
  - **Solução**: Formato obrigatório "Category: <nome>" + regex
- **Desafio 2**: Integração sequencial de tasks
  - **Solução**: Context dependencies no CrewAI
- **Desafio 3**: Validação automática
  - **Solução**: Extração de ground truth do filename

### Slide 19: Próximos Passos
- Melhorar precisão da classificação
- Adicionar mais fontes de dados
- Implementar métricas de avaliação (accuracy, F1-score)
- Suporte a mais idiomas
- Dashboard de estatísticas

### Slide 20: Conclusão
- **VerbaFlow** demonstra o paradigma ReAct aplicado à classificação de textos
- Sistema multi-agente eficiente com 3 agentes especializados
- Validação automática e enriquecimento contextual
- Interface intuitiva e relatórios profissionais
- Projeto acadêmico completo para Módulo 15

### Slide 21: Agradecimentos e Referências
- CrewAI Framework
- Groq API (Llama 3.1 70B)
- Tavily Search API
- Streamlit
- Scikit-Learn (20 Newsgroups Dataset)

---

## Notas de Design para Gamma AI

- Use cores profissionais (azul, verde, branco)
- Inclua ícones relevantes para cada seção
- Mantenha consistência visual
- Use gráficos/diagramas para arquitetura e fluxo
- Destaque os 3 agentes visualmente
- Mostre exemplos de código quando relevante
- Use animações sutis para transições entre slides

---

## Palavras-chave para Busca de Imagens

- Multi-agent system
- Text classification
- NLP (Natural Language Processing)
- AI agents
- Machine learning pipeline
- Data processing workflow
- Web search integration
- Report generation

---

**Fim do Prompt**

