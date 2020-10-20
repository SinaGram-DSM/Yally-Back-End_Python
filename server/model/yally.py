from sqlalchemy import Column, String, ForeignKey

from server.model import Base


class Yally(Base):
    __tablename__ = 'yallies'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    userEmail = Column(ForeignKey('users.email', onupdate="cascade", ondelete="cascade"), nullable=False)
    postId = Column(ForeignKey('posts.id', onupdate="cascade", ondelete="cascade"), nullable=False)
