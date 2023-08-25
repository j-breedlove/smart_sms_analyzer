from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# csrf = CSRFProtect(app)
CORS(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#
with app.app_context():
    db.create_all()


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(1000))
    messages = db.relationship("SMS", backref='user', lazy='dynamic')


class SMS(db.Model):
    __tablename__ = "sms"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Renamed column to user_id
    direction = db.Column(db.String(10), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)


@app.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    print(email)
    name = request.json.get('name')
    password = request.json.get('password')
    # confirm_password = request.json.get('confirm_password')

    if not email or not password:
        return jsonify(message="Please enter your email and password"), 400
    if User.query.filter_by(email=email).first():
        return jsonify(message="You have already signed up with that email, log in instead!"), 400

    user = User()
    user.email = email
    user.name = name
    user.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    db.session.add(user)
    db.session.commit()
    # login_user(user)
    return jsonify(message="You have successfully registered!"), 200


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify(message="Flask and React are connected!"), 200


if __name__ == '__main__':
    app.run(debug=True)
