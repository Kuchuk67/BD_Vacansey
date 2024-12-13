from src.db_connect import DBConnect
from src.indastries import Industries
import logging
from src.color import color

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


class DBInsert(DBConnect):

    # def __init__(self):
    # super.__init__()

    def industries_insert(self, cur) -> None:
        # Заполнение БД industries
        industries = Industries()
        # print(industries.load())
        logger_info.info(color('white', industries.load()))

        cur.execute('delete FROM industries;')

        sql = "INSERT INTO industries VALUES "
        i, separate = 0, ""
        for key, value in Industries.dict_industries.items():
            sql = sql + f"{separate} ({key}, '{value}')"
            separate = ", "
        sql = sql + ";"
        cur.execute(sql)

    def vacancies_insert(self, cur):
        pass

    def company_insert(self, cur):
        pass

    def delete(self):
        "удаляет данные из таблиц"
        pass

    def reset(self):
        "удаляет полностью БД"
        pass
