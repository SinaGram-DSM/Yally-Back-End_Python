import redis

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

Redis = redis.Redis(host='localhost', port=6379, db=0)