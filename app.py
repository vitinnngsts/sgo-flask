from flask import Flask, session, redirect,render_template,request
from database import criar_tabelas
from auth import auth
from functools import wraps
from models import listar_logs,listar_usuarios,criar_usuario,buscar_usuario_por_id,atualizar_usuario,deletar_usuario



app = Flask(__name__)
app.secret_key = 'super-secret'

app.register_blueprint(auth)

# ------------------------
# DECORATORS
# ------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return 'Acesso negado', 403
        return f(*args, **kwargs)
    return decorated


# ------------------------
# ROTAS
# ------------------------

@app.route('/')
def index():
    return 'SGO rodando 🚀'


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/logs')
@login_required
@admin_required
def logs():
    logs = listar_logs()
    return render_template('logs.html', logs=logs)

@app.route('/usuarios')
@login_required
@admin_required
def usuarios():
    usuarios = listar_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

from flask import request
from models import criar_usuario

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_usuario():
    if request.method == 'GET':
        return render_template('novo_usuario.html')

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    role = request.form['role']

    criar_usuario(nome, email, senha, role)

    return redirect('/usuarios')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return 'Área administrativa 👑'

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    if request.method == 'GET':
        usuario = buscar_usuario_por_id(id)
        return render_template('editar_usuario.html', usuario=usuario)

    nome = request.form['nome']
    email = request.form['email']
    role = request.form['role']

    atualizar_usuario(id, nome, email, role)

    return redirect('/usuarios')


@app.route('/usuarios/<int:id>/deletar')
@login_required
@admin_required
def deletar(id):
    # evita apagar a si mesmo (opcional mas recomendado)
    if session.get('usuario_id') == id:
        return 'Você não pode apagar seu próprio usuário', 400

    deletar_usuario(id)
    return redirect('/usuarios')



# ------------------------
# START
# ------------------------

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)
