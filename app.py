from datetime import datetime
from flask import Flask, render_template, session, redirect, request
from flask.helpers import url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key= "lotus"
io = SocketIO(app)

mensagems = []

def get_time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@app.route("/")
def home():
    if 'user' not in session:
        return redirect('login')
    return render_template("chat.html", mensagems=mensagems)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/trocarUsuario')
def trocar_usuario():
    return redirect(url_for('login'))
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    session['user'] = request.form['user']
    return redirect(url_for('home'))

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

