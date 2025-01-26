(Note: We couldn't really complete the project but this has whatever we aere able to do (not much))
# NITC_MEET

NITC Meet is a real-time video chat application designed to connect students via their NITC email. The app uses Flask for the backend and WebRTC for peer-to-peer video communication. Users can start, stop, and skip chats, with relevant information displayed about connected peers.

---

## Features
- **User Authentication**: Login and registration using email and password.
- **Real-Time Video Chat**: Peer-to-peer video and audio communication using WebRTC.
- **Random Pairing**: Match users randomly for chats.
- **Skip Functionality**: Skip the current peer and connect with a new one.
- **User Management**: Display a list of connected users on skip for debugging.

---

## Requirements
- Python 3.8+
- Node.js (for WebRTC and Socket.IO frontend integration)

### Python Packages
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-SocketIO

### Frontend
- WebRTC
- HTML/CSS/JavaScript

---

## Installation

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nitc-meet.git
   cd nitc-meet
   ```

2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -c "from app import db; db.create_all()"
   ```

5. Run the Flask app:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Open the `templates` folder and ensure the HTML, CSS, and JavaScript files are in place.
2. Start the frontend by accessing the app at `http://127.0.0.1:5000`.

---

## Usage

### User Login and Registration
- Navigate to the login page (`http://127.0.0.1:5000`).
- Register as a new user or log in with existing credentials.

### Video Chat
- Upon successful login, you will be redirected to the welcome page.
- Start a video chat session with a random peer.
- Use the **Skip** button to connect with another user.
- Mute audio or turn off the camera using the respective buttons.

---

## Code Structure
```
.
├── app.py                # Main Flask application
├── models.py             # Database models
├── extensions.py         # Flask extensions
├── static/               # Static files (CSS, JS, etc.)
├── templates/            # HTML templates
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Debugging Tips

### Print Connected Users on Skip
Ensure `print` statements are working correctly:
```python
@socket.on('skip')
def handle_skip():
    global connected_users
    print("Skip event triggered")
    print("Connected users:", connected_users)
```
Run the Flask app with `debug=True` to see logs in the terminal.

---

---


## Contributors
- Team Thryristor


