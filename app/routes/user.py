from flask import jsonify, request, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from run import db
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/signup/', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        abort(400, "User with this email already exists")
    user = User(email=email, password=generate_password_hash(password, method='SHA256'))
    db.session.add(user)
    db.session.commit()
    return {"message": "Signup successfully"}


@simple_page.route("/login/", methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        raise abort(400, "Incorrect Credentials")
    raise abort(400, " User with this email does not exist")
