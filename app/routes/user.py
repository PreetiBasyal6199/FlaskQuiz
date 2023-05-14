from flask import jsonify, request, Blueprint, abort
from app.models import User
from run import db
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.schema import UserCreateSchema, UserLoginSchema
from werkzeug.security import generate_password_hash

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/signup/', methods=['POST'])
def signup():
    try:
        user_schema = UserCreateSchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400
    user_obj = User(email=user_schema['email'],
                    password=generate_password_hash(user_schema['password'], method='SHA256'),
                    is_admin=user_schema.get("is_admin"))
    db.session.add(user_obj)
    db.session.commit()
    return {"message": "Signup successfully"}


@simple_page.route("/login/", methods=['POST'])
def login():
    try:
        user = UserLoginSchema().load(request.json)  # load the request data into schema for validation
        validated_data = UserLoginSchema().validate(user)
        user_obj = User.query.filter_by(email=validated_data.get('email')).first()  # get the user object from email
        access_token = create_access_token(identity=user_obj.id)    # generates access token for JWT authentication
        return jsonify({"access_token": access_token}), 200
    except ValidationError as err:
        return err.messages, 400
