from sgo.database import conectar

from models import listar_logs





def registrar_log(usuario_id,acao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (usuario_id, acao) VALUES (?, ?)",
        (usuario_id, acao)
    )

    conn.commit()
    conn.close()