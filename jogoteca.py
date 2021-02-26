from flask import Flask
from models import Jogo
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = MySQL(app)

from views import *

if __name__ == '__main__':
    app.run(debug= True,port = 8080)

'''
usuario1 = Usuario('thi', "Thi", "Mestre")
usuario2 = Usuario('dani', "Dani", "Especialista")
usuario3 = Usuario('hulk', "Luci", "Apresentador")

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3}
'''
'''
jogoOne = Jogo("Doom Eternal", "FPS", "Xbox One")
jogoTwo = Jogo("Need for Speed Heat", "Corrida", "PC")
jogoThree = Jogo("New Super Mario U Deluxe", "Plataforma", "Nintendo Switch")
lista = [jogoOne, jogoTwo, jogoThree]
'''