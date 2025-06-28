from sqlalchemy.orm import Session

from ..Models.All_models import ResidentialComplex
from ..Schemas.RC_schema import ResidentialComplexCreate


def create_residential_complex(db: Session, complex_data: ResidentialComplexCreate):
    db_complex = ResidentialComplex(
        name=complex_data.name,
        address=complex_data.address,
        developer_name=complex_data.developer_name,
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


def get_residential_complexes_by_developer(db: Session, developer_name: str, skip: int = 0, limit: int = 100):
    """Получить все жилые комплексы застройщика по имени застройщика"""
    return db.query(ResidentialComplex).filter(
        ResidentialComplex.developer_name == developer_name
    ).offset(skip).limit(limit).all()


def get_all_residential_complexes(db: Session, skip: int = 0, limit: int = 100):
    """Получить все жилые комплексы"""
    return db.query(ResidentialComplex).offset(skip).limit(limit).all()


def get_residential_complex_by_id(db: Session, complex_id: int):
    """Получить жилой комплекс по ID"""
    return db.query(ResidentialComplex).filter(ResidentialComplex.id == complex_id).first()