from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from servidor_app.models.file_system_model import FileSystemModel
from servidor_app.services.server_info_service import get_server_info
import os

file_bp = Blueprint('file', __name__)

@file_bp.route('/')
@login_required
def index():
    # Use FileSystemModel to get directory listing with pagination
    from servidor_app.models.file_system_model import FileSystemModel

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
    try:
        pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('index.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@file_bp.route('/browse/<path:sub_path>')
@login_required
def browse(sub_path):
    # Use FileSystemModel to get directory listing with pagination
    from servidor_app.models.file_system_model import FileSystemModel

    current_path = sub_path
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
    try:
        pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('index.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@file_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    from servidor_app.models.file_system_model import FileSystemModel

    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado', 'success': False}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Nome de arquivo vazio', 'success': False}), 400

    current_path = request.form.get('current_path', '')
    # Determine root_dir based on current_path context
    if current_path.startswith('Licitações') or request.referrer and '/licitacoes' in request.referrer:
        root_dir = current_app.config['LICITACOES_DIR']
    else:
        root_dir = current_app.config['ROOT_DIR']

    fs_model = FileSystemModel(root_dir)

    try:
        filename = fs_model.save_file(file, current_path, current_user)
        # Determine redirect URL based on context
        if request.referrer and '/licitacoes' in request.referrer:
            redirect_url = url_for('main.licitacoes', path=current_path) if current_path else url_for('main.licitacoes')
        else:
            redirect_url = url_for('file.browse', sub_path=current_path) if current_path else url_for('file.index')
        return jsonify({
            'message': f'Arquivo {filename} enviado com sucesso',
            'success': True,
            'redirect_url': redirect_url
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao enviar arquivo: {str(e)}', 'success': False}), 500

@file_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    from servidor_app.models.file_system_model import FileSystemModel

    folder_name = request.form.get('folder_name')
    current_path = request.form.get('current_path', '')

    if not folder_name:
        return jsonify({'message': 'Nome da pasta é obrigatório', 'success': False}), 400

    # Determine root_dir based on current_path context
    if current_path.startswith('Licitações') or request.referrer and '/licitacoes' in request.referrer:
        root_dir = current_app.config['LICITACOES_DIR']
    else:
        root_dir = current_app.config['ROOT_DIR']

    fs_model = FileSystemModel(root_dir)

    try:
        fs_model.create_folder(folder_name, current_path, current_user)
        # Determine redirect URL based on context
        if request.referrer and '/licitacoes' in request.referrer:
            redirect_url = url_for('main.licitacoes', path=current_path) if current_path else url_for('main.licitacoes')
        else:
            redirect_url = url_for('file.browse', sub_path=current_path) if current_path else url_for('file.index')
        return jsonify({
            'message': f'Pasta {folder_name} criada com sucesso',
            'success': True,
            'redirect_url': redirect_url
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao criar pasta: {str(e)}', 'success': False}), 500

@file_bp.route('/move_item', methods=['POST'])
@login_required
def move_item():
    from servidor_app.models.file_system_model import FileSystemModel

    source_path = request.form.get('source_path')
    destination_path = request.form.get('destination_path')

    if not source_path or not destination_path:
        return jsonify({'message': 'Caminhos de origem e destino são obrigatórios', 'success': False}), 400

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    try:
        fs_model.move_item(source_path, destination_path, current_user)
        return jsonify({
            'message': 'Item movido com sucesso',
            'success': True,
            'redirect_url': url_for('file.index')
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao mover item: {str(e)}', 'success': False}), 500

@file_bp.route('/download/<path:file_path>')
@login_required
def download(file_path):
    from servidor_app.models.file_system_model import FileSystemModel
    import os
    from flask import send_from_directory, send_file, jsonify, current_app

    # Determine root directory based on path prefix
    if file_path.startswith('Licitações/'):
        root_dir = current_app.config['LICITACOES_DIR']
        relative_path = file_path[len('Licitações/'):]
    elif file_path.startswith('Sistemas/'):
        root_dir = current_app.config['SISTEMAS_DIR']
        relative_path = file_path[len('Sistemas/'):]
    elif file_path.startswith('Dropbox/'):
        root_dir = current_app.config['DROPBOX_DIR']
        relative_path = file_path[len('Dropbox/'):]

    else:
        root_dir = current_app.config['ROOT_DIR']
        relative_path = file_path

    fs_model = FileSystemModel(root_dir)
    full_path = os.path.join(root_dir, relative_path)

    # Log the request
    current_app.logger.info(f"Download requested: file_path={file_path}, relative_path={relative_path}, full_path={full_path}")

    # Security check
    if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir)):
        current_app.logger.warning(f"Security check failed for path: {full_path}")
        return jsonify({'message': 'Acesso negado', 'success': False}), 403

    if not os.path.exists(full_path):
        current_app.logger.warning(f"File not found: {full_path}")
        return jsonify({'message': 'Arquivo não encontrado', 'success': False}), 404

    if os.path.isdir(full_path):
        # If it's a directory, create a zip file
        memory_file, download_name = fs_model.create_zip_from_folder(relative_path)
        if memory_file:
            memory_file.seek(0)
            return send_file(
                memory_file,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/zip'
            )
        else:
            current_app.logger.error(f"Error creating zip for folder: {full_path}")
            return jsonify({'message': 'Erro ao criar arquivo zip', 'success': False}), 500
    else:
        # If it's a file, send it directly
        directory = os.path.dirname(full_path)
        return send_from_directory(directory, os.path.basename(full_path), as_attachment=True)
