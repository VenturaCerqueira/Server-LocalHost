from flask import Blueprint, jsonify, current_app
import servidor_app.services.database_service as db_service

sync_api_bp = Blueprint('sync_api', __name__, url_prefix='/api')

@sync_api_bp.route('/sync_db/<db_name>', methods=['POST'])
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
