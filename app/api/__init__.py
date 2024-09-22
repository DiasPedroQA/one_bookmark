# app/api/__init__.py

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True  # Certifique-se de que isso esteja aqui
    # Configurações adicionais e inicializações
    return app
