import psycopg2
import os
from dotenv import load_dotenv
from typing import Any
import re

# Загрузка переменных из .env-файла
load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
SQL_DATABASE = re.sub("[^A-Za-z0-9]", "", os.getenv("SQL_DATABASE"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_DATABASE_ADMIN = re.sub("[^A-Za-z0-9]", "", os.getenv("SQL_DATABASE_ADMIN"))

import logging
#from config import LIST_COMPANY, WHITE, YELLOW, RESET_COLOR
from src.color import color

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)

class DBConnect:
    """ Соединение с Базой Данных. Проверка на наличие Бд и таблиц в ней"""

    def __init__(self) -> None:
        self.status = 'Ok'
        try:
            conn = psycopg2.connect(
                host=SQL_HOST,
                database=SQL_DATABASE_ADMIN,
                user=SQL_USER,
                password=SQL_PASS
            )
        except Exception as e:
            self.status = f'Error {e}'
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("SELECT datname  FROM pg_database WHERE datname = %s", (SQL_DATABASE,))
        except Exception as e:
            self.status = f'Error {e}'
        if not cur.fetchone():
            # если нет БД, то создадим
            cur.execute(f"CREATE DATABASE {SQL_DATABASE} ENCODING 'UTF8' "  )
            logger_info.info(color('white', "Создали БД") )
            #logger_info.info(WHITE + "Создали БД" + SQL_DATABASE + RESET_COLOR)

        cur.close()
        conn.close()
        try:
            conn = psycopg2.connect(
                host=SQL_HOST,
                database=SQL_DATABASE,
                user=SQL_USER,
                password=SQL_PASS
            )
        except Exception as e:
            self.status = f'Error {e}'
        cur = conn.cursor()
        try:
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        except Exception as e:
            self.status = f'Error {e}'
        rows = cur.fetchall()
        print(rows)

        if not ('company',) in rows:
            logger_info.info(color('white', "создается таблица company"))
            #logger_info.info(WHITE + "создается таблица company" + RESET_COLOR)
        if not ('vacancies',) in rows:
            logger_info.info(color('white', "создается таблица vacancies"))
            #logger_info.info(WHITE + "создается таблица vacancies" + RESET_COLOR)
        if not ('industries',) in rows:
            logger_info.info(color('white', "создается таблица industries"))
            #logger_info.info(WHITE + "создается таблица industries" + RESET_COLOR)


        self.__connect = conn
        self.status = 'Ok'


    @property
    def connect(self):
        return self.__connect


