from sqlalchemy import Column, String, ForeignKey

from server.model import Base


class Comment(Base):
    __tablename__ = 'comments'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(String(40), primary_key=True)
    content = Column(String(100), nullable=True)
    sound = Column(String(40), nullable=True)
    postId = Column(ForeignKey('posts.id', onupdate="cascade", ondelete="cascade"), nullable=False)
    userEmail = Column(ForeignKey('users.email', onupdate="cascade", ondelete="cascade"), nullable=False)