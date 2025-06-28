import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.DB_connection import engine, base
from Models.All_models import *

def recreate_tables():
    """Пересоздает все таблицы в базе данных"""
    try:
        print("Удаление существующих таблиц...")
        base.metadata.drop_all(engine)
        print("Создание новых таблиц...")
        base.metadata.create_all(engine)
        print("Таблицы успешно пересозданы!")
    except Exception as e:
        print(f"Ошибка при пересоздании таблиц: {e}")
        print(f"Тип ошибки: {type(e)}")

if __name__ == "__main__":
    recreate_tables() 