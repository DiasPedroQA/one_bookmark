from flask import Flask
from app.api.v1.controllers import api_bp


def register_routes(app: Flask):
    app.register_blueprint(api_bp, url_prefix='/api/v1')
