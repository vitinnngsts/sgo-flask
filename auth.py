from flask import Blueprint, request, session, redirect, render_template
from werkzeug.security import check_password_hash
from models import buscar_usuario_por_email
from logs import registrar_log

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    senha = request.form['senha']

    usuario = buscar_usuario_por_email(email)

    if usuario and check_password_hash(usuario[3], senha):
        session['usuario_id'] = usuario[0]
        session['role'] = usuario[4]

        # 👇 AQUI É O LOG
        registrar_log(usuario[0], 'login')

        return redirect('/dashboard')

    return 'Credenciais inválidas', 401


@auth.route('/logout')
def logout():
    usuario_id = session.get('usuario_id')

    if usuario_id:
        registrar_log(usuario_id, 'logout')

    session.clear()
    return redirect('/login')
