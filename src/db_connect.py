import os
import re
import logging
from src.color import color
from typing import Any
from psycopg2 import sql
import psycopg2
from dotenv import load_dotenv


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
    def conn(self) -> object:
        return self.__conn

    def close(self) -> None:
        self.__conn.close()

    def __init__(self) -> None:

        self.status: str = ""
        try:
            conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE_ADMIN, user=SQL_USER, password=SQL_PASS)
            self.__conn = conn
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
                psycopg2.sql.SQL("CREATE DATABASE {basedata} ENCODING 'UTF8' ").format(basedata=psycopg2.sql.Identifier(SQL_DATABASE))
            )
            cur.close()
            conn.close()

            try:
                conn = psycopg2.connect(host=SQL_HOST, database=SQL_DATABASE, user=SQL_USER, password=SQL_PASS)
            except Exception as e:
                logger_info.error(color("red", f"Error: Ошибка соединения с БД {e}"))
                quit()
            conn.autocommit = True
            cur = conn.cursor()

            with open('create_table.sql', 'r') as inserts:
                sql = inserts.read()

            cur.execute(sql)

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
            return []
        else:
            rows = cur.fetchall()
            self.status = "Ok"
            cur.close()
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
