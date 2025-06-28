from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..Models.All_models import ResidentialComplex
from ..Schemas.RC_schema import ResidentialComplexCreate


def create_residential_complex(db: Session, complex_data: ResidentialComplexCreate):
    db_complex = ResidentialComplex(
        name=complex_data.name,
        address=complex_data.address,
        developer_name=complex_data.developer_name,
        zastroy_id=complex_data.zastroy_id,
        city=complex_data.city,
        commissioning_date=complex_data.commissioning_date,
        housing_class=complex_data.housing_class,
        status=complex_data.status,
        avatar_url=complex_data.avatar_url
    )
    db.add(db_complex)
    db.commit()
    db.refresh(db_complex)
    return db_complex


def get_residential_complexes_by_zastroy_id(db: Session, zastroy_id: int, skip: int = 0, limit: int = 100):
    """Получить все жилые комплексы застройщика по ID застройщика"""
    return db.query(ResidentialComplex).filter(
        ResidentialComplex.zastroy_id == zastroy_id
    ).offset(skip).limit(limit).all()


def get_residential_complexes_by_developer(db: Session, developer_name: str, skip: int = 0, limit: int = 100):
    """Получить все жилые комплексы застройщика по имени застройщика"""
    return db.query(ResidentialComplex).filter(
        ResidentialComplex.developer_name == developer_name
    ).offset(skip).limit(limit).all()


def get_all_residential_complexes(db: Session, skip: int = 0, limit: int = 100):
    """Получить все жилые комплексы"""
    return db.query(ResidentialComplex).offset(skip).limit(limit).all()


def get_residential_complex(db: Session, complex_id: int):
    """Получить жилой комплекс по ID"""
    return db.query(ResidentialComplex).filter(ResidentialComplex.id == complex_id).first()


def rate_residential_complex(db: Session, complex_id: int, rating: float) -> bool:
    """Оценить ЖК"""
    complex_obj = get_residential_complex(db, complex_id)
    if not complex_obj:
        raise ValueError("Жилой комплекс не найден")
    
    if rating < 1.0 or rating > 5.0:
        raise ValueError("Рейтинг должен быть от 1 до 5")
    
    # Обновляем рейтинг
    if complex_obj.rating is None:
        complex_obj.rating = rating
        complex_obj.rating_count = 1
    else:
        total_rating = complex_obj.rating * complex_obj.rating_count + rating
        complex_obj.rating_count += 1
        complex_obj.rating = total_rating / complex_obj.rating_count
    
    db.commit()
    return True