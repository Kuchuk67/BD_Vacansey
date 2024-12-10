import psycopg2
import os
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")


def main():
    try:
        conn = psycopg2.connect(
            host=SQL_HOST,
            database=SQL_DATABASE,
            user=SQL_USER,
            password=SQL_PASS
        )

    except Exception as e:
         print(e)


        # print(conn)

    cursor = conn.cursor()
    conn.autocommit = True
    # команда для создания базы данных metanit
    sql = "CREATE DATABASE metanit"

    # выполняем код sql
    try:
        cursor.execute(sql)
    except Exception as er:
        print(er)
    print("База данных успешно создана")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
