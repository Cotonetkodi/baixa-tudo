from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class MegaAccount(db.Model):
    __tablename__ = 'mega_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)  # Será encriptada
    total_space = db.Column(db.BigInteger, default=0)
    used_space = db.Column(db.BigInteger, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'total_space': self.total_space,
            'used_space': self.used_space,
            'available_space': self.total_space - self.used_space,
            'usage_percentage': round((self.used_space / self.total_space * 100), 2) if self.total_space > 0 else 0,
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat()
        }
    
    def is_nearly_full(self, threshold=90):
        """Verifica se a conta está quase cheia (padrão: 90%)"""
        if self.total_space == 0:
            return False
        return (self.used_space / self.total_space * 100) >= threshold

