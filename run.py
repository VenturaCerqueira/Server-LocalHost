# run.py
import os
from dotenv import load_dotenv
from pyngrok import ngrok, conf
from servidor_app import create_app
import logging

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura um logger para o pyngrok para ver mais detalhes se necessário
# logging.basicConfig(level=logging.DEBUG)

def start_ngrok(port):
    """Inicia um túnel ngrok seguro com autenticação e maior tolerância."""
    authtoken = os.environ.get("NGROK_AUTHTOKEN")
    basic_auth = os.environ.get("NGROK_BASIC_AUTH")

    if not basic_auth:
        print("AVISO: A variável de ambiente NGROK_BASIC_AUTH não foi definida. O túnel será público.")

    try:
        if authtoken:
            ngrok.set_auth_token(authtoken)

        print("Iniciando túnel ngrok com timeout estendido...")

        public_url = ngrok.connect(
            port,
            "http",
            auth=basic_auth
        ).public_url

        print(f" * Túnel Ngrok seguro rodando em: {public_url}")
        if basic_auth and ':' in basic_auth:
            print(f" * Usuário/Senha para acesso: {basic_auth.split(':')[0]} / {'*' * len(basic_auth.split(':')[1])}")
        else:
            print(" * Usuário/Senha para acesso: Não configurado corretamente")

        return public_url

    except Exception as e:
        print(f"Erro ao iniciar o ngrok: {e}")
        print(" * A aplicação será executada apenas localmente.")
        # Não tenta desconectar túneis se o ngrok falhou ao iniciar
        return None

if __name__ == '__main__':
    port = 5000
    debug_mode = True 

    # Inicia o túnel ngrok
    public_url = start_ngrok(port)
    
    if public_url:
        print(f" * A aplicação Flask será acessível publicamente através de: {public_url}")
    else:
        print(" * Não foi possível iniciar o túnel ngrok. A aplicação rodará apenas localmente.")

    try:
        app = create_app()
        # Use `use_reloader=False` para evitar que o ngrok seja reiniciado
        app.run(port=port, debug=debug_mode, use_reloader=False)

    except Exception as e:
        print(f"Erro ao rodar a aplicação Flask: {e}")
    finally:
        # Garante que o túnel ngrok seja fechado ao encerrar a aplicação
        print("\nDesconectando túneis do ngrok...")
        try:
            ngrok.kill()
        except Exception as e:
            print(f"Erro ao desconectar túneis do ngrok: {e}")
