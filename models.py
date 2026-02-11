from database import conectar
from werkzeug.security import generate_password_hash
def buscar_usuario_por_email(email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome, email, senha, role FROM usuarios WHERE email = ?",
        (email,)
    )

    usuario = cursor.fetchone()
    conn.close()
    return usuario

def listar_logs():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
           SELECT l.id, u.nome, l.acao, l.criado_em
           FROM logs l
           LEFT JOIN usuarios u ON u.id = l.usuario_id
           ORDER BY l.criado_em DESC
       """)

    logs = cursor.fetchall()
    conn.close()
    return logs


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT id, nome, email, role, criado_em
            FROM usuarios
            ORDER BY criado_em DESC
        """)

    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def criar_usuario(nome, email, senha,role):
    conn = conectar()
    cursor = conn.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, role)
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha_hash, role))

    conn.commit()
    conn.close()


def buscar_usuario_por_id(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, role
        FROM usuarios
        WHERE id = ?
    """, (usuario_id,))

    usuario = cursor.fetchone()
    conn.close()
    return usuario


def atualizar_usuario(usuario_id, nome, email, role):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, email = ?, role = ?
        WHERE id = ?
    """, (nome, email, role, usuario_id))

    conn.commit()
    conn.close()

def deletar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (usuario_id,)
    )

    conn.commit()
    conn.close()
