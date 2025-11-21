# VerbaFlow
<<<<<<< HEAD

Sistema Multi-Agente usando CrewAI, Groq e Tavily para Classificação e Enriquecimento de Textos. Projeto Capstone para Módulo 15 DSA.

## 📋 Descrição

VerbaFlow é um sistema multi-agente que demonstra o paradigma **ReAct (Reason + Act)** aplicado à classificação de textos. O sistema utiliza três agentes especializados trabalhando em sequência para classificar textos do dataset 20 Newsgroups e enriquecê-los com contexto web moderno.

## 🏗️ Arquitetura

O sistema é composto por **3 agentes especializados**:

1. **O Analista** - Especialista em classificação NLP (20 categorias Newsgroups)
2. **O Pesquisador** - Busca contexto moderno na web usando Tavily
3. **O Editor Chefe** - Compila relatório final em Markdown (pt-BR)

## 🚀 Tecnologias

- **Python 3.12** (obrigatório para compatibilidade CrewAI/Pydantic)
- **CrewAI** - Framework para sistemas multi-agente
- **Groq (Llama 3.1 70B)** - Modelo de linguagem
- **Tavily** - Busca web para enriquecimento
- **Streamlit** - Interface web interativa
- **Scikit-Learn** - Dataset 20 Newsgroups
- **Pandas** - Processamento de dados CSV

## 📁 Estrutura do Projeto

```
VerbaFlow/
├── data/
│   ├── samples/          # Amostras do 20 Newsgroups
│   └── raw/              # CSV customizado (6 classes)
├── src/
│   ├── agents.py         # Definições dos 3 agentes
│   ├── tasks.py          # 3 tasks sequenciais
│   ├── tools.py          # TavilySearchTool
│   └── utils.py          # Carregamento e pré-processamento
├── notebooks/
│   └── experimentacao_agentes.ipynb
├── docs/
│   └── GAMMA_SLIDES_PROMPT.md
├── app.py                # Interface Streamlit
├── requirements.txt
└── .env.example
```

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd VerbaFlow
```

2. Crie um ambiente virtual (Python 3.12):
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as API Keys:
```bash
cp .env.example .env
# Edite .env e adicione suas chaves:
# - GROQ_API_KEY
# - TAVILY_API_KEY
```

## 🎯 Uso

### Interface Streamlit

Execute a aplicação web:
```bash
streamlit run app.py
```

A interface permite:
- Configurar API Keys (Groq e Tavily)
- Selecionar fonte de dados (20 Newsgroups ou CSV customizado)
- Visualizar texto original e ground truth
- Executar classificação e enriquecimento
- Validar resultados automaticamente

### Notebook Jupyter

Para experimentação sem interface:
```bash
jupyter notebook notebooks/experimentacao_agentes.ipynb
```

## 📊 Dataset

O sistema suporta duas fontes de dados:

1. **20 Newsgroups**: Dataset clássico com 20 categorias de textos
2. **CSV Customizado**: Arquivo `Base_dados_textos_6_classes.csv` na pasta `data/raw/`

## ✅ Validação

O sistema valida automaticamente as classificações comparando:
- **Ground Truth**: Extraído do nome do arquivo (formato: `categoria___sampleN.txt`)
- **Predicted**: Extraído do output do Analista (formato: `Category: <nome>`)

## 📝 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Projeto desenvolvido para Módulo 15 DSA.
=======
Multi-Agent System using CrewAI, Groq, and Tavily for Text Classification &amp; Enrichment. Capstone Project for DSA Module 15.
>>>>>>> 0dca2f1246f2fdba8060d848684b0258c919222b
