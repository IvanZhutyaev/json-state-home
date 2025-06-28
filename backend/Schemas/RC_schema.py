from typing import Optional
from pydantic import BaseModel


class ResidentialComplexCreate(BaseModel):
    name: str                      # Название (обязательное)
    address: str                   # Адрес (обязательное)
    developer_name: str            # Имя застройщика (обязательное)
    city: str                      # Город (обязательное)
    commissioning_date: Optional[str] = None  # Ввод в эксплуатацию (необязательное)
    housing_class: Optional[str] = None        # Класс (необязательное)
    status: Optional[str] = None               # Статус (необязательное)
    avatar_url: Optional[str] = None           # Ссылка на аватар (необязательное)
    
    class Config:
        from_attributes = True  # Работает с ORM (для FastAPI >= 2.0)