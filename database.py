import sqlite3


def criar_banco():
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()

    # Tabela de Alunos
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS alunos
                   (
                       matricula
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome
                       TEXT
                       NOT
                       NULL,
                       dt_nascimento
                       TEXT
                   );
                   """)

    # Tabela de Disciplinas
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS disciplinas
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome
                       TEXT
                       NOT
                       NULL,
                       turma
                       TEXT,
                       sala
                       TEXT,
                       professor
                       TEXT
                   );
                   """)

    # Tabela de Notas (com chaves estrangeiras)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS notas
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       valor
                       REAL
                       NOT
                       NULL,
                       matricula_aluno
                       INTEGER,
                       disciplina_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       matricula_aluno
                   ) REFERENCES alunos
                   (
                       matricula
                   ),
                       FOREIGN KEY
                   (
                       disciplina_id
                   ) REFERENCES disciplinas
                   (
                       id
                   )
                       );
                   """)

    # cursor.execute("DROP TABLE IF EXISTS notas;")
    # cursor.execute("DROP TABLE IF EXISTS disciplinas;")
    # cursor.execute("DROP TABLE IF EXISTS alunos;")

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect('escola.db')