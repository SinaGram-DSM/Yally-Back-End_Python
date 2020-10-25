from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import abort
from server.controller.profile import get_profile_timeline


class GetProfileTimeline(Resource):

    @jwt_required
    def get(self, email, page):
        user_email = get_jwt_identity()

        if not page.isdigit():
            return abort(400, "Check you json key name and value type")

        return get_profile_timeline(user_email, email, int(page))


