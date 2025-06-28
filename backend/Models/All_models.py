from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, false
from sqlalchemy.orm import relationship

from ..Database.DB_connection import base, engine


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


class Property(base):
    __tablename__ = "Properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    city = Column(String, nullable=False)
    is_available = Column(BOOLEAN, nullable=False, default=True)
    zastroy_id = Column(Integer, ForeignKey("Law_faces.id"), nullable=False)


class Booking(base):
    __tablename__ = "Bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    booking_date = Column(String, nullable=True)
    status = Column(String, nullable=False, default="booked")


class ResidentialComplex(base):
    __tablename__ = "residential_complexes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # Название
    address = Column(String, nullable=False)          # Адрес
    developer_name = Column(String, nullable=False)   # Имя застройщика
    city = Column(String, nullable=False)             # Город
    commissioning_date = Column(String, nullable=False)                 # Ввод в эксплуатацию (может быть NULL)
    housing_class = Column(String)                    # Класс (эконом, комфорт, бизнес)
    status = Column(String)                           # Статус дома (строится, сдан, планируется)
    avatar_url = Column(String)                       # Ссылка на аватар (может быть NULL)




base.metadata.create_all(engine)
# base.metadata.create_all(engine)