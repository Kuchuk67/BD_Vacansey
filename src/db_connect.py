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

    status: str = ""

    @staticmethod
    def connect() -> Any:
        """Устанавливает соединение с БД"""
        try:
            conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASS)
        except Exception as e:
            logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
            quit()
        return conn

    def __init__(self) -> None:
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
            DBConnect.status = f"Error {e}"
        if not cur.fetchone():
            # если нет БД, то создадим
            cur.execute(sql.SQL("CREATE DATABASE {basedata} ENCODING 'UTF8' ").format(basedata=sql.Identifier(SQL_DATABASE)))
            logger_info.info(color("grey", "Создали БД"))

        cur.close()
        conn.close()

        # .connect с БД
        conn = DBConnect.connect()
        # Загружаем названия таблиц из БД
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        except Exception as e:
            DBConnect.status = f"Error {e}"
        rows = cur.fetchall()
        # Проверяем есть ли таблицы в БД, если нет - создаем

        if not ("industries",) in rows:
            logger_info.info(color("grey", "создается таблица industries"))
            try:
                cur.execute(
                    """CREATE TABLE industries (
                industries_id character(10) PRIMARY KEY,
                industries_name varchar(255) NOT NULL
                );"""
                )
            except Exception as e:
                DBConnect.status = f"Error {e}"
                logger_info.error(color("red", "Error CREATE TABLE industries"))
            else:
                DBConnect.status = "Ok"
                logger_info.info(color("green", "Ok"))
                # загрузить таблицу данными
                # DBConnect.industries_insert(conn, cur)

        if not ("company",) in rows:
            logger_info.info(color("grey", "создается таблица company"))
            try:
                cur.execute(
                    "CREATE TABLE company ( "
                    "company_id int PRIMARY KEY, "
                    "name varchar(255) NOT NULL, "
                    "site_url varchar(255), "
                    "industries character(10), "
                    "FOREIGN KEY (industries) REFERENCES industries(industries_id) "
                    ");"
                )
            except Exception as e:
                DBConnect.status = f"Error {e}"
                logger_info.error(color("red", "Error CREATE TABLE company"))
            else:
                DBConnect.status = "Ok"
                logger_info.info(color("green", "Ok"))

        if not ("vacancies",) in rows:
            logger_info.info(color("grey", "создается таблица vacancies"))
            try:
                cur.execute(
                    """CREATE TABLE vacancies ( number_id serial PRIMARY KEY,
vacancies_id int,
vacancies_name varchar(255),
salary_from int,
salary_to int,
salary_avg int,
address varchar(255),
snippet varchar(255),
responsibility varchar(255),
schedule varchar(80),
company_id int REFERENCES company(company_id) NOT NULL
);"""
                )
            except Exception as e:
                DBConnect.status = f"Error {e}"
                logger_info.error(color("red", "Error CREATE TABLE vacancies"))
            else:
                DBConnect.status = "Ok"
                logger_info.info(color("green", "Ok"))

        cur.close()
        conn.close()

        DBConnect.status = "Ok"

    @staticmethod
    def select_(sql_txt: str) -> Any:
        """Соединяется с БД и
        отправляет SQL запрос.
        Возвращает список строк или пустой список
        Записывает статус ответа в DBConnect.status"""
        list_word_sql = sql_txt.split(" ")
        if list_word_sql[0] != "SELECT":
            DBConnect.status = "Error Неверный формат запроса"
            logger_info.error(color("red", "Error Неверный формат запроса"))
            return []
        # .connect с БД
        conn = DBConnect.connect()
        cur = conn.cursor()
        try:
            cur.execute(sql_txt)
        except Exception:
            DBConnect.status = "Error"
            cur.close()
            conn.close()
            return []
        else:
            rows = cur.fetchall()
            DBConnect.status = "Ok"
            cur.close()
            conn.close()
            return rows

    @staticmethod
    def drop_all() -> None:
        """удаляет полностью БД"""

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
            DBConnect.status = f"Error {e}"
            logger_info.error(color("red", f"Error: Ошибка удаления БД {e}"))
        else:
            print("БД удалена. Работа приложения завершена.")
            quit()

        cur.close()
        conn.close()
