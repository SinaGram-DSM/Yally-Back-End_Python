from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

from server.model import session
from server.model.user import User


def create_new_user(email, password, nickname, age):

    new_user = User(email=email,
                    password=generate_password_hash(password),
                    nickname=nickname,
                    age=age)

    session.add(new_user)
    session.commit()


def sign_up(email, password, nickname, age):

    user = session.query(User).filter(User.email).first()

    if user:
        return abort(409, "This email is already sign up")

    try:

        create_new_user(email, password, nickname, age)

        return {
            "message": "Successfully signed up"
        }

    except SQLAlchemyError:
        session.rollback()
        return abort(500, "db_error")


def login(email, password):
    pass
