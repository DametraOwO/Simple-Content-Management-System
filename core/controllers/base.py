from flask import render_template, redirect, url_for, flash, request, jsonify
from functools import wraps
from flask_login import current_user, login_required

class BaseController:
    def __init__(self, model_class=None):
        self.model_class = model_class

    def render(self, template, **kwargs):
        """Render a template with the given context"""
        return render_template(template, **kwargs)

    def redirect(self, endpoint, **kwargs):
        """Redirect to the given endpoint"""
        return redirect(url_for(endpoint, **kwargs))

    def flash(self, message, category='info'):
        """Flash a message to the user"""
        flash(message, category)

    def json_response(self, data, status_code=200):
        """Return a JSON response"""
        return jsonify(data), status_code

    def get_model(self, id):
        """Get a model instance by ID"""
        if not self.model_class:
            raise NotImplementedError("Model class not set")
        return self.model_class.get_by_id(id)

    def get_all_models(self):
        """Get all model instances"""
        if not self.model_class:
            raise NotImplementedError("Model class not set")
        return self.model_class.get_all()

    def create_model(self, **kwargs):
        """Create a new model instance"""
        if not self.model_class:
            raise NotImplementedError("Model class not set")
        return self.model_class.create(**kwargs)

    def update_model(self, id, **kwargs):
        """Update a model instance"""
        model = self.get_model(id)
        if model:
            return model.update(**kwargs)
        return None

    def delete_model(self, id):
        """Delete a model instance"""
        model = self.get_model(id)
        if model:
            model.delete()
            return True
        return False

    @staticmethod
    def require_auth(f):
        """Decorator to require authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def require_admin(f):
        """Decorator to require admin privileges"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_admin:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function 