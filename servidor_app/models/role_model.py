from .. import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    # Store allowed navigation areas as a JSON string list
    allowed_areas = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'
