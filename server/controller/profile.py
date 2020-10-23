from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from server.model import session
from server.model.user import User
from server.model.post import Post
from server.model.yally import Yally
from server.model.comment import Comment
from server import S3_URL


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
        post = session.query(Post) \
                   .filter(Post.userEmail == profile_user_email) \
                   .order_by(Post.createdAt.desc()) \
                   .all()[page:page + limit]
    except SQLAlchemyError:
        return abort(418, "db_error")

    posts = []
    if post:
        for i in range(len(post)):
            try:
                posts.append({
                    "content": post[i].content,
                    "sound": f"{S3_URL}{post[i].sound}",
                    "yallyCount": session.query(Yally).filter(Yally.postId == post[i].id).count(),
                    "commentCount": session.query(Comment).filter(Comment.postId == post[i].id).count(),
                    "isYally": True if session.query(Yally).filter(Yally.userEmail == user_email).filter(Yally.postId == post[i].id).first() else False,
                    "createdAt": str(post[i].createdAt)
                })
            except SQLAlchemyError:
                return abort(418, "db_error")

    return {
        "posts": posts
    }
