from core.database import db
from datetime import datetime

class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the model instance to the database"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete the model instance from the database"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """Get a model instance by its ID"""
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        """Get all instances of the model"""
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs):
        """Create a new instance of the model"""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, **kwargs):
        """Update the model instance with the given attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        return self.save()

    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        } 