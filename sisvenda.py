
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = '123456'

def conectar():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicialização do banco de dados
with conectar() as db:
    db.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL, estoque INTEGER DEFAULT 0)')
    db.execute('CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT, produto TEXT, total REAL)')
    db.commit()

@app.route('/')
def index():
    if 'logado' not in session: return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('usuario') == 'admin' and request.form.get('senha') == '123':
            session['logado'] = True
            return redirect(url_for('index'))
        return "Login incorreto! <a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        if request.method == 'POST':
            db.execute('INSERT INTO clientes (nome, email) VALUES (?,?)', (request.form['nome'], request.form['email']))
            db.commit()
        dados = db.execute('SELECT * FROM clientes').fetchall()
    return render_template('clientes.html', clientes=dados)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        if request.method == 'POST':
            preco = request.form['preco'].replace(',', '.').strip()
            qtd = request.form.get('estoque', 10)
            db.execute('INSERT INTO produtos (nome, preco, estoque) VALUES (?,?,?)', (request.form['nome'], float(preco), int(qtd)))
            db.commit()
        dados = db.execute('SELECT * FROM produtos').fetchall()
    return render_template('produtos.html', produtos=dados)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        if request.method == 'POST':
            total = request.form['total'].replace(',', '.').strip()
            db.execute('INSERT INTO vendas (cliente, produto, total) VALUES (?,?,?)', (request.form['cliente'], request.form['produto'], float(total)))
            db.commit()
        dados = db.execute('SELECT * FROM vendas').fetchall()
    return render_template('vendas.html', vendas=dados)

@app.route('/estoque')
def estoque():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        dados = db.execute('SELECT * FROM produtos').fetchall()
    return render_template('estoque.html', produtos=dados)

@app.route('/financeiro')
def financeiro():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        vendas_dados = db.execute('SELECT * FROM vendas').fetchall()
        resultado = db.execute('SELECT SUM(total) as faturamento FROM vendas').fetchone()
        faturamento = resultado['faturamento'] if resultado['faturamento'] else 0.0
    return render_template('financeiro.html', vendas=vendas_dados, faturamento_total=faturamento, total_vendas=len(vendas_dados))

@app.route('/relatorio')
def relatorio():
    if 'logado' not in session: return redirect(url_for('login'))
    with conectar() as db:
        total_cli = db.execute('SELECT COUNT(*) as qtd FROM clientes').fetchone()['qtd']
        total_prod = db.execute('SELECT COUNT(*) as qtd FROM produtos').fetchone()['qtd']
        vendas_dados = db.execute('SELECT COUNT(*) as qtd FROM vendas').fetchone()['qtd']
        resultado_fin = db.execute('SELECT SUM(total) as faturamento FROM vendas').fetchone()
        faturamento = resultado_fin['faturamento'] if resultado_fin['faturamento'] else 0.0
    return render_template('relatorio.html', total_clientes=total_cli, total_produtos=total_prod, total_vendas=vendas_dados, faturamento_total=faturamento)

if __name__ == '__main__':
    app.run(debug=True)
