from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from servidor_app.models.user_model import User
from servidor_app.models.role_model import Role
from servidor_app.services.server_info_service import get_server_info
from servidor_app.controllers.permissions import require_access, AREAS
from servidor_app import db
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@require_access(AREAS['admin'])
def admin():
    # Get all users and roles for admin dashboard
    users = User.query.all()
    roles = Role.query.all()
    # Remove dados_servidor here to avoid conflict with global context processor
    return render_template('admin/admin.html', users=users, roles=roles)

@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Don't allow deleting self
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.admin'))

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    flash(f'Usuário {user.username} foi excluído com sucesso.', 'success')
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)

    # Don't allow blocking self
    if user.id == current_user.id:
        flash('Você não pode bloquear sua própria conta.', 'danger')
        return redirect(url_for('admin.admin'))

    # Toggle active status
    user.is_active = not user.is_active
    db.session.commit()

    status = 'desbloqueado' if user.is_active else 'bloqueado'
    flash(f'Usuário {user.username} foi {status} com sucesso.', 'success')
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/<int:user_id>/assign_role', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def assign_role(user_id):
    user = User.query.get_or_404(user_id)
    role_id = request.form.get('role_id')

    if role_id:
        role = Role.query.get_or_404(role_id)
        user.role = role
        db.session.commit()
        flash(f'Função {role.name} atribuída com sucesso ao usuário {user.username}.', 'success')
    else:
        # Remove role assignment
        user.role = None
        db.session.commit()
        flash(f'Função removida com sucesso do usuário {user.username}.', 'success')

    return redirect(url_for('admin.admin'))

# Role Management Routes
@admin_bp.route('/admin/roles')
@login_required
@require_access(AREAS['admin'])
def admin_roles():
    # Get all roles for admin dashboard
    roles = Role.query.all()
    return render_template('admin/admin_roles.html', roles=roles)

@admin_bp.route('/admin/roles/create', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['admin'])
def create_role():
    if request.method == 'POST':
        name = request.form.get('name')
        allowed_areas = request.form.getlist('allowed_areas')

        if not name:
            flash('Nome da função é obrigatório.', 'danger')
            return redirect(url_for('admin.create_role'))

        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            flash('Nome da função já existe.', 'danger')
            return redirect(url_for('admin.create_role'))

        new_role = Role(
            name=name,
            allowed_areas=json.dumps(allowed_areas)
        )
        db.session.add(new_role)
        db.session.commit()
        flash('Função criada com sucesso.', 'success')
        return redirect(url_for('admin.admin_roles'))

    return render_template('admin/admin_role_form.html', role=None)

@admin_bp.route('/admin/roles/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['admin'])
def edit_role(role_id):
    role = Role.query.get_or_404(role_id)

    if request.method == 'POST':
        name = request.form.get('name')
        allowed_areas = request.form.getlist('allowed_areas')

        if not name:
            flash('Nome da função é obrigatório.', 'danger')
            return redirect(url_for('admin.edit_role', role_id=role_id))

        existing_role = Role.query.filter_by(name=name).first()
        if existing_role and existing_role.id != role_id:
            flash('Nome da função já existe.', 'danger')
            return redirect(url_for('admin.edit_role', role_id=role_id))

        role.name = name
        role.allowed_areas = json.dumps(allowed_areas)
        db.session.commit()
        flash('Função atualizada com sucesso.', 'success')
        return redirect(url_for('admin.admin_roles'))

    return render_template('admin/admin_role_form.html', role=role)

@admin_bp.route('/admin/roles/<int:role_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)

    # Check if role is assigned to any users
    if role.users:
        flash('Não é possível excluir uma função que está atribuída a usuários.', 'danger')
        return redirect(url_for('admin.admin_roles'))

    db.session.delete(role)
    db.session.commit()
    flash(f'Função {role.name} foi excluída com sucesso.', 'success')
    return redirect(url_for('admin.admin_roles'))
