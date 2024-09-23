import os


class Config:
    DEBUG = os.getenv('DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
