import os

class Config:
    # Base configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SECRET_KEY = 'your_secret_key'
    DATABASE_URI = 'sqlite:///cms.db'
    
    # Template configuration
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 