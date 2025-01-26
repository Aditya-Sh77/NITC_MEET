from extensions import db

# User model for SQLite
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    email = db.Column(db.String(120), unique=True, nullable=False)  # User email
    password = db.Column(db.String(120), nullable=False)  # Hashed password
    name = db.Column(db.String(100), nullable=False)  # User name
