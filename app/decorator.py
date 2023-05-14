from flask import abort
from flask_login import current_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User


def is_admin(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            abort(401, "You don't have permission to access this resource")
        return func(*args, **kwargs)

    return wrapper
