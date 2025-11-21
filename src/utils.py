"""
Utilitários para carregamento e pré-processamento de dados.
"""
import os
import re
import pandas as pd
from pathlib import Path
from sklearn.datasets import fetch_20newsgroups
import random


def fetch_newsgroups_samples(output_dir: str = "data/samples", num_samples: int = 5):
    """
    Baixa amostras aleatórias do dataset 20 Newsgroups e salva com ground truth no filename.
    
    Args:
        output_dir: Diretório onde salvar as amostras
        num_samples: Número de amostras aleatórias a baixar
    
    Returns:
        Lista de caminhos dos arquivos salvos
    """
    # Criar diretório se não existir
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Baixar dataset completo
    print("Baixando dataset 20 Newsgroups...")
    newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
    
    # Selecionar amostras aleatórias
    indices = random.sample(range(len(newsgroups.data)), min(num_samples, len(newsgroups.data)))
    
    saved_files = []
    for i, idx in enumerate(indices):
        text = newsgroups.data[idx]
        category = newsgroups.target_names[newsgroups.target[idx]]
        
        # Formato: categoria___sampleN.txt
        filename = f"{category}___{i+1}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        saved_files.append(filepath)
        print(f"Salvo: {filename}")
    
    return saved_files


def clean_text(text: str) -> str:
    """
    Pré-processamento básico de texto.
    
    Args:
        text: Texto bruto
    
    Returns:
        Texto limpo
    """
    if not text:
        return ""
    
    # Converter para lowercase
    text = text.lower()
    
    # Remover caracteres especiais excessivos (manter pontuação básica)
    text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', text)
    
    # Remover espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    
    # Remover espaços no início e fim
    text = text.strip()
    
    return text


def load_custom_csv(csv_path: str = "data/raw/Base_dados_textos_6_classes.csv") -> pd.DataFrame:
    """
    Carrega CSV customizado de 6 classes.
    
    Args:
        csv_path: Caminho para o arquivo CSV
    
    Returns:
        DataFrame com os dados ou DataFrame vazio se arquivo não existir
    """
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"CSV carregado com sucesso: {len(df)} registros")
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()


def extract_ground_truth_from_filename(filename: str) -> str:
    """
    Extrai a categoria (ground truth) do nome do arquivo.
    Formato esperado: categoria___sampleN.txt
    
    Args:
        filename: Nome do arquivo ou caminho completo
    
    Returns:
        Categoria extraída ou string vazia se não encontrar
    """
    # Extrair apenas o nome do arquivo se for caminho completo
    basename = os.path.basename(filename)
    
    # Procurar padrão: categoria___algo.txt
    match = re.match(r'^([^_]+(?:_[^_]+)*)___', basename)
    if match:
        return match.group(1)
    
    return ""


def get_text_from_file(filepath: str) -> str:
    """
    Lê conteúdo de um arquivo de texto.
    
    Args:
        filepath: Caminho para o arquivo
    
    Returns:
        Conteúdo do arquivo
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {filepath}: {e}")
        return ""

