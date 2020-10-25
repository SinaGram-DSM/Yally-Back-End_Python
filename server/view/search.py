from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from server.controller.search import get_user_search_info


class GetUserSearch(Resource):

    @jwt_required
    def get(self):
        owner_email = get_jwt_identity()
        user_nickname = request.args['nickname']

        if not user_nickname:
            return abort(404, "no search word")

        return get_user_search_info(owner_email, user_nickname)
