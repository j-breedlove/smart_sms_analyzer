from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
csrf = CSRFProtect(app)
CORS(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    # __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(1000))
    # Add the relationship to Messages
    messages = relationship("SMS", backref='user', lazy='dynamic')


class SMS(db.Model):
    # __bind_key__ = 'blog'
    __tablename__ = "sms"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    direction = db.Column(db.String(10), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify(message="Flask and React are connected!"), 200


if __name__ == '__main__':
    app.run(debug=True)
