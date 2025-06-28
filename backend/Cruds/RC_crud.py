from sqlalchemy.orm import Session

from backend.Models.All_models import ResidentialComplex
from backend.Schemas.RC_schema import ResidentialComplexCreate


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