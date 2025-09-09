from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from servidor_app.models.user_model import User
from servidor_app.services.server_info_service import get_server_info
import servidor_app.services.database_service as db_service
from servidor_app.services.metrics_service import metrics_service
from servidor_app.services.optimization_service import performance_optimizer
from servidor_app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
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

@main_bp.route('/browse/<path:sub_path>')
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

@main_bp.route('/databases')
@login_required
def databases():
    # Database management page with MySQL databases from XAMPP
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    mysql_dbs = db_service.list_local_mysql_databases(current_app.config)
    return render_template('databases.html', dados_servidor=dados_servidor, mysql_dbs=mysql_dbs)

@main_bp.route('/sistemas')
@login_required
def sistemas():
    # Systems management page pointing to XAMPP htdocs
    from servidor_app.models.file_system_model import FileSystemModel
    import os

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['SISTEMAS_DIR']
    fs_model = FileSystemModel(root_dir)
    try:
        full_path = os.path.join(root_dir, current_path)
        if not os.path.exists(full_path):
            flash(f"Diretório não encontrado: {full_path}", "danger")
            pastas = []
            pagination = None
            parent_path = None
        else:
            pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('sistemas.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/licitacoes')
@login_required
def licitacoes():
    # Licitações management page pointing to D:\Servidor\Licitações
    from servidor_app.models.file_system_model import FileSystemModel
    import os

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['LICITACOES_DIR']
    fs_model = FileSystemModel(root_dir)
    try:
        full_path = os.path.join(root_dir, current_path)
        if not os.path.exists(full_path):
            flash(f"Diretório não encontrado: {full_path}", "danger")
            pastas = []
            pagination = None
            parent_path = None
        else:
            pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('licitacoes.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/dropbox')
