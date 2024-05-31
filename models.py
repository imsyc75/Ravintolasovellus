from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        self.password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
