from sqlalchemy.orm import Session
from Database.DB_connection import SessionLocal, engine
from Models.All_models import User, Law_Face, Property, Booking
from Cruds.User_crud import create_user
from Cruds.Law_crud import create_zastroy
from Cruds.Property_crud import create_property
from Schemas.User_schema import UserModel
from Schemas.Zastroy_schema import ZastroyModel
from Schemas.Property_schema import PropertyModel


def seed_database():
    db = SessionLocal()
    try:
        # Создаем тестовых пользователей
        test_users = [
            UserModel(
                User_name="Иван Иванов",
                Phone_number="+79991234567",
                password="password123"
            ),
            UserModel(
                User_name="Мария Петрова",
                Phone_number="+79987654321",
                password="password123"
            )
        ]
        
        created_users = []
        for user_data in test_users:
            try:
                user = create_user(db, user_data)
                created_users.append(user)
                print(f"Создан пользователь: {user.User_name}")
            except Exception as e:
                print(f"Ошибка создания пользователя: {e}")
        
        # Создаем тестовых застройщиков
        test_zastroys = [
            ZastroyModel(
                Company_name="ООО 'Солнечный Дом'",
                INN=1234567890,
                OGRN=1234567890123,
                Adress="г. Москва, ул. Солнечная, 15",
                User_name="admin_sun",
                password="password123"
            ),
            ZastroyModel(
                Company_name="ООО 'Парковый Квартал'",
                INN=9876543210,
                OGRN=9876543210987,
                Adress="г. Москва, ул. Парковая, 8",
                User_name="admin_park",
                password="password123"
            )
        ]
        
        created_zastroys = []
        for zastroy_data in test_zastroys:
            try:
                zastroy = create_zastroy(db, zastroy_data)
                created_zastroys.append(zastroy)
                print(f"Создан застройщик: {zastroy.Company_name}")
            except Exception as e:
                print(f"Ошибка создания застройщика: {e}")
        
        # Создаем тестовую недвижимость
        test_properties = [
            PropertyModel(
                name="ЖК 'Солнечный', кв. 45",
                address="г. Москва, ул. Солнечная, 15",
                price=3200000.0,
                description="Уютная квартира с видом на парк",
                image_url="https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК+Солнечный",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[0].id if created_zastroys else 1
            ),
            PropertyModel(
                name="ЖК 'Парковый', кв. 78",
                address="г. Москва, ул. Парковая, 8",
                price=4100000.0,
                description="Просторная квартира в тихом районе",
                image_url="https://via.placeholder.com/300x200/34c759/ffffff?text=ЖК+Парковый",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1
            ),
            PropertyModel(
                name="ЖК 'Речной', кв. 23",
                address="г. Москва, наб. Речная, 12",
                price=6800000.0,
                description="Элитная квартира с видом на реку",
                image_url="https://via.placeholder.com/300x200/ff9500/ffffff?text=ЖК+Речной",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[0].id if created_zastroys else 1
            ),
            PropertyModel(
                name="ЖК 'Лесной', кв. 12",
                address="г. Москва, ул. Лесная, 25",
                price=2800000.0,
                description="Компактная квартира для молодой семьи",
                image_url="https://via.placeholder.com/300x200/5856d6/ffffff?text=ЖК+Лесной",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1
            )
        ]
        
        created_properties = []
        for property_data in test_properties:
            try:
                property_obj = create_property(db, property_data)
                created_properties.append(property_obj)
                print(f"Создана недвижимость: {property_obj.name}")
            except Exception as e:
                print(f"Ошибка создания недвижимости: {e}")
        
        # Создаем тестовые брони
        if created_users and created_properties:
            from Cruds.Property_crud import create_booking
            from Schemas.Property_schema import BookingModel
            
            test_booking = BookingModel(property_id=created_properties[0].id)
            try:
                booking = create_booking(db, created_users[0].id, test_booking)
                print(f"Создана бронь для пользователя {created_users[0].User_name}")
            except Exception as e:
                print(f"Ошибка создания брони: {e}")
        
        print("База данных успешно заполнена тестовыми данными!")
        
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database() 