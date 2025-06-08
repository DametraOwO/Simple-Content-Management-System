from flask import Blueprint, request
from flask_login import login_required, current_user
from core.controllers.base import BaseController
from core.models.user import User

settings_bp = Blueprint('settings', __name__)
settings_controller = BaseController()

@settings_bp.route('/')
@login_required
def index():
    return settings_controller.render('settings/index.html')

@settings_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if username is already taken
        if username != current_user.username:
            if User.query.filter_by(username=username).first():
                settings_controller.flash('Username already taken', 'danger')
                return settings_controller.redirect('settings.profile')
        
        # Check if email is already taken
        if email != current_user.email:
            if User.query.filter_by(email=email).first():
                settings_controller.flash('Email already registered', 'danger')
                return settings_controller.redirect('settings.profile')
        
        # Update user profile
        current_user.username = username
        current_user.email = email
        
        # Update password if provided
        if current_password and new_password:
            if not current_user.verify_password(current_password):
                settings_controller.flash('Current password is incorrect', 'danger')
                return settings_controller.redirect('settings.profile')
            
            if new_password != confirm_password:
                settings_controller.flash('New passwords do not match', 'danger')
                return settings_controller.redirect('settings.profile')
            
            current_user.password = new_password
        
        current_user.save()
        settings_controller.flash('Profile updated successfully', 'success')
        return settings_controller.redirect('settings.profile')
    
    return settings_controller.render('settings/profile.html')

@settings_bp.route('/appearance')
@login_required
def appearance():
    return settings_controller.render('settings/appearance.html')

@settings_bp.route('/notifications')
@login_required
def notifications():
    return settings_controller.render('settings/notifications.html') 