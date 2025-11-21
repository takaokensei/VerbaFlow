"""
Aplicação Streamlit principal do VerbaFlow.
"""
import os
import re
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from crewai import Crew, Process

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
from src.utils import (
    fetch_newsgroups_samples,
    clean_text,
    load_custom_csv,
    extract_ground_truth_from_filename,
    get_text_from_file
)
from src.agents import (
    get_llm,
    create_analyst_agent,
    create_researcher_agent,
    create_editor_agent
)
from src.tasks import (
    create_classification_task,
    create_enrichment_task,
    create_reporting_task
)


# Configuração da página
st.set_page_config(
    page_title="VerbaFlow - Classificação e Enriquecimento de Textos",
    page_icon="📝",
    layout="wide"
)

# Título principal
st.title("📝 VerbaFlow")
st.markdown("### Sistema Multi-Agente para Classificação e Enriquecimento de Textos")
st.markdown("---")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Chave de API do Groq para o modelo Llama 3.1 70B"
    )
    
    tavily_key = st.text_input(
        "Tavily API Key",
        type="password",
        help="Chave de API do Tavily para busca web"
    )
    
    # Salvar API keys nas variáveis de ambiente
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
    
    st.markdown("---")
    st.markdown("### 📊 Fonte de Dados")
    
    data_source = st.radio(
        "Selecione a fonte de dados:",
        ["20 Newsgroups (Amostras)", "CSV Customizado (6 Classes)"],
        index=0
    )


# Área principal
if not groq_key:
    st.warning("⚠️ Por favor, configure a Groq API Key na barra lateral para continuar.")
    st.stop()

# Seleção de dados
if data_source == "20 Newsgroups (Amostras)":
    st.subheader("📰 Dataset 20 Newsgroups")
    
    if st.button("🔄 Carregar Amostras Aleatórias"):
        with st.spinner("Baixando amostras do dataset 20 Newsgroups..."):
            try:
                samples = fetch_newsgroups_samples(num_samples=5)
                st.session_state['samples'] = samples
                st.success(f"✅ {len(samples)} amostras carregadas com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar amostras: {e}")
    
    if 'samples' in st.session_state and st.session_state['samples']:
        sample_files = st.session_state['samples']
        selected_file = st.selectbox(
            "Selecione uma amostra:",
            options=sample_files,
            format_func=lambda x: os.path.basename(x)
        )
        
        if selected_file:
            # Carregar texto
            raw_text = get_text_from_file(selected_file)
            ground_truth = extract_ground_truth_from_filename(selected_file)
            
            # Exibir texto e ground truth
            st.markdown("### 📄 Texto Original")
            st.text_area("", raw_text, height=200, disabled=True, key="raw_text_display")
            
            st.markdown(f"### 🏷️ Categoria Real (Ground Truth)")
            st.info(f"**{ground_truth}**")
            
            # Executar VerbaFlow
            if st.button("🚀 Executar VerbaFlow", type="primary"):
                if not tavily_key:
                    st.warning("⚠️ Tavily API Key é necessária para enriquecimento completo.")
                
                with st.spinner("🔄 Processando com agentes CrewAI..."):
                    try:
                        # Limpar texto
                        cleaned_text = clean_text(raw_text)
                        
                        # Configurar variáveis de ambiente para forçar uso do Groq
                        # O CrewAI precisa que OPENAI_API_KEY não esteja definida ou seja inválida
                        # para usar LLM customizado
                        if "OPENAI_API_KEY" in os.environ:
                            # Salvar temporariamente e remover
                            original_openai_key = os.environ.pop("OPENAI_API_KEY", None)
                        
                        # Criar LLM Groq
                        llm = get_llm()
                        
                        # Criar agentes com LLM explicitamente configurado
                        analyst = create_analyst_agent(llm)
                        researcher = create_researcher_agent(llm)
                        editor = create_editor_agent(llm)
                        
                        # Criar tasks
                        task1 = create_classification_task(analyst, cleaned_text)
                        task2 = create_enrichment_task(researcher, task1)
                        task3 = create_reporting_task(editor, task1, task2)
                        
                        # Criar crew - cada agente já tem seu LLM Groq configurado
                        crew = Crew(
                            agents=[analyst, researcher, editor],
                            tasks=[task1, task2, task3],
                            process=Process.sequential,
                            verbose=True
                        )
                        
                        # Executar
                        result = crew.kickoff()
                        
                        # Extrair categoria prevista
                        predicted_category = ""
                        category_match = re.search(r'Category:\s*([^\n]+)', str(result), re.IGNORECASE)
                        if category_match:
                            predicted_category = category_match.group(1).strip()
                        
                        # Validação
                        st.markdown("---")
                        st.markdown("### ✅ Resultado da Validação")
                        
                        # Comparar categorias (case-insensitive)
                        is_correct = predicted_category.lower() == ground_truth.lower()
                        
                        if is_correct:
                            st.success("## ✅ Classificação Correta!")
                            st.balloons()
                        else:
                            st.error("## ❌ Classificação Incorreta")
                        
                        # Exibir comparação
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Categoria Real", ground_truth)
                        with col2:
                            st.metric("Categoria Prevista", predicted_category if predicted_category else "Não encontrada")
                        
                        # Exibir relatório completo
                        st.markdown("---")
                        st.markdown("### 📋 Relatório Enriquecido Completo")
                        st.markdown(str(result))
                        
                        # Salvar resultado na sessão
                        st.session_state['last_result'] = {
                            'ground_truth': ground_truth,
                            'predicted': predicted_category,
                            'is_correct': is_correct,
                            'report': str(result)
                        }
                        
                    except Exception as e:
                        st.error(f"❌ Erro durante execução: {e}")
                        st.exception(e)

