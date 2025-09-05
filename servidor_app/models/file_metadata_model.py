from .. import db
from datetime import datetime

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True, nullable=False)  # Relative path from root_dir
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_files')
    updated_by = db.relationship('User', foreign_keys=[updated_by_id], backref='updated_files')

    def __repr__(self):
        return f'<FileMetadata {self.path}>'
