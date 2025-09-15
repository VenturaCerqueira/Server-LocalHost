from datetime import datetime
from servidor_app import db

class SystemLink(db.Model):
    __tablename__ = 'system_links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    icon = db.Column(db.String(255), nullable=True)  # Icon class name from icon package
    block = db.Column(db.String(255), nullable=True)  # Optional category/block
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SystemLink {self.name} ({self.url})>"
