from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
io = SocketIO(app)

mensagems = []

def get_time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@app.route("/")
def home():
    return render_template("chat.html", mensagems=mensagems)

@io.on('sendMessage')
def message_handler(msg):
    msg['time'] = get_time_now()
    mensagems.append(msg);
    emit('getMsg', msg, broadcast=True)

@io.on('clearMessages')
def clear_messages_handler():
    mensagems.clear()


if __name__ == "__main__":
    io.run(app, host='0.0.0.0', debug=True)

