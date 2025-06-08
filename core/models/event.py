from core.models.base import BaseModel
from core.database import db

class Event(BaseModel):
    __tablename__ = 'events'
    
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get all events for a specific user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_upcoming(cls):
        """Get all upcoming events"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        return cls.query.filter(Event.date >= today).order_by(Event.date).all()
    
    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author.username if self.author else None
        return data 