@login_required
def dropbox():
    # Dropbox management page pointing to network path
    from servidor_app.models.file_system_model import FileSystemModel
    import os
    import logging

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['DROPBOX_DIR']
    error_message = None

    # Check if root directory exists before initializing FileSystemModel
    if not os.path.exists(root_dir):
        error_message = f"Diretório Dropbox não encontrado ou inacessível: {root_dir}"
        pastas = []
        pagination = None
        parent_path = None
    else:
        try:
            fs_model = FileSystemModel(root_dir)
            full_path = os.path.join(root_dir, current_path)
            if not os.path.exists(full_path):
                error_message = f"Diretório não encontrado: {full_path}"
                pastas = []
                pagination = None
                parent_path = None
            else:
                pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
                # Log debug info
                logging.debug(f"Dropbox list_directory called with current_path={current_path}, page={page}, per_page={per_page}")
                if pagination:
                    logging.debug(f"Pagination info: total_items={pagination.get('total_items')}, total_pages={pagination.get('total_pages')}")
        except Exception as e:
            error_message = f"Erro ao listar diretório: {e}"
            pastas = []
            pagination = None
            parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('dropbox.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor, error_message=error_message)

@main_bp.route('/metrics')
@login_required
def metrics():
    # Metrics monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    system_resources = performance_optimizer.get_system_resources()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('metrics.html', dados_servidor=dados_servidor, system_resources=system_resources, metrics_summary=metrics_summary)

@main_bp.route('/performance')
@login_required
def performance():
    # Performance monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    performance_stats = performance_optimizer.get_performance_stats()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('performance.html', dados_servidor=dados_servidor, performance_stats=performance_stats, metrics_summary=metrics_summary)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email:
            flash('Email é obrigatório.', 'danger')
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash('A senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('main.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso. Faça login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/perfil')
@login_required
def perfil():
    # Show logged-in user info
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('perfil.html', user=current_user, dados_servidor=dados_servidor)

@main_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    if request.method == 'POST':
        new_username = request.form.get('username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify current password
        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'danger')
            return redirect(url_for('main.configuracoes'))

        # Check new password confirmation
        if new_password != confirm_password:
            flash('A nova senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('main.configuracoes'))

        # Update username and password
        if new_username:
            current_user.username = new_username
        if new_password:
            current_user.set_password(new_password)

        db.session.commit()
        flash('Configurações atualizadas com sucesso.', 'success')
        return redirect(url_for('main.perfil'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('configuracoes.html', user=current_user, dados_servidor=dados_servidor)

@main_bp.route('/admin')
@login_required
def admin():
    # Only allow user 'keep' to access admin area
    if current_user.username != 'keep':
        flash('Acesso negado. Você não tem permissão para acessar esta área.', 'danger')
        return redirect(url_for('main.index'))

    # Get all users for admin dashboard
    users = User.query.all()
    # Remove dados_servidor here to avoid conflict with global context processor
    return render_template('admin.html', users=users)

@main_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    # Only allow user 'keep' to delete users
    if current_user.username != 'keep':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    # Don't allow deleting self
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('main.admin'))

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    flash(f'Usuário {user.username} foi excluído com sucesso.', 'success')
    return redirect(url_for('main.admin'))

@main_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user(user_id):
    # Only allow user 'keep' to block/unblock users
    if current_user.username != 'keep':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    # Don't allow blocking self
    if user.id == current_user.id:
        flash('Você não pode bloquear sua própria conta.', 'danger')
        return redirect(url_for('main.admin'))

    # Toggle active status
    user.is_active = not user.is_active
    db.session.commit()

    status = 'desbloqueado' if user.is_active else 'bloqueado'
    flash(f'Usuário {user.username} foi {status} com sucesso.', 'success')
    return redirect(url_for('main.admin'))

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    from servidor_app.models.file_system_model import FileSystemModel

    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado', 'success': False}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Nome de arquivo vazio', 'success': False}), 400

    current_path = request.form.get('current_path', '')
    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    try:
        filename = fs_model.save_file(file, current_path, current_user)
        return jsonify({
            'message': f'Arquivo {filename} enviado com sucesso',
            'success': True,
            'redirect_url': url_for('main.browse', sub_path=current_path) if current_path else url_for('main.index')
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao enviar arquivo: {str(e)}', 'success': False}), 500

@main_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    from servidor_app.models.file_system_model import FileSystemModel

    folder_name = request.form.get('folder_name')
    current_path = request.form.get('current_path', '')

    if not folder_name:
        return jsonify({'message': 'Nome da pasta é obrigatório', 'success': False}), 400

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    try:
        fs_model.create_folder(folder_name, current_path, current_user)
        return jsonify({
            'message': f'Pasta {folder_name} criada com sucesso',
            'success': True,
            'redirect_url': url_for('main.browse', sub_path=current_path) if current_path else url_for('main.index')
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao criar pasta: {str(e)}', 'success': False}), 500

@main_bp.route('/move_item', methods=['POST'])
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
            'redirect_url': url_for('main.index')
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao mover item: {str(e)}', 'success': False}), 500

@main_bp.route('/download/<path:file_path>')
@login_required
def download(file_path):
    from servidor_app.models.file_system_model import FileSystemModel
    import os
    from flask import send_from_directory, send_file

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
    full_path = os.path.join(current_app.config['ROOT_DIR'], file_path)

    # Security check
    if not os.path.abspath(full_path).startswith(os.path.abspath(current_app.config['ROOT_DIR'])):
        return jsonify({'message': 'Acesso negado', 'success': False}), 403

    if not os.path.exists(full_path):
        return jsonify({'message': 'Arquivo não encontrado', 'success': False}), 404

    if os.path.isdir(full_path):
        # If it's a directory, create a zip file
        memory_file, download_name = fs_model.create_zip_from_folder(file_path)
        if memory_file:
            memory_file.seek(0)
            return send_file(
                memory_file,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/zip'
            )
        else:
            return jsonify({'message': 'Erro ao criar arquivo zip', 'success': False}), 500
    else:
        # If it's a file, send it directly
        directory = os.path.dirname(full_path)
        return send_from_directory(directory, os.path.basename(full_path), as_attachment=True)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('404.html', dados_servidor=dados_servidor), 404
