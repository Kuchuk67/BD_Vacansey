import logging
from typing import Any
from src.color import color
from src.indastries import Industries

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


class DBInsert:
    """Содержит методы для записи данных в таблицы"""

    def __init__(self, connect: Any):
        # connect = DBConnect()
        # self.connect =  DBConnect.connect()
        self.__cur = connect.cursor()

    def industries_insert(self) -> None:
        """Заполнение БД industries"""

        # Загрузка API отраслей промышленности
        industries = Industries()
        industries_load = industries.load()
        logger_info.info(color("green", industries_load))

        # Заполнение БД industries
        self.__cur.executemany(
            "INSERT INTO industries (industries_id, industries_name)  VALUES (%s,%s)",
                               Industries.dict_industries
                               )


    def company_insert(self, list_companies: list) -> None:
        """Заполнение БД company"""
        self.__cur.executemany("INSERT INTO company VALUES (%s,%s,%s,%s)", list_companies)


    def vacancies_insert(self, vacancies: list, company_id: int) -> None:
        """Заполнение БД vacancies"""

        self.__cur.executemany(
            "INSERT INTO vacancies VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (vacancies_id) DO NOTHING;",
            vacancies
        )


        # f = open(str(company_id), 'w', encoding='utf-8')
        # f.write(args_str)
        # f.close()

    def remove_db(self, connect: Any) -> None:
        """удаляет данные из таблиц."""

        # .connect с БД
        # conn = DBConnect.connect()
        # cur = self.__cur.cursor()
        try:
            sql_txt = "delete FROM vacancies; delete FROM company; delete FROM industries"
            self.__cur.execute(sql_txt)
        except Exception as er:
            logger_info.error(color("red", f"Ошибка удаления данных таблиц.\n {er}"))
        else:
            connect.commit()

    def close(self) -> None:
        self.__cur.close()
