from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

from server.model import session
from server.model.user import User
from server.model import Redis


def create_new_user(email, password, nickname, age):

    new_user = User(email=email,
                    password=generate_password_hash(password),
                    nickname=nickname,
                    age=age)

    session.add(new_user)
    session.commit()


def sign_up(email, password, nickname, age):

    user = session.query(User).filter(User.email == email).first()

    if user:
        return abort(409, "This email is already sign up")

    try:
        create_new_user(email, password, nickname, age)

        return {
            "message": "Successfully signed up"
        }, 201

    except SQLAlchemyError:
        session.rollback()
        return abort(500, "db_error")


def login(email, password):

    user = session.query(User).filter(User.email == email).first()

    if user:
        user_pw = check_password_hash(user.password, password)

        if user_pw:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)

            return {
                "accessToken": access_token,
                "refreshToken": refresh_token
            }

        else:
            return abort(400, "The password is incorrect")
    else:
        return abort(404, "The email is incorrect")


def check_auth_code(email, code):
    auth_code = Redis.get(email).decode('utf-8')

    if auth_code == code:
        return {
            "message": "Successfully authenticated"
        }
    else:
        return abort(401, "The verification code is not correct")



