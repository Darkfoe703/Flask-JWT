from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Hash generator."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hash."""
        return check_password_hash(self.password_hash, password)