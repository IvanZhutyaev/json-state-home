from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..Schemas.Zastroy_schema import ZastroyModel, ZastroyResponse, ZastroyLogin
from ..Cruds.Law_crud import (
    create_zastroy,
    get_zastroy,
    get_zastroys,
    update_zastroy,
    delete_zastroy, 
    check_zastroy_credentials
)
from ..Database.DB_connection import get_db

router = APIRouter(prefix="/zastroys", tags=["Застройщики"])

@router.post("/", response_model=ZastroyResponse)
def create_new_zastroy(zastroy: ZastroyModel, db: Session = Depends(get_db)):
    try:
        return create_zastroy(db, zastroy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def zastroy_login(credentials: ZastroyLogin, db: Session = Depends(get_db)):
    if check_zastroy_credentials(db, credentials.inn, credentials.password):
        return {"status": "success", "message": "Аутентификация прошла успешно"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный ИНН или пароль"
    )

@router.get("/", response_model=list[ZastroyResponse])
def read_zastroys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_zastroys(db, skip=skip, limit=limit)

@router.get("/{zastroy_id}", response_model=ZastroyResponse)
def read_zastroy(zastroy_id: int, db: Session = Depends(get_db)):
    db_zastroy = get_zastroy(db, zastroy_id)
    if not db_zastroy:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    return db_zastroy

@router.put("/{zastroy_id}", response_model=ZastroyResponse)
def update_existing_zastroy(zastroy_id: int, zastroy: ZastroyModel, db: Session = Depends(get_db)):
    try:
        return update_zastroy(db, zastroy_id, zastroy)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{zastroy_id}")
def remove_zastroy(zastroy_id: int, db: Session = Depends(get_db)):
    try:
        return delete_zastroy(db, zastroy_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))