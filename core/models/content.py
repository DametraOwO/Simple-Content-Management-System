from core.models.base import BaseModel
from core.database import db

class Content(BaseModel):
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Content {self.title}>'
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get all contents for a specific user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.date.desc()).all()
    
    @classmethod
    def get_published(cls):
        """Get all published contents"""
        return cls.query.filter_by(status='Published').order_by(cls.date.desc()).all()
    
    @classmethod
    def get_drafts(cls):
        """Get all draft contents"""
        return cls.query.filter_by(status='Draft').all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author.username if self.author else None
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit() 