from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, false, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

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
    
    # Связи
    properties = relationship("Property", back_populates="zastroy")
    residential_complexes = relationship("ResidentialComplex", back_populates="zastroy")


class User(base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    User_name=Column(String, nullable=False, default="undified")
    Phone_number=Column(String, nullable=False, default="undified")
    Email=Column(String, nullable=False, default="undified")
    password=Column(String, nullable=False, default="undified")
    IsVerified=Column(BOOLEAN, nullable=False, default=True)
    
    # Связи
    bookings = relationship("Booking", back_populates="user")


class Property(base):
    __tablename__ = "Properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    city = Column(String, nullable=False)
    is_available = Column(BOOLEAN, nullable=False, default=True)
    zastroy_id = Column(Integer, ForeignKey("Law_faces.id"), nullable=False)
    complex_id = Column(Integer, ForeignKey("residential_complexes.id"), nullable=True)  # ЖК
    area = Column(Integer, nullable=True)  # Площадь в м²
    rooms = Column(Integer, nullable=True)  # Количество комнат
    floor = Column(Integer, nullable=True)  # Этаж
    
    # Связи
    zastroy = relationship("Law_Face", back_populates="properties")
    complex = relationship("ResidentialComplex", back_populates="properties")
    events = relationship("ApartmentEvent", back_populates="property")
    bookings = relationship("Booking", back_populates="property")


class Booking(base):
    __tablename__ = "Bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default="booked")
    
    # Связи
    user = relationship("User", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")


class ResidentialComplex(base):
    __tablename__ = "residential_complexes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # Название
    address = Column(String, nullable=False)          # Адрес
    developer_name = Column(String, nullable=False)   # Имя застройщика
    zastroy_id = Column(Integer, ForeignKey("Law_faces.id"), nullable=False)  # ID застройщика
    city = Column(String, nullable=False)             # Город
    commissioning_date = Column(String, nullable=False)                 # Ввод в эксплуатацию (может быть NULL)
    housing_class = Column(String)                    # Класс (эконом, комфорт, бизнес)
    status = Column(String)                           # Статус дома (строится, сдан, планируется)
    avatar_url = Column(String)                       # Ссылка на аватар
    
    # Связи
    zastroy = relationship("Law_Face", back_populates="residential_complexes")
    properties = relationship("Property", back_populates="complex")


class ApartmentEvent(base):
    __tablename__ = "apartment_events"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    user_id = Column(String(255), nullable=False)  # Обычная строка для ID пользователя
    event_type = Column(String(100), nullable=False)  # Тип события (click_3d_tour, click_book, time_on_page, etc.)
    event_value = Column(Float, nullable=True)  # Значение события (например, время на странице)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Связь с объектом недвижимости
    property = relationship("Property", back_populates="events")


base.metadata.create_all(engine)