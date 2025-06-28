from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..Models.All_models import Property, Booking, User
from ..Schemas.Property_schema import PropertyModel, PropertySearch, BookingModel
from typing import List, Optional


def create_property(db: Session, property_data: PropertyModel) -> Property:
    db_property = Property(**property_data.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def get_properties(db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
    return db.query(Property).offset(skip).limit(limit).all()


def get_property(db: Session, property_id: int) -> Optional[Property]:
    return db.query(Property).filter(Property.id == property_id).first()


def search_properties(db: Session, search_params: PropertySearch) -> List[Property]:
    query = db.query(Property)
    
    if search_params.city:
        query = query.filter(Property.city.ilike(f"%{search_params.city}%"))
    
    if search_params.min_price is not None:
        query = query.filter(Property.price >= search_params.min_price)
    
    if search_params.max_price is not None:
        query = query.filter(Property.price <= search_params.max_price)
    
    if search_params.rooms is not None:
        query = query.filter(Property.rooms == search_params.rooms)
    
    if search_params.min_area is not None:
        query = query.filter(Property.area >= search_params.min_area)
    
    if search_params.max_area is not None:
        query = query.filter(Property.area <= search_params.max_area)
    
    if search_params.is_available is not None:
        query = query.filter(Property.is_available == search_params.is_available)
    
    return query.all()


def create_booking(db: Session, user_id: int, booking_data: BookingModel) -> Booking:
    # Проверяем, что недвижимость доступна
    property_obj = get_property(db, booking_data.property_id)
    if not property_obj or not property_obj.is_available:
        raise ValueError("Недвижимость недоступна для бронирования")
    
    # Проверяем, что у пользователя нет активной брони на эту недвижимость
    existing_booking = db.query(Booking).filter(
        and_(
            Booking.user_id == user_id,
            Booking.property_id == booking_data.property_id,
            Booking.status == "booked"
        )
    ).first()
    
    if existing_booking:
        raise ValueError("У вас уже есть активная бронь на эту недвижимость")
    
    db_booking = Booking(
        user_id=user_id,
        property_id=booking_data.property_id,
        status="booked"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_user_bookings(db: Session, user_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def cancel_booking(db: Session, booking_id: int, user_id: int) -> bool:
    booking = db.query(Booking).filter(
        and_(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == "booked"
        )
    ).first()
    
    if not booking:
        raise ValueError("Бронь не найдена или уже отменена")
    
    booking.status = "cancelled"
    db.commit()
    return True


def purchase_property(db: Session, booking_id: int, user_id: int) -> bool:
    booking = db.query(Booking).filter(
        and_(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == "booked"
        )
    ).first()
    
    if not booking:
        raise ValueError("Бронь не найдена")
    
    # Обновляем статус брони
    booking.status = "purchased"
    
    # Делаем недвижимость недоступной
    property_obj = get_property(db, booking.property_id)
    if property_obj:
        property_obj.is_available = False
    
    db.commit()
    return True


def update_user_profile(db: Session, user_id: int, name: str, phone: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Пользователь не найден")
    
    user.User_name = name
    user.Phone_number = phone
    db.commit()
    db.refresh(user)
    return user 