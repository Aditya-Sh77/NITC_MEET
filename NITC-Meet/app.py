# from flask import Flask, render_template, request, jsonify
# from extensions import db, bcrypt, socketio,emit
# from models import User

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize extensions
# db.init_app(app)
# bcrypt.init_app(app)
# socketio.init_app(app)

# @app.route('/')
# def login_page():
#     return render_template('login.html')

# @app.route('/welcome')
# def welcome_page():
#     return render_template('welcome.html')

# @app.route('/video_chat')
# def video_chat_page():
#     return render_template('vc.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     user = User.query.filter_by(email=data['email']).first()

#     if user and bcrypt.check_password_hash(user.password, data['password']):
#         return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'name': user.name}})
#     return jsonify({'message': 'Invalid email or password'}), 401

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
#     new_user = User(email=data['email'], password=hashed_password, name=data['name'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'Registration successful'})

# @socketio.on('signal')
# def handle_signal(data):
#     emit('signal', data, broadcast=True)

# @socketio.on('join_room')
# def on_join(data):
#     room = data['room']
#     emit('join_room', {'message': f'User joined room {room}'}, room=room)

# if __name__ == '__main__':
#     with app.app_context():  # Ensure you're in an application context
#         db.create_all()  # Create database tables
#     socketio.run(app, debug=True)


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO , emit
import random
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socket = SocketIO(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'redirect': '/welcome'})
    return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'})

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html')

# Sample list of users connected for video calls
connected_users = []
@socket.on('skip')
def handle_skip():

    if request.sid in connected_users:
        connected_users.remove(request.sid)  # Remove the current user temporarily
        logger.debug(f"User {request.sid} skipped.")

    if len(connected_users) > 0:
        random_peer = random.choice(connected_users)
        connected_users.append(request.sid)  # Re-add the user
        emit('signal', {'action': 'new_peer', 'peer_id': random_peer}, room=request.sid)
        emit('signal', {'action': 'new_peer', 'peer_id': request.sid}, room=random_peer)
    else:
        emit('signal', {'action': 'no_peer'}, room=request.sid)
    logger.debug(f"User {request.sid} skipped.")    


@socket.on('connect')
def handle_connect():
    # Store the connected user in connected_users list
    connected_users.append(request.sid)
    print(f"User connected: {request.sid}")

@socket.on('disconnect')
def handle_disconnect():
    # Remove the disconnected user from connected_users list
    if request.sid in connected_users:
        connected_users.remove(request.sid)
    print(f"User disconnected: {request.sid}")

@socket.on('signal')
def handle_signal(data):
    target = data.get('target')
    if target:
        emit('signal', data, room=target)  # Relay the signal to the target peer
    else:
        print("No target specified in signal data.")


@socket.on('request_random_peer')
def handle_random_peer_request():
    # Find a random peer for the new user
    if len(connected_users) > 1:
        # Make sure there are at least two users
        random_peer = random.choice([user for user in connected_users if user != request.sid])
        emit('signal', {'offer': generate_offer_for_user(request.sid, random_peer)}, room=random_peer)
        emit('signal', {'message': 'Connected to random peer'}, room=request.sid)
    else:
        emit('signal', {'message': 'No peers available at the moment.'}, room=request.sid)

# Generate an offer for the user
def generate_offer_for_user(user_sid, peer_sid):
    # Logic to generate an SDP offer for the peer
    # The offer can be based on WebRTC's createOffer
    offer = "Generated SDP Offer"
    return offer

if __name__ == '__main__':
    print("Starting server...")
    socket.run(app, debug=True)
