from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..Schemas.Property_schema import (
    PropertyModel, 
    PropertyResponse, 
    PropertySearch, 
    BookingModel, 
    BookingResponse
)
from ..Cruds.Property_crud import (
    create_property,
    get_properties,
    get_property,
    search_properties,
    create_booking,
    get_user_bookings,
    cancel_booking,
    purchase_property,
    update_user_profile
)
from ..Database.DB_connection import get_db

router = APIRouter(prefix="/properties", tags=["Недвижимость"])


@router.get("/", response_model=List[PropertyResponse])
def read_properties(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Получить список всей недвижимости"""
    return get_properties(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[PropertyResponse])
def search_properties_endpoint(
    city: Optional[str] = Query(None, description="Город"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    is_available: Optional[bool] = Query(True, description="Доступность"),
    db: Session = Depends(get_db)
):
    """Поиск недвижимости по параметрам"""
    search_params = PropertySearch(
        city=city,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available
    )
    return search_properties(db, search_params)


@router.get("/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретной недвижимости"""
    db_property = get_property(db, property_id)
    if not db_property:
        raise HTTPException(status_code=404, detail="Недвижимость не найдена")
    return db_property


@router.post("/", response_model=PropertyResponse)
def create_new_property(property_data: PropertyModel, db: Session = Depends(get_db)):
    """Создать новую недвижимость (для застройщиков)"""
    try:
        return create_property(db, property_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Роуты для бронирований
@router.post("/book", response_model=BookingResponse)
def book_property(
    booking_data: BookingModel,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Забронировать недвижимость"""
    try:
        return create_booking(db, user_id, booking_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bookings/{user_id}", response_model=List[BookingResponse])
def get_bookings(user_id: int, db: Session = Depends(get_db)):
    """Получить все брони пользователя"""
    return get_user_bookings(db, user_id)


@router.post("/bookings/{booking_id}/cancel")
def cancel_booking_endpoint(
    booking_id: int,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Отменить бронь"""
    try:
        cancel_booking(db, booking_id, user_id)
        return {"message": "Бронь успешно отменена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bookings/{booking_id}/purchase")
def purchase_property_endpoint(
    booking_id: int,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Купить забронированную недвижимость"""
    try:
        purchase_property(db, booking_id, user_id)
        return {"message": "Недвижимость успешно куплена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 