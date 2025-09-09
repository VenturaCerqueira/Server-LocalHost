# servidor_app/controllers/api_controller.py
from flask import Blueprint, jsonify, current_app, request
from servidor_app.models.file_system_model import FileSystemModel
from servidor_app.services.server_info_service import get_server_info

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status')
def api_status():
    try:
        server_data = get_server_info(current_app.config['ROOT_DIR'])
        return jsonify(server_data)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter status do servidor: {e}")
        return jsonify({"error": "Erro interno ao obter status do servidor"}), 500

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
