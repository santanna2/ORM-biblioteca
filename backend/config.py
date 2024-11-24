import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_secreto'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/Biblioteca'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
