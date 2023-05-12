from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

app = Flask('__name__')
app.config.from_object('config.Config')
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


