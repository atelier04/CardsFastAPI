from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation

from models.mixins import Timestamp
from dbconfig.config import Base


class Todo(Timestamp, Base):
    __tablename__ = "meintodos"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(30), unique=True, nullable=False)
    description: str = Column(String(30), unique=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relation("User",cascade="all, delete", back_populates="todos")

    def __repr__(self):
        return f"{self.title=} {self.description=}"
