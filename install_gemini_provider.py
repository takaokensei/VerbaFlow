"""
Script opcional para instalar o provider nativo do Gemini para CrewAI.
Execute este script se o fallback do Gemini não estiver funcionando.

Uso:
    python install_gemini_provider.py
"""
import subprocess
import sys

def install_gemini_provider():
    """Tenta instalar o provider nativo do Gemini para CrewAI"""
    print("🔧 Instalando provider nativo do Gemini para CrewAI...")
    print("=" * 60)
    
    try:
        # Tentar instalar com pip
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "crewai[google-genai]"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Provider nativo do Gemini instalado com sucesso!")
        print("\n📝 Saída da instalação:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao instalar provider nativo do Gemini")
        print("\n📝 Erro:")
        print(e.stderr)
        print("\n💡 Alternativas:")
        print("1. Aguarde o reset do rate limit do Groq (~12 minutos)")
        print("2. Use um modelo menor do Groq (llama-3.1-8b-instant)")
        print("3. Tente instalar manualmente: pip install 'crewai[google-genai]'")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = install_gemini_provider()
    sys.exit(0 if success else 1)

