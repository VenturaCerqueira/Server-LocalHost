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
            return jsonify({"message": "Git pull executado com sucesso", "output": result.stdout + result.stderr, "success": True}), 200
        else:
            return jsonify({"message": "Erro ao executar git pull", "output": result.stderr + result.stdout, "success": False}), 500
    except Exception as e:
        current_app.logger.error(f"Erro no git pull: {e}")
        return jsonify({"error": f"Erro interno no git pull: {str(e)}"}), 500

@git_api_bp.route('/git_pull_project', methods=['GET', 'POST'])
def git_pull_project():
    from flask import Response
    try:
        project_path = request.args.get('project_path')
        if not project_path:
            return jsonify({"error": "Caminho do projeto não fornecido"}), 400

        # Sanitize and construct absolute path
        base_dir = current_app.config.get('SISTEMAS_DIR', current_app.root_path)
        import os
        abs_path = os.path.abspath(os.path.join(base_dir, project_path))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"error": "Acesso negado ao caminho do projeto"}), 403

        def generate():
            import subprocess
            process = subprocess.Popen(['git', 'pull'], cwd=abs_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    yield f"data: {line.strip()}\n\n"
            process.stdout.close()
            process.wait()
            if process.returncode == 0:
                yield "data: SUCCESS\n\n"
            else:
                yield "data: ERROR\n\n"

        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        current_app.logger.error(f"Erro no git pull do projeto: {e}")
        return jsonify({"error": f"Erro interno no git pull do projeto: {str(e)}"}), 500

@git_api_bp.route('/git_status', methods=['GET'])
def git_status():
    from flask import Response
    try:
        project_path = request.args.get('project_path')
        if not project_path:
            return jsonify({"error": "Caminho do projeto não fornecido"}), 400

        # Sanitize and construct absolute path
        base_dir = current_app.config.get('SISTEMAS_DIR', current_app.root_path)
        import os
        abs_path = os.path.abspath(os.path.join(base_dir, project_path))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"error": "Acesso negado ao caminho do projeto"}), 403

        def generate():
            import subprocess
            process = subprocess.Popen(['git', 'status'], cwd=abs_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    yield f"data: {line.strip()}\n\n"
            process.stdout.close()
            process.wait()
            yield "data: END\n\n"

        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        current_app.logger.error(f"Erro no git status: {e}")
        return jsonify({"error": f"Erro interno no git status: {str(e)}"}), 500

@git_api_bp.route('/api/git_merge_abort', methods=['POST'])
def git_merge_abort():
    try:
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

        # Execute git merge --abort
        result = subprocess.run(['git', 'merge', '--abort'], cwd=abs_path, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Merge abortado com sucesso", "output": result.stdout + result.stderr, "success": True}), 200
        else:
            return jsonify({"message": "Erro ao abortar merge", "output": result.stderr + result.stdout, "success": False}), 500
    except Exception as e:
        current_app.logger.error(f"Erro no git merge --abort: {e}")
        return jsonify({"error": f"Erro interno no git merge --abort: {str(e)}"}), 500

@git_api_bp.route('/api/git_clone', methods=['GET', 'POST'])
def git_clone():
    from flask import Response
    try:
        if request.method == 'POST':
            repo_url = request.form.get('repo_url')
        else:
            repo_url = request.args.get('repo_url')
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

        def generate():
            import subprocess
            process = subprocess.Popen(['git', 'clone', repo_url, abs_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    yield f"data: {line.strip()}\n\n"
            process.stdout.close()
            process.wait()
            if process.returncode == 0:
                yield "data: SUCCESS\n\n"
            else:
                yield "data: ERROR\n\n"

        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        current_app.logger.error(f"Erro no git clone: {e}")
        return jsonify({"error": f"Erro interno no git clone: {str(e)}"}), 500
