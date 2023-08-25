import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# csrf = CSRFProtect(app)
CORS(app)

# CONNECT TO DB
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    name = request.json.get('name')
    password = request.json.get('password')

    if not email or not password:
        return jsonify(message="Please enter your email and password"), 400

    # Check if user already exists
    users_ref = db.collection('users')
    existing_user = users_ref.where('email', '==', email).get()
    if existing_user:
        return jsonify(message="You have already signed up with that email, log in instead!"), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    user_data = {
        'email': email,
        'name': name,
        'password': hashed_password
    }
    users_ref.add(user_data)

    return jsonify(message="You have successfully registered!"), 200


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    users_ref = db.collection('users')
    user_data = users_ref.where('email', '==', email).get()

    if user_data and user_data[0].to_dict():
        stored_password = user_data[0].to_dict().get('password')
        if check_password_hash(stored_password, password):
            return jsonify(message="Successfully logged in!"), 200
        else:
            return jsonify(message="Incorrect password!"), 400
    else:
        return jsonify(message="User not found!"), 404


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify(message="Flask and React are connected!"), 200


if __name__ == '__main__':
    app.run(debug=True)
