from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:testen@localhost/shop"
                       ,future=True)
Session = sessionmaker(bind=engine, future=True)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_session():
    session= Session()
    try:
        yield session
    finally:
        session.close()
