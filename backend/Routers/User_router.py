from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from starlette import status

# from Cruds.Law_crud import check_zastroy_credentials
from ..Schemas.User_schema import UserModel, UserResponse, UserLogin
# from Cruds.User_crud import (
#     create_user,
#     get_user,
#     get_users,
#     update_user,
#     delete_user, check_user_credentials
# )
# from Database.DB_connection import get_db
from ..Schemas.Zastroy_schema import ZastroyLogin

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserModel):
    # db: Session = Depends(get_db)
    try:
        # return create_user(db, user)
        return {"message": "Пользователь зарегистрирован (режим без БД)"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def user_login(credentials: UserLogin):
    # db: Session = Depends(get_db)
    # if check_user_credentials(db, credentials.phone, credentials.password):
    #     return {"status": "success", "message": "Аутентификация прошла успешно"}
    return {"status": "success", "message": "Аутентификация прошла успешно (режим без БД)"}

    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Неверный Телефон или пароль"
    # )

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    # db: Session = Depends(get_db)
    # return get_users(db, skip=skip, limit=limit)
    return [{"message": "Список пользователей (режим без БД)"}]

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    # db: Session = Depends(get_db)
    # db_user = get_user(db, user_id)
    # if not db_user:
    #     raise HTTPException(status_code=404, detail="Пользователь не найден")
    # return db_user
    return {"message": f"Пользователь {user_id} (режим без БД)"}

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserModel):
    # db: Session = Depends(get_db)
    try:
        # return update_user(db, user_id, user)
        return {"message": f"Пользователь {user_id} обновлен (режим без БД)"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def remove_user(user_id: int):
    # db: Session = Depends(get_db)
    try:
        # return delete_user(db, user_id)
        return {"message": f"Пользователь {user_id} удален (режим без БД)"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))