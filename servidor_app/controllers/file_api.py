from flask import Blueprint, jsonify, current_app, send_file
from servidor_app.models.file_system_model import FileSystemModel
import os

file_api_bp = Blueprint('file_api', __name__, url_prefix='/api')

@file_api_bp.route('/folder_info/<path:folder_path>')
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

@file_api_bp.route('/download_folder/<path:folder_path>')
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
