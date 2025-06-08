from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from core.controllers.base import BaseController
from core.models.user import User
from core import login_manager

auth_bp = Blueprint('auth', __name__)
auth_controller = BaseController(User)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        
        flash('Invalid username or password', 'danger')
    return auth_controller.render('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email)
        user.password = password
        user.save()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return auth_controller.render('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login')) 