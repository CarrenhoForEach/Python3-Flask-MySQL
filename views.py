from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo
from dao import JogoDao, UsuarioDao
import time
from jogoteca import db, app
from helpers import deleta, recupera_imagem

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    #lista_jogos = ["Jedi", "Super Mario World", "Street fighter 5"]
    return render_template('lista.html', titulo="Jogos legais do Thiago", jogos = lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))
    return render_template("novo.html", titulo = "Criar novo jogo")

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    game = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    #capa_jogo = f'capa{id}.jpg'
    return render_template('editar.html', titulo = "Editar jogo existente", jogo = game, capa_jogo = nome_imagem)


@app.route('/criar', methods = ['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    #arquivo.save(f'uploads/{arquivo.filename}')
    #lista.append(jogo)   
    #return render_template('lista.html', titulo = "jogos legais do Thiago", jogos = lista)
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
    #if request.form['usuario'] in usuarios:
        #usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' você logou com sucesso!!!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        
    else:
        flash("Credencial negada! Tente novamente")
        return redirect(url_for('login'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi deletado com sucesso')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Você foi deslogado. Sua sessão expirou.")
    return redirect(url_for('index'))

@app.route('/uploads/<arquivo_nome>')
def imagem(arquivo_nome):
    return send_from_directory('uploads', arquivo_nome)