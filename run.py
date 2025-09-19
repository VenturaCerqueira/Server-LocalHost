import os
from dotenv import load_dotenv
from pyngrok import ngrok, conf
from servidor_app import create_app
import logging
import webbrowser
import threading
import time
import socket

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
            auth=basic_auth,
            options={
                "request_timeout": 300,  # 5 minutes timeout
                "response_timeout": 300,  # 5 minutes timeout
            }
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

def open_browser(url):
    """Abre o navegador padrão após um pequeno delay para garantir que o servidor esteja rodando."""
    time.sleep(2)
    webbrowser.open(url)

def get_local_ip():
    """Obtém o endereço IP local da máquina."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    port = 5000
    debug_mode = True

    # Obtém o IP local para acesso na rede
    local_ip = get_local_ip()
    network_url = f"http://{local_ip}:{port}"

    # Inicia o túnel ngrok
    public_url = start_ngrok(port)

    if public_url:
        print(f" * A aplicação Flask será acessível publicamente através de: {public_url}")
        print(f" * A aplicação também estará acessível na rede local em: {network_url}")
        # Abre o navegador no URL público em uma thread separada
        threading.Thread(target=open_browser, args=(public_url,)).start()
    else:
        print(" * Não foi possível iniciar o túnel ngrok. A aplicação rodará apenas localmente.")
        print(f" * A aplicação estará acessível localmente em: http://127.0.0.1:{port}")
        print(f" * A aplicação estará acessível na rede local em: {network_url}")
        threading.Thread(target=open_browser, args=(network_url,)).start()

    try:
        app = create_app()
        # Use `use_reloader=False` para evitar que o ngrok seja reiniciado
        # Run on 0.0.0.0 to allow access from network
        app.run(host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False)

    except Exception as e:
        print(f"Erro ao rodar a aplicação Flask: {e}")
    finally:
        # Garante que o túnel ngrok seja fechado ao encerrar a aplicação
        print("\nDesconectando túneis do ngrok...")
        try:
            ngrok.kill()
        except Exception as e:
            print(f"Erro ao desconectar túneis do ngrok: {e}")
