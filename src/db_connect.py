import psycopg2
import os
from dotenv import load_dotenv
from typing import Any

# Загрузка переменных из .env-файла
load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")

class DBConnect:
    """ Соединение с Базой Данных. Проверка на наличие Бд и таблиц в ней"""

    def __init__(self) -> None:

        try:
            connect = psycopg2.connect(
                host=SQL_HOST,
                database=SQL_DATABASE,
                user=SQL_USER,
                password=SQL_PASS
            )

        except Exception as e:
            print(e)
            self.__connect = None
        else:
            self.__connect = connect


    @property
    def connect(self):
        return self.__connect


    cursor = connect.cursor()
    connect.autocommit = True
    # команда для создания базы данных
    sql = "CREATE DATABASE metanit"

    # выполняем код sql
    try:
        cursor.execute(sql)
    except Exception as er:
        print(er)
    print("База данных успешно создана")

    cursor.close()
    conn.close()