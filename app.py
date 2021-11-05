from datetime import datetime
from flask import Flask, render_template, session, redirect, request
from flask.helpers import url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
io = SocketIO(app)
app.secret_key= "lotus"

mensagems = []

def get_time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
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

@app.route('/admin')
def admin():
    if session.get('admin') == True:
        return render_template("admin.html", mensagems=mensagems)
    else:
        return redirect(url_for('login_admin'))

@app.route('/deletar/<int:indice>')
def deletar(indice):
    del(mensagems[indice])
    return redirect(url_for('admin'))

@app.route('/login_admin')
def login_admin():
    return render_template('login_admin.html')

@app.route('/autenticar_admin', methods=['POST', ])
def autenticar_admin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if senha == 'batatinhafrita':
        session['user'] = usuario
        session['admin'] = True
        return redirect(url_for('admin'))
    else:
        redirect(url_for('login_admin'))

@app.route('/logout')
def logout():
    session['admin'] = False
    return redirect(url_for('home'))

@io.on('sendMessage')
def message_handler(msg):
    msg['time'] = get_time_now()
    mensagems.append(msg);
    # msg['indice'] = len(mensagems)
    msg['indice'] = mensagems.index(msg)
    emit('getMsg', msg, broadcast=True)


if __name__ == "__main__":
    io.run(app, host='0.0.0.0', debug=True)

