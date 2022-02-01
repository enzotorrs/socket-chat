from __main__ import app, io
from flask import render_template, session, redirect, request
from flask_socketio import emit
from flask.helpers import flash, url_for
from utils import get_time_now, admin_is_auth


mensagems = []


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
    if admin_is_auth(senha):
        session['user'] = usuario
        session['admin'] = True
        flash('logado como administrador')
        return redirect(url_for('admin'))
    else:
        flash('Login incorreto')
        return redirect(url_for('login_admin'))

@app.route('/logout')
def logout():
    session['admin'] = False
    flash('deslogado do administrador')
    return redirect(url_for('login'))

@io.on('sendMessage')
def message_handler(msg):
    msg['time'] = get_time_now()
    mensagems.append(msg);
    msg['indice'] = mensagems.index(msg)
    emit('getMsg', msg, broadcast=True)
