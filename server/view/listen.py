from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.controller.listen import listening, unlistening
from server.view import check_json


class Listen(Resource):

    @jwt_required
    @check_json({
        "listeningEmail": str,
    })
    def post(self):
        listening_email = request.json['listeningEmail']
        owner_email = get_jwt_identity()

        return listening(owner_email, listening_email)

    @jwt_required
    @check_json({
        "listeningEmail": str,
    })
    def delete(self):
        listening_email = request.json['listeningEmail']
        owner_email = get_jwt_identity()

        return unlistening(owner_email, listening_email)


