from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = '123456' # Necessário para o login funcionar

def conectar():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Cria o banco e as tabelas se não existirem
with conectar() as db:
    db.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, email TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT, preco REAL)')
    db.execute('CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY, cliente TEXT, produto TEXT, total REAL)')

@app.route('/')
def index():
    if 'logado' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        if user == 'admin' and senha == '123':
            session['logado'] = True
            return redirect(url_for('index'))
        else:
            return "Login incorreto! <a href='/login'>Tentar de novo</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'logado' not in session: return redirect(url_for('login'))
    db = conectar()
    if request.method == 'POST':
        db.execute('INSERT INTO clientes (nome, email) VALUES (?,?)', (request.form['nome'], request.form['email']))
        db.commit()
    dados = db.execute('SELECT * FROM clientes').fetchall()
    return render_template('clientes.html', clientes=dados)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if 'logado' not in session: return redirect(url_for('login'))
    db = conectar()
    if request.method == 'POST':
        db.execute('INSERT INTO produtos (nome, preco) VALUES (?,?)', (request.form['nome'], request.form['preco']))
        db.commit()
    dados = db.execute('SELECT * FROM produtos').fetchall()
    return render_template('produtos.html', produtos=dados)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if 'logado' not in session: return redirect(url_for('login'))
    db = conectar()
    if request.method == 'POST':
        db.execute('INSERT INTO vendas (cliente, produto, total) VALUES (?,?,?)', 
                   (request.form['cliente'], request.form['produto'], request.form['total']))
        db.commit()
    dados = db.execute('SELECT * FROM vendas').fetchall()
    return render_template('vendas.html', vendas=dados)

if __name__ == '__main__':
    app.run(debug=True)
