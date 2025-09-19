from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from servidor_app.models.system_link_model import SystemLink
from servidor_app.services.server_info_service import get_server_info
from servidor_app.services.metrics_service import metrics_service
from servidor_app.services.optimization_service import performance_optimizer
from servidor_app.controllers.permissions import require_access, AREAS
from servidor_app import db
import os
import logging

system_bp = Blueprint('system', __name__)

@system_bp.route('/sistemas')
@login_required
@require_access(AREAS['sistemas'])
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
    return render_template('system/sistemas.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@system_bp.route('/portal')
@login_required
@require_access(AREAS['sistemas'])
def portal():
    # Portal page with blocks of system links
    links = SystemLink.query.all()
    # Group links by block
    blocks = {}
    for link in links:
        block = link.block or 'Geral'
        if block not in blocks:
            blocks[block] = []
        blocks[block].append(link)

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('system/portal.html', blocks=blocks, dados_servidor=dados_servidor)

@system_bp.context_processor
def inject_blocks():
    # Provide distinct blocks for use in templates like portal_add.html
    distinct_blocks = [row[0] for row in db.session.query(SystemLink.block).distinct().all() if row[0]]
    # Also include a default block 'Geral' if not present
    if 'Geral' not in distinct_blocks:
        distinct_blocks.append('Geral')
    return dict(distinct_blocks=distinct_blocks)

@system_bp.route('/portal/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['sistemas'])
def edit_system_link(link_id):
    link = SystemLink.query.get_or_404(link_id)

    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        block = request.form.get('block')
        icon = request.form.get('icon')

        if not name or not url:
            flash('Nome e URL são obrigatórios.', 'danger')
            return redirect(url_for('system.edit_system_link', link_id=link_id))

        link.name = name
        link.url = url
        link.block = block
        link.icon = icon

        db.session.commit()
        flash('Link atualizado com sucesso.', 'success')
        return redirect(url_for('system.portal'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('system/portal_add.html', link=link, dados_servidor=dados_servidor)

@system_bp.route('/portal/<int:link_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['sistemas'])
def delete_system_link(link_id):
    link = SystemLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link excluído com sucesso.', 'success')
    return redirect(url_for('system.portal'))

@system_bp.route('/portal/add', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['sistemas'])
def add_system_link():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        block = request.form.get('block')
        icon = request.form.get('icon')

        if not name or not url:
            flash('Nome e URL são obrigatórios.', 'danger')
            return redirect(url_for('system.add_system_link'))

        new_link = SystemLink(name=name, url=url, block=block, icon=icon)
        db.session.add(new_link)
        db.session.commit()
        flash('Link adicionado com sucesso.', 'success')
        return redirect(url_for('system.portal'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('system/portal_add.html', dados_servidor=dados_servidor)

@system_bp.route('/licitacoes')
@login_required
@require_access(AREAS['licitacoes'])
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
    return render_template('main/licitacoes.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@system_bp.route('/dropbox')
@login_required
@require_access(AREAS['dropbox'])
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
    return render_template('main/dropbox.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor, error_message=error_message)

@system_bp.route('/metrics')
@login_required
@require_access(AREAS['metrics'])
def metrics():
    # Metrics monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    system_resources = performance_optimizer.get_system_resources()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('main/metrics.html', dados_servidor=dados_servidor, system_resources=system_resources, metrics_summary=metrics_summary)

@system_bp.route('/performance')
@login_required
@require_access(AREAS['performance'])
def performance():
    # Performance monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    performance_stats = performance_optimizer.get_performance_stats()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('main/performance.html', dados_servidor=dados_servidor, performance_stats=performance_stats, metrics_summary=metrics_summary)
