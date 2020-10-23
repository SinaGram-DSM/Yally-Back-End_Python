from sqlalchemy import Column, String, ForeignKey

from server.model import Base


class Yally(Base):
    __tablename__ = 'yallies'
    __table_args__ = {'useexisting': True}

    userEmail = Column(ForeignKey('users.email', onupdate="cascade", ondelete="cascade"), primary_key=True)
    postId = Column(ForeignKey('posts.id', onupdate="cascade", ondelete="cascade"), primary_key=True)
