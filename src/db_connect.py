import os
import re
import logging
from src.color import color
# from abc import ABC, abstractmethod
from typing import Any
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

# Загрузка переменных из .env-файла
load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
SQL_DATABASE = re.sub("[^A-Za-z0-9]", "", str(os.getenv("SQL_DATABASE")))
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_DATABASE_ADMIN = re.sub("[^A-Za-z0-9]", "", str(os.getenv("SQL_DATABASE_ADMIN")))

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


class DBConnect:
    """Соединение с Базой Данных.
    Проверка на наличие Бд и таблиц в ней
    """

    def connect(self) -> None:
        """Устанавливает соединение с БД"""
        try:
            self.__conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASS)
        except Exception as e:
            logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
            quit()

    @property
    def conn(self):
        return self.__conn


    def close(self):
        self.__conn.close()

    def __init__(self) -> None:
        self.__conn: Any = None
        self.status: str = ""
        try:
            conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE_ADMIN, user=SQL_USER, password=SQL_PASS)
        except Exception as e:
            logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
            quit()
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("SELECT datname  FROM pg_database WHERE datname = %s", (SQL_DATABASE,))
        except Exception as e:
            self.status = f"Error {e}"

        if not cur.fetchone():
            # если нет БД, то создадим БД и таблицы

            cur.execute(
                sql.SQL("CREATE DATABASE {basedata} ENCODING 'UTF8' ").format(basedata=sql.Identifier(SQL_DATABASE)))
            cur.close()
            conn.close()

            try:
                conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASS)
            except Exception as e:
                logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
                quit()
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("""CREATE TABLE industries (
                                industries_id character(10) PRIMARY KEY,
                                industries_name varchar(255) NOT NULL
                                );
                            CREATE TABLE company ( 
                                company_id int PRIMARY KEY, 
                                name varchar(255) NOT NULL, 
                                site_url varchar(255), 
                                industries character(10), 
                                FOREIGN KEY (industries) REFERENCES industries(industries_id) 
                                );
                            CREATE TABLE vacancies (
                                vacancies_id int PRIMARY KEY,
                                vacancies_name varchar(255),
                                salary_from int,
                                salary_to int,
                                salary_avg int,
                                address varchar(255),
                                snippet varchar(255),
                                responsibility varchar(255),
                                schedule varchar(80),
                                company_id int REFERENCES company(company_id) NOT NULL
                                );""")

            cur.close()
            conn.close()



    def select_(self, sql_txt: str) -> Any:
        """Соединяется с БД и
        отправляет SQL запрос.
        Возвращает список строк или пустой список
        Записывает статус ответа в DBConnect.status"""
        list_word_sql = sql_txt.split(" ")
        if list_word_sql[0] != "SELECT":
            self.status = "Error Неверный формат запроса"
            logger_info.error(color("red", "Error Неверный формат запроса"))
            return []
        # .connect с БД
        # conn = DBConnect.connect()
        cur = self.__conn.cursor()
        try:
            cur.execute(sql_txt)
        except Exception:
            self.status = "Error"
            cur.close()
            # conn.close()
            return []
        else:
            rows = cur.fetchall()
            self.status = "Ok"
            cur.close()
            # conn.close()
            return rows


    def drop_all(self) -> None:
        """удаляет полностью БД"""
        self.__conn.close()  # закрываем соединение
        try:
            conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE_ADMIN, user=SQL_USER, password=SQL_PASS)
        except Exception as e:
            logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
            quit()
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("""DROP DATABASE  %s""" % (SQL_DATABASE,))
        except Exception as e:
            # DBConnect.status = f"Error {e}"
            logger_info.error(color("red", f"Error: Ошибка удаления БД {e}"))
        else:
            print("БД удалена. Работа приложения завершена.")
            quit()

        cur.close()
        conn.close()
