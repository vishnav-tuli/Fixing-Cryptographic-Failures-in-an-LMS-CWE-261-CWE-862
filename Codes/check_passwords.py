from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"Username: {user.username}, Password Hash: {user.password_hash}")
