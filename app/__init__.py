from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask('__name__')
app.config.from_object('config.Config')
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
jwt = JWTManager(app)


