from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user, login_user, logout_user
from servidor_app.models.user_model import User
from servidor_app import db
from servidor_app.services.server_info_service import get_server_info

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('A senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('auth.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso. Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/perfil')
@login_required
def perfil():
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('perfil.html', user=current_user, dados_servidor=dados_servidor)

@auth_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    if request.method == 'POST':
        new_username = request.form.get('username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'danger')
            return redirect(url_for('auth.configuracoes'))

        if new_password != confirm_password:
            flash('A nova senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('auth.configuracoes'))

        if new_username:
            current_user.username = new_username
        if new_password:
            current_user.set_password(new_password)

        db.session.commit()
        flash('Configurações atualizadas com sucesso.', 'success')
        return redirect(url_for('auth.perfil'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('configuracoes.html', user=current_user, dados_servidor=dados_servidor)
