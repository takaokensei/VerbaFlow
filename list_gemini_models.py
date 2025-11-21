"""
Script para listar modelos disponíveis da API do Google Gemini.
Execute este script para descobrir quais modelos estão disponíveis e seus formatos corretos.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Tentar importar a biblioteca do Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    # Tentar instalar ou usar alternativa
    try:
        from google import generativeai as genai
        GEMINI_AVAILABLE = True
    except ImportError:
        print("ERRO: google-generativeai nao esta instalado.")
        print("Instalando...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        import google.generativeai as genai
        GEMINI_AVAILABLE = True

# Obter a chave da API
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERRO: GOOGLE_API_KEY ou GEMINI_API_KEY nao encontrada nas variaveis de ambiente")
    print("Configure no arquivo .env ou como variavel de ambiente")
    exit(1)

# Configurar a API
genai.configure(api_key=api_key)

print("Listando modelos disponiveis da API do Google Gemini...")
print("=" * 60)

try:
    # Listar todos os modelos disponíveis
    models = genai.list_models()
    models_list = list(models)
    
    print(f"\nEncontrados {len(models_list)} modelos disponiveis:\n")
    
    # Filtrar apenas modelos que suportam generateContent
    generate_content_models = []
    for model in models_list:
        if 'generateContent' in model.supported_generation_methods:
            generate_content_models.append(model)
            print(f"Nome: {model.name}")
            print(f"   Display Name: {model.display_name}")
            if hasattr(model, 'description') and model.description:
                print(f"   Descricao: {model.description}")
            print(f"   Metodos suportados: {', '.join(model.supported_generation_methods)}")
            if hasattr(model, 'version'):
                print(f"   Versao: {model.version}")
            print()
    
    print("=" * 60)
    print(f"\nTotal de modelos que suportam generateContent: {len(generate_content_models)}")
    
    # Mostrar apenas os nomes dos modelos para uso no código
    print("\nModelos recomendados para uso (apenas o nome do modelo):")
    for model in generate_content_models:
        # Extrair apenas o nome do modelo (sem o prefixo "models/")
        model_name = model.name.replace("models/", "")
        print(f"   - {model_name}")
    
    # Verificar especificamente gemini-1.5-pro e gemini-1.5-flash
    print("\nVerificando modelos especificos:")
    specific_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro-latest"]
    for model_name in specific_models:
        found = False
        for model in generate_content_models:
            if model_name in model.name:
                print(f"   OK {model_name} encontrado como: {model.name}")
                found = True
                break
        if not found:
            print(f"   NAO {model_name} NAO encontrado")
    
except Exception as e:
    print(f"ERRO ao listar modelos: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

