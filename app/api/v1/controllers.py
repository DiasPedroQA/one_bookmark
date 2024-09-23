from flask import Blueprint, request, jsonify
from app.core.usecases.manipulador_arquivo import ManipuladorArquivo
from app.core.usecases.manipulador_diretorio import ManipuladorDiretorio

api_bp = Blueprint('api', __name__)


@api_bp.route('/arquivos', methods=['POST'])
def criar_arquivo():
    data = request.json
    manipulador = ManipuladorArquivo()
    resultado = manipulador.criar_arquivo(data['caminho'], data['conteudo'])
    return jsonify(resultado), 201


@api_bp.route('/diretorios', methods=['POST'])
def criar_diretorio():
    data = request.json
    manipulador = ManipuladorDiretorio()
    resultado = manipulador.criar_diretorio(data['caminho'])
    return jsonify(resultado), 201
