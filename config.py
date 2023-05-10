from decouple import config
import os


class Config:
    SECRET_KEY = config('SECRET_KEY', default="TESTSECRETKEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
