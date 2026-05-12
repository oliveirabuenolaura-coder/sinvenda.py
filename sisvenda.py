from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta_facil'

# Função para conectar ao banco
def conectar_bd():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabelas iniciais
with conectar_bd() as db:
    db.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, email TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL)')
    db.execute('CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY, cliente TEXT, produto TEXT, total REAL)')

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == '123':
            session['usuario'] = 'admin'
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    db = conectar_bd()
    if request.method == 'POST':
        db.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', 
                   (request.form['nome'], request.form['email']))
        db.commit()
    lista = db.execute('SELECT * FROM clientes').fetchall()
    return render_template('clientes.html', clientes=lista)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    db = conectar_bd()
    if request.method == 'POST':
        db.execute('INSERT INTO produtos (nome, preco) VALUES (?, ?)', 
                   (request.form['nome'], request.form['preco']))
        db.commit()
    lista = db.execute('SELECT * FROM produtos').fetchall()
    return render_template('produtos.html', produtos=lista)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    db = conectar_bd()
    if request.method == 'POST':
        db.execute('INSERT INTO vendas (cliente, produto, total) VALUES (?, ?, ?)', 
                   (request.form['cliente'], request.form['produto'], request.form['total']))
        db.commit()
    lista = db.execute('SELECT * FROM vendas').fetchall()
    return render_template('vendas.html', vendas=lista)

if __name__ == '__main__':
    app.run(debug=True)