else:  # CSV Customizado
    st.subheader("📊 CSV Customizado (6 Classes)")
    
    csv_path = "data/raw/Base_dados_textos_6_classes.csv"
    
    if not os.path.exists(csv_path):
        st.warning(f"⚠️ Arquivo CSV não encontrado em: {csv_path}")
        st.info("Por favor, coloque o arquivo 'Base_dados_textos_6_classes.csv' na pasta data/raw/")
    else:
        df = load_custom_csv(csv_path)
        
        if not df.empty:
            # Assumir que o CSV tem colunas 'texto' e 'categoria' (ou similar)
            # Tentar detectar automaticamente
            text_col = None
            category_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'text' in col_lower or 'texto' in col_lower:
                    text_col = col
                if 'categor' in col_lower or 'class' in col_lower or 'label' in col_lower:
                    category_col = col
            
            if text_col and category_col:
                st.dataframe(df.head(), use_container_width=True)
                
                selected_idx = st.selectbox(
                    "Selecione um registro:",
                    options=range(len(df)),
                    format_func=lambda x: f"Registro {x+1}: {df.iloc[x][category_col]}"
                )
                
                if selected_idx is not None:
                    raw_text = str(df.iloc[selected_idx][text_col])
                    ground_truth = str(df.iloc[selected_idx][category_col])
                    
                    st.markdown("### 📄 Texto Original")
                    st.text_area("", raw_text, height=200, disabled=True)
                    
                    st.markdown(f"### 🏷️ Categoria Real (Ground Truth)")
                    st.info(f"**{ground_truth}**")
                    
                    if st.button("🚀 Executar VerbaFlow", type="primary"):
                        # Similar ao fluxo acima, mas adaptado para CSV
                        st.info("Funcionalidade para CSV customizado - implementação similar ao 20 Newsgroups")
            else:
                st.error("❌ Não foi possível detectar automaticamente as colunas 'texto' e 'categoria' no CSV.")
                st.info("Colunas encontradas: " + ", ".join(df.columns.tolist()))
        else:
            st.error("❌ Erro ao carregar CSV ou arquivo vazio.")

