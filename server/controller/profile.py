from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from server.model import session
from server.model.user import User
from server.model.post import Post
from server.model.yally import Yally
from server.model.comment import Comment


# 무한 스크롤시 중복 post 처리는 복잡해서 아직 안함
def get_profile_timeline(user_email, profile_user_email, page):
    limit = 7

    try:
        user = session.query(User).filter(User.email == profile_user_email).first()
    except SQLAlchemyError:
        return abort(418, "db_error")

    page = (page - 1) * limit

    if user is None:
        return abort(404, "User not Found")

    try:
        posts = session.query(Post) \
                   .filter(Post.userEmail == profile_user_email) \
                   .order_by(Post.createdAt.desc()) \
                   .all()[page:page + limit]
    except SQLAlchemyError:
        return abort(418, "db_error")

    return {
        "posts": [{
            "id": post.id,
            "user": {
                "email": user.email,
                "nickname": user.nickname,
                "img": user.img
            },
            "content": post.content,
            "sound": post.sound,
            "img": post.img,
            "yally": session.query(Yally).filter(Yally.postId == post.id).count(),
            "comment": session.query(Comment).filter(Comment.postId == post.id).count(),
            "isYally": True if session.query(Yally).filter(Yally.userEmail == user_email).filter(Yally.postId == post.id).first() else False,
            "createdAt": str(post.createdAt)
        }for post in posts]
    }
