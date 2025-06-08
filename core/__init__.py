from flask import Flask
from flask_login import LoginManager
from core.config.config import config
from core.database import init_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    init_db(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from core.controllers.auth import auth_bp
    from core.controllers.content import content_bp
    from core.controllers.dashboard import dashboard_bp
    from core.controllers.settings import settings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)
    
    return app 