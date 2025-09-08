# servidor_app/controllers/api_controller.py
from flask import Blueprint, jsonify, current_app, request, send_file
from servidor_app.models.file_system_model import FileSystemModel
from servidor_app.services.server_info_service import get_server_info
import servidor_app.services.database_service as db_service
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status')
def api_status():
    try:
        server_data = get_server_info(current_app.config['ROOT_DIR'])
        return jsonify(server_data)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter status do servidor: {e}")
        return jsonify({"error": "Erro interno ao obter status do servidor"}), 500

@api_bp.route('/folder_info/<path:folder_path>')
def api_folder_info(folder_path):
    try:
        fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
        full_path = os.path.join(fs_model.root_dir, folder_path)

        if not os.path.abspath(full_path).startswith(os.path.abspath(fs_model.root_dir)):
            return jsonify({"error": "Acesso negado"}), 403

        if os.path.isdir(full_path):
            size_formatted = fs_model.get_folder_size(full_path)
            if "N/A" in size_formatted:
                return jsonify({"size": "N/A"}), 500
            return jsonify({"size": size_formatted})

        return jsonify({"error": "Não é uma pasta"}), 400
    except Exception as e:
        current_app.logger.error(f"Erro ao obter informações da pasta {folder_path}: {e}")
        return jsonify({"error": "Erro interno ao obter informações da pasta"}), 500

@api_bp.route('/search')
def search():
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        current_app.logger.info(f"Search request received: query='{query}', page={page}, per_page={per_page}")
        fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
        results, pagination = fs_model.search(query, page=page, per_page=per_page)
        current_app.logger.info(f"Search returned {len(results)} results")
        return jsonify({
            'results': results,
            'pagination': pagination
        })
    except Exception as e:
        current_app.logger.error(f"Erro na busca por '{query}': {e}")
        return jsonify({"error": "Erro interno na busca"}), 500

@api_bp.route('/sync_db/<db_name>', methods=['POST'])
def sync_db(db_name):
    try:
        result = db_service.sync_mysql_production_to_local(db_name, current_app.config)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        current_app.logger.error(f"Erro na sincronização do banco {db_name}: {e}")
        return jsonify({"error": f"Erro interno na sincronização: {str(e)}"}), 500

@api_bp.route('/git_pull', methods=['POST'])
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

@api_bp.route('/git_pull_project', methods=['POST'])
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

@api_bp.route('/git_clone', methods=['POST'])
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

@api_bp.route('/download_folder/<path:folder_path>')
def download_folder(folder_path):
    try:
        import zipfile
        import io
        base_dir = current_app.config.get('SISTEMAS_DIR', current_app.root_path)
        abs_path = os.path.abspath(os.path.join(base_dir, folder_path))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            return jsonify({"error": "Acesso negado"}), 403

        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            return jsonify({"error": "Pasta não encontrada"}), 404

        # Create zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(abs_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, abs_path)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)
        folder_name = os.path.basename(abs_path)
        return send_file(zip_buffer, as_attachment=True, download_name=f"{folder_name}.zip", mimetype='application/zip')
    except Exception as e:
        current_app.logger.error(f"Erro no download da pasta {folder_path}: {e}")
        return jsonify({"error": f"Erro interno no download: {str(e)}"}), 500
