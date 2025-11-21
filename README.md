# 🧠 VerbaFlow

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![CrewAI](https://img.shields.io/badge/AI-CrewAI-orange)
![Streamlit](https://img.shields.io/badge/frontend-Streamlit-red)
![License](https://img.shields.io/badge/license-MIT-green)

> **Sistema Multi-Agente para Classificação e Enriquecimento Contextual de Textos.**
> *Projeto Capstone desenvolvido para o Módulo 15 da Formação em Inteligência Artificial (DSA).*

---

## 📖 Sobre o Projeto

**VerbaFlow** é uma aplicação que demonstra a evolução do Processamento de Linguagem Natural (NLP) saindo de modelos estáticos para sistemas dinâmicos baseados em agentes.

Utilizando o paradigma **ReAct (Reason + Act)**, o sistema não apenas classifica uma notícia (como modelos tradicionais), mas "entende" o conteúdo, busca validação externa na web em tempo real e gera um relatório enriquecido.

### ✨ Diferenciais
* **Orquestração de Agentes:** 3 agentes especializados trabalhando em cadeia.
* **Enriquecimento Web:** Uso da API Tavily para buscar fatos atuais sobre textos antigos (anos 90).
* **Validação Automática:** Comparação em tempo real entre a *Predição do Agente* e o *Ground Truth* do dataset.
* **Interface Interativa:** UI amigável construída com Streamlit.

---

## 🏗️ Arquitetura do Sistema

O fluxo de trabalho segue um pipeline sequencial processado pelo framework **CrewAI**:

```mermaid
graph TD
    A[Usuário / Input] --> B(Agente 1: O Analista);
    B -->|Classificação & Tópico| C(Agente 2: O Pesquisador);
    C -->|Contexto Web & Fatos| D(Agente 3: O Editor Chefe);
    D -->|Relatório Final Markdown| E[Interface Streamlit];
    
    subgraph "Validação"
    B -.-> V{Comparar com Ground Truth};
    V -->|✅ ou ❌| E;
    end
````

### Os Agentes

1.  🕵️ **O Analista:** Especialista em NLP. Lê o texto bruto e determina a categoria exata (baseado no dataset 20 Newsgroups).
2.  🌐 **O Pesquisador:** Especialista em Fact-Checking. Usa o **Tavily** para buscar o contexto moderno do tópico identificado.
3.  ✍️ **O Editor Chefe:** Especialista em síntese. Compila a classificação técnica e a pesquisa web em um relatório executivo em Português.

-----

## 🚀 Tecnologias Utilizadas

  * **Core:** Python 3.12 (Versão estável para CrewAI/Pydantic)
  * **Orquestração:** CrewAI
  * **LLM Engine:** Groq (Modelo: `llama-3.3-70b-versatile`)
  * **Ferramentas (Tools):** Tavily Search API
  * **Interface:** Streamlit
  * **Dados:** Scikit-Learn (20 Newsgroups) & Pandas

-----

## 📁 Estrutura do Repositório

```bash
VerbaFlow/
├── data/
│   ├── samples/          # Cache de amostras do 20 Newsgroups (com Ground Truth no nome)
│   └── raw/              # Dataset customizado (CSV)
├── src/
│   ├── agents.py         # Definição dos Agentes (Brain)
│   ├── tasks.py          # Definição das Tarefas (Instructions)
│   ├── tools.py          # Configuração do Tavily
│   └── utils.py          # Carregamento e limpeza de dados
├── notebooks/
│   └── experimentacao_agentes.ipynb  # Sandbox para testes sem interface
├── docs/
│   └── GAMMA_SLIDES_PROMPT.md        # Prompt para geração de slides
├── app.py                # Aplicação Principal (Entry Point)
├── requirements.txt      # Dependências do projeto
└── .env.example          # Template de variáveis de ambiente
```

-----

## ⚡ Instalação e Execução

### Pré-requisitos

  * Python 3.12+
  * API Key do [Groq](https://groq.com/)
  * API Key do [Tavily](https://tavily.com/)
  * (Opcional) API Key do [Google Gemini](https://ai.google.dev/) para fallback automático

### Passo a Passo

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/takaokensei/VerbaFlow.git](https://github.com/takaokensei/VerbaFlow.git)
    cd VerbaFlow
    ```

2.  **Crie o ambiente virtual:**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Chaves de API:**
     
     **IMPORTANTE:** Crie um arquivo `.env` na raiz do projeto (copie do `.env.example`):
     
     ```bash
     # Windows (PowerShell)
     Copy-Item .env.example .env
     
     # Linux/Mac
     cp .env.example .env
     ```
     
     Depois, edite o arquivo `.env` e insira suas chaves reais:
     
     ```env
     GROQ_API_KEY=sua_chave_groq_aqui
     TAVILY_API_KEY=sua_chave_tavily_aqui
     GOOGLE_API_KEY=sua_chave_gemini_aqui  # Opcional: para fallback automático
     USE_GEMINI_FALLBACK=true              # Opcional: ativar fallback automático
     ```
     
     ⚠️ **Nota:** O arquivo `.env` está no `.gitignore` e não será commitado. O `.env.example` é apenas um template.

6.  **(Opcional) Instale o Provider Nativo do Gemini para Fallback:**
     
     Se você quiser usar o fallback automático para Gemini quando o Groq atingir o rate limit, instale o provider nativo:
     
     ```bash
     # Opção 1: Usando o script fornecido
     python install_gemini_provider.py
     
     # Opção 2: Instalação manual
     pip install 'crewai[google-genai]'
     ```
     
     ⚠️ **Nota:** O provider nativo do Gemini é opcional. Se não estiver instalado, o sistema ainda funcionará com Groq, mas o fallback automático para Gemini não estará disponível.

7.  **Execute a Aplicação:**

    ```bash
    streamlit run app.py
    ```

-----

## 📊 Dados e Validação

O sistema foi projetado para suportar duas fontes de dados para fins de demonstração acadêmica:

1.  **20 Newsgroups:** Dataset canônico de classificação de textos. O sistema extrai o *Ground Truth* do nome do arquivo (ex: `sci.space___sample1.txt`) e valida se o Agente Analista acertou a previsão.
2.  **CSV Customizado:** Suporte para carga de dados proprietários via arquivo `data/raw/Base_dados_textos_6_classes.csv`.

-----

## 👤 Autor

**Cauã Vitor F. Silva**

  * *Engenharia Elétrica - UFRN*
  * *Projeto desenvolvido para o Módulo 15 da Data Science Academy.*

-----

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.