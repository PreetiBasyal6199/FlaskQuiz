from decouple import config
import os


class Config:
    SECRET_KEY = config('SECRET_KEY', default="TESTSECRETKEY")
    """
    Database URI is taken from .env file
    Format of database URI:
    
    'postgresql://{{user}}:{password}@{{host}}:{port}/{database_name}'
    """
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI',
                                     default='postgresql://postgres:postgres@localhost:5432/quiz')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key'
