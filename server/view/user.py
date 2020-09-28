from flask import request
from flask_restful import Resource

from server.controller.user import sign_up


# class Auth(Resource):
#
#     def post(self):
#         email = request.json['email']
#         password = request.json['password']
#
#         login(email, password)


class User(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        nickname = request.json['nickname']
        age = request.json['age']

        sign_up(email, password, nickname, age)
