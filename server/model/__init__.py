import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server import DATABASE_URL
engine = create_engine(DATABASE_URL, encoding="utf-8", pool_size=20,
                       pool_recycle=500, max_overflow=20)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)