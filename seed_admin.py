from werkzeug.security import generate_password_hash
from database import conectar

def criar_admin():
    conn = conectar()
    cursor = conn.cursor()

    nome = 'Admin'
    email = 'admin@sgo.com'
    senha = generate_password_hash('admin123')
    role = 'admin'

    try:
        cursor.execute("""
                INSERT INTO usuarios (nome, email, senha, role)
                VALUES (?, ?, ?, ?)
            """, (nome, email, senha, role))

        conn.commit()
        print('✅ Admin criado com sucesso')
    except Exception as e:
        print('⚠️ Admin já existe ou erro:', e)

    conn.close()


if __name__ == '__main__':
    criar_admin()