from flask import Blueprint, jsonify, current_app, request
import subprocess
import os
from urllib.parse import urlparse

git_api_bp = Blueprint('git_api', __name__, url_prefix='/api')

@git_api_bp.route('/git_pull', methods=['POST'])
def git_pull():
    try:
        import subprocess
        # Execute git pull in the project directory
        result = subprocess.run(['git', 'pull'], cwd=current_app.root_path, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Git pull executado com sucesso", "output": result.stdout, "success": True}), 200
        else:
            return jsonify({"message": "Erro ao executar git pull", "output": result.stderr, "success": False}), 500
    except Exception as e:
        current_app.logger.error(f"Erro no git pull: {e}")
        return jsonify({"error": f"Erro interno no git pull: {str(e)}"}), 500

@git_api_bp.route('/git_pull_project', methods=['POST'])
def git_pull_project():
    try:
        import subprocess
        data = request.get_json()
        project_path = data.get('project_path')
        if not project_path:
            return jsonify({"error": "Caminho do projeto não fornecido"}), 400

        # Sanitize and construct absolute path
        base_dir = current_app.config.get('SISTEMAS_DIR', current_app.root_path)
        import os
        abs_path = os.path.abspath(os.path.join(base_dir, project_path))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"error": "Acesso negado ao caminho do projeto"}), 403

        # Execute git pull in the specified project directory
        result = subprocess.run(['git', 'pull'], cwd=abs_path, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": f"Git pull executado com sucesso em {project_path}", "output": result.stdout, "success": True}), 200
        else:
            return jsonify({"message": f"Erro ao executar git pull em {project_path}", "output": result.stderr, "success": False}), 500
    except Exception as e:
        current_app.logger.error(f"Erro no git pull do projeto: {e}")
        return jsonify({"error": f"Erro interno no git pull do projeto: {str(e)}"}), 500

@git_api_bp.route('/git_clone', methods=['POST'])
def git_clone():
    try:
        import subprocess
        import os
        from urllib.parse import urlparse
        data = request.get_json()
        repo_url = data.get('repo_url')
        if not repo_url:
            return jsonify({"error": "URL do repositório é obrigatória"}), 400

        # Extract repository name from URL
        parsed_url = urlparse(repo_url)
        repo_name = os.path.splitext(os.path.basename(parsed_url.path))[0]
        if not repo_name:
            return jsonify({"error": "Não foi possível extrair o nome do repositório da URL"}), 400

        # Construct absolute path using repo name
        base_dir = current_app.config.get('SISTEMAS_DIR', current_app.root_path)
        abs_path = os.path.abspath(os.path.join(base_dir, repo_name))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"error": "Acesso negado ao caminho de destino"}), 403

        # Ensure the base directory exists
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)

        # Execute git clone
        result = subprocess.run(['git', 'clone', repo_url, abs_path], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": f"Repositório clonado com sucesso em {repo_name}", "output": result.stdout, "success": True}), 200
        else:
            return jsonify({"message": f"Erro ao clonar repositório", "output": result.stderr, "success": False}), 500
    except Exception as e:
        current_app.logger.error(f"Erro no git clone: {e}")
        return jsonify({"error": f"Erro interno no git clone: {str(e)}"}), 500
