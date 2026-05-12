from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
# A secret_key é obrigatória para usar o 'session' (o que mantém você logado)
app.secret_key = 'chave_secreta_para_vendas'

# --- FUNÇÕES DE BANCO DE DADOS ---
def conectar_bd():
    # Conecta ao arquivo sqlite (cria se não existir)
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

def iniciar_banco():
    # Cria as tabelas necessárias se elas ainda não existirem
    with conectar_bd() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS clientes 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT)''')
        db.execute('''CREATE TABLE IF NOT EXISTS produtos 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL)''')
        db.execute('''CREATE TABLE IF NOT EXISTS vendas 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT, produto TEXT, total REAL)''')
        db.commit()

# Rodar a criação das tabelas ao abrir o programa
iniciar_banco()

# --- ROTAS DO SISTEMA ---

@app.route('/')
def index():
    # Verifica se o usuário está logado na sessão
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        # LOGIN: admin / SENHA: 123
        if usuario == 'admin' and senha == '123':
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            erro = "Usuário ou senha inválidos!"
            
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    db = conectar_bd()
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        db.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        db.commit()
    
    lista = db.execute('SELECT * FROM clientes').fetchall()
    return render_template('clientes.html', clientes=lista)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    db = conectar_bd()
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        db.execute('INSERT INTO produtos (nome, preco) VALUES (?, ?)', (nome, preco))
        db.commit()
    
    lista = db.execute('SELECT * FROM produtos').fetchall()
    return render_template('produtos.html', produtos=lista)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    db = conectar_bd()
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        produto = request.form.get('produto')
        total = request.form.get('total')
        db.execute('INSERT INTO vendas (cliente, produto, total) VALUES (?, ?, ?)', 
                   (cliente, produto, total))
        db.commit()
    
    lista = db.execute('SELECT * FROM vendas').fetchall()
    return render_template('vendas.html', vendas=lista)

if __name__ == '__main__':
    # Rode o app em modo debug para ver erros detalhados no navegador
    app.run(debug=True)
