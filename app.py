from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
io = SocketIO(app)
app.secret_key= "lotus"

import routes

if __name__ == "__main__":
    io.run(app, host='0.0.0.0', debug=True)

