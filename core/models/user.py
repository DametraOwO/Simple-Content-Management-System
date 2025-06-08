from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.models.base import BaseModel
from core.database import db

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    contents = db.relationship('Content', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        data = super().to_dict()
        data.pop('password_hash', None)
        return data 