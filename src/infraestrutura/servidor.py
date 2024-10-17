# src/infraestrutura/servidor.py

"""
Módulo principal da aplicação FastAPI.

Este módulo inicializa a aplicação, configura o CORS e define
as rotas e manipuladores de exceções.
"""

import uvicorn
from fastapi import FastAPI

# from fastapi.routing import APIRouter
from aplicacao.rotas import router as rotas_router


# Função para criar e configurar a aplicação FastAPI
def criar_app() -> FastAPI:
    """
    Cria e configura a instância da aplicação FastAPI.

    Returns:
        FastAPI: A instância da aplicação FastAPI configurada.
    """
    aplicativo: FastAPI = FastAPI(
        title="One Bookmark API",
        description="API para validação de caminhos de arquivos e outras funcionalidades.",
        version="1.0.0",
    )

    # Inclui as rotas da aplicação
    aplicativo.include_router(rotas_router)

    return aplicativo


# Função para rodar o servidor usando Uvicorn
def iniciar_servidor() -> None:
    """
    Inicia o servidor Uvicorn para rodar a aplicação FastAPI.
    """
    uvicorn.run(
        "infraestrutura.servidor:criar_app",
        host="127.0.0.1",  # ou "0.0.0.0" para permitir acesso externo
        port=8000,
        log_level="info",
        reload=True,  # Habilita recarregamento automático ao salvar mudanças
    )
