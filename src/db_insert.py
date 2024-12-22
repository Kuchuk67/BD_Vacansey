import logging
from typing import Any
from src.color import color
from src.db_connect import DBConnect
from src.indastries import Industries

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


class DBInsert:
    """Подключается к БД
    Содержит методы для записи данных в таблицы"""
    def __init__(self):
        connect = DBConnect()
        self.connect =  DBConnect.connect()

    def industries_insert(self, cur: Any) -> None:
        """Заполнение БД industries"""

        DBConnect.status = "Ok"
        # Загрузка API отраслей промышленности
        industries = Industries()
        industries_load = industries.load()
        logger_info.info(color("green", industries_load))

        # Заполнение БД industries
        args_str = ','.join(cur.mogrify("(%s,%s)", x).decode('utf-8') for x in Industries.dict_industries)
        cur.execute("INSERT INTO industries (industries_id, industries_name) VALUES " + args_str)


    def company_insert(self, cur: Any, list_companies: list) -> None:
        """Заполнение БД company"""
        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in list_companies)
        cur.execute("INSERT INTO company VALUES " + args_str)


    def vacancies_insert(self, cur: Any, vacancies: list, company_id: int) -> None:
        """Заполнение БД vacancies"""
        # Код для проверки того, что записывается в базу вакансии

        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in vacancies)
        cur.execute("INSERT INTO vacancies VALUES " + args_str)

        f = open(str(company_id), 'w', encoding='utf-8')
        f.write(args_str)
        f.close()



    def remove_db(self) -> None:
        """удаляет данные из таблиц.  """

        # .connect с БД
        conn = DBConnect.connect()
        cur = conn.cursor()
        try:
            sql_txt = "delete FROM vacancies; delete FROM company; delete FROM industries"
            cur.execute(sql_txt)
        except Exception as er:
            logger_info.error(color("red", f"Ошибка удаления данных таблиц.\n {er}"))
        else:
            conn.commit()

