from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    mega_filename = db.Column(db.String(255), nullable=False, unique=True)
    size = db.Column(db.BigInteger, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    mega_account_id = db.Column(db.Integer, db.ForeignKey('mega_accounts.id'), nullable=False)
    mega_file_id = db.Column(db.String(255), nullable=False)
    share_link = db.Column(db.Text, nullable=False)
    
    # Relacionamento com MegaAccount
    mega_account = db.relationship('MegaAccount', backref=db.backref('files', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'size': self.size,
            'category': self.category,
            'upload_date': self.upload_date.isoformat(),
            'share_link': self.share_link
        }

