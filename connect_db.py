
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base


# URI: postgresql://username:password@domain:port/database

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
db = config.get('DEV_DB', 'DB_NAME')


class Base(DeclarativeBase):
    pass

# Base = declarative_base()

# DB_URL = "postgresql://postgres:0000@localhost/test"
DB_URL = f"postgresql://{user}:{password}@{domain}:{port}/{db}"

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)
session = Session()