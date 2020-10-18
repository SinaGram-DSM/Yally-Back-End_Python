from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token

from server.controller.user import sign_up, login
from server.controller.mail import send_email, check_auth_code, change_password
from server.view import check_json


class Auth(Resource):

    @check_json({
        "email": str,
        "password": str
    })
    def post(self):
        email = request.json['email']
        password = request.json['password']

        return login(email, password)


class User(Resource):

    @check_json({
        "email": str,
        "password": str,
        "nickname": str,
        "age": int
    })
    def post(self):
        email = request.json['email']
        password = request.json['password']
        nickname = request.json['nickname']
        age = request.json['age']

        return sign_up(email, password, nickname, age)


class Refresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()

        return {
            'accessToken': create_access_token(identity=user)
        }


class SendAuthEmail(Resource):

    @check_json({
        "email": str
    })
    def post(self):
        email = request.json['email']

        return send_email(email, codetype='auth')


class SendResetEmail(Resource):

    @check_json({
        "email": str
    })
    def post(self):
        email = request.json['email']

        return send_email(email, codetype='reset')


class CheckAuthCode(Resource):

    @check_json({
        "email": str,
        "code": str
    })
    def post(self):
        email = request.json['email']
        code = request.json['code']
        return check_auth_code(email, code)


class ChangePassword(Resource):

    @check_json({
        "email": str,
        "code": str,
        "password": str
    })
    def put(self):
        email = request.json['email']
        code = request.json['code']
        password = request.json['password']

        return change_password(email, code, password)




