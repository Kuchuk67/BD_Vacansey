import psycopg2
import os
from dotenv import load_dotenv
from typing import  Any
import re
from abc import ABC,abstractmethod


# Загрузка переменных из .env-файла
load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
SQL_DATABASE = re.sub("[^A-Za-z0-9]", "", os.getenv("SQL_DATABASE"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_DATABASE_ADMIN = re.sub("[^A-Za-z0-9]", "", os.getenv("SQL_DATABASE_ADMIN"))

import logging
from src.color import color

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)

class DBConnect():
    """ Соединение с Базой Данных.
    Проверка на наличие Бд и таблиц в ней
    """

    @staticmethod
    def connect() -> Any:
        try:
            conn = psycopg2.connect(
                host=SQL_HOST,
                database=SQL_DATABASE,
                user=SQL_USER,
                password=SQL_PASS
            )
        except Exception as e:
            logger_info.error(color('red', f"Error: Ошибка соединения с БД {e}" ))
            quit()
        return conn


    def __init__(self) -> None:
        DBConnect.status = 'Ok'
        self.__cur = None
        try:
            conn = psycopg2.connect(
                host=SQL_HOST,
                database=SQL_DATABASE_ADMIN,
                user=SQL_USER,
                password=SQL_PASS
            )
        except Exception as e:
            logger_info.error(color('red', f"Error: Ошибка соединения с БД {e}" ))
            quit()
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute("SELECT datname  FROM pg_database WHERE datname = %s", (SQL_DATABASE,))
        except Exception as e:
            DBConnect.status = f'Error {e}'
        if not cur.fetchone():
            # если нет БД, то создадим
            cur.execute(f"CREATE DATABASE {SQL_DATABASE} ENCODING 'UTF8' ")
            logger_info.info(color('white', "Создали БД"))


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
            DBConnect.status = f'Error {e}'
        rows = cur.fetchall()
        # Проверяем есть ли таблицы в БД, если нет - создаем
        if not ('company',) in rows:
            logger_info.info(color('white', "создается таблица company"))
            try:
                cur.execute("CREATE TABLE company ( "
                            "company_id int PRIMARY KEY, "
                            "name varchar(255) NOT NULL, "
                            "site_url varchar(255), "
                            "description text, "
                            "industries character(10), "
                            "FOREIGN KEY (industries) REFERENCES industries(industries_id) "
                            ");")
            except Exception as e:
                DBConnect.status = f'Error {e}'
                logger_info.error(color('red', "Error CREATE TABLE company"))
            else:
                DBConnect.status = 'Ok'
                logger_info.info(color('white', "Ok"))
        if not ('vacancies',) in rows:
            logger_info.info(color('white', "создается таблица vacancies"))
            try:
                cur.execute("""CREATE TABLE vacancies ( vacancies_id serial PRIMARY KEY,
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
            except Exception as e:
                DBConnect.status = f'Error {e}'
                logger_info.error(color('red', "Error CREATE TABLE vacancies"))
            else:
                DBConnect.status = 'Ok'
                logger_info.info(color('white', "Ok"))

        if not ('industries',) in rows:
            logger_info.info(color('white', "создается таблица industries"))
            try:
                cur.execute("""CREATE TABLE industries (
                industries_id character(10) PRIMARY KEY, 
                industries_name varchar(255) NOT NULL
                );""")

            except Exception as e:
                DBConnect.status = f'Error {e}'
                logger_info.error(color('red', "Error CREATE TABLE industries"))
            else:
                DBConnect.status = 'Ok'
                logger_info.info(color('white', "Ok"))
                # загрузить таблицу данными
                # DBConnect.industries_insert(conn, cur)
        cur.close()
        conn.close()

        DBConnect.status = 'Ok'

    @staticmethod
    def select_(sql_txt: str) -> list:
        """ Соединяется с БД и
        отправляет SQL запрос.
        Возвращает список строк или пустой список
        Записывает статус ответа в DBConnect.status"""
        list_word_sql = sql_txt.split(' ')
        if list_word_sql[0] != 'SELECT':
            DBConnect.status = 'Error Неверный формат запроса'
            logger_info.error(color('red', 'Error Неверный формат запроса'))
            return []
        # .connect с БД
        conn = DBConnect.connect()
        cur = conn.cursor()
        try:
            cur.execute(sql_txt)
        except Exception:
            DBConnect.status = 'Error'
            cur.close()
            conn.close()
            return []
        else:
            rows = cur.fetchall()
            DBConnect.status = 'Ok'
            cur.close()
            conn.close()
            return rows





