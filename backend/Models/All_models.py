from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, false
from sqlalchemy.dialects.mysql import NUMERIC
from sqlalchemy.orm import relationship

from backend.Database.DB_connection import base, engine


class Law_Face(base):
    __tablename__="Law_faces"
    id = Column(Integer,primary_key=True, index=True)
    Company_name = Column(String, nullable=False)
    INN=Column(Integer, unique=True)
    OGRN=Column(Integer, unique=True)
    Adress=Column(String, nullable=False)
    User_name=Column(String, nullable=False)
    password=Column(String, nullable=False)
    IsVerified=Column(BOOLEAN, nullable=False, default=True)


class User(base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    User_name=Column(String, nullable=False, default="undified")
    Phone_number=Column(String, nullable=False)
    password = Column(String, nullable=False)



base.metadata.create_all(engine)