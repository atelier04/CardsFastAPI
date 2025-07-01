from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relation

from dbconfig.config import Base
from models.mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(30), nullable=False)
    todos: list = relation("Todo", back_populates="user")
