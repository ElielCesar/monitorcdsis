# Código separado para lidar com o banco
import sqlite3

# função para conectar ao banco
def conectar_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c


# função para criar tabela se não existir
def criar_tabela():
    conn, c = conectar_db()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS monitorados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
        )
        ''')
    conn.commit()
    conn.close()

# função para adicionar URL
def adicionar_url(url):
    conn, c = conectar_db()
    c.execute('INSERT INTO monitorados (url) VALUES (?)', (url,))
    conn.commit()
    conn.close()


# função para buscar todas as URLs
def listar_urls():
    conn, c = conectar_db()
    c.execute('SELECT * FROM monitorados')
    dados = c.fetchall()
    conn.close()
    return dados

# função para atualizar uma url
def atualizar_url(id, nova_url):
    conn, c = conectar_db()
    c.execute('UPDATE monitorados SET url = ? WHERE id = ?', (nova_url, id))
    conn.commit()
    conn.close()

# função para excluir uma url
def excluir_url(id):
    conn, c = conectar_db()
    c.execute('DELETE FROM monitorados WHERE id = ?', (id,))
    conn.commit()
    conn.close()