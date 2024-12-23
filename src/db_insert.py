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
        args_str = [(x) for x in Industries.dict_industries]
        self.__cur.executemany("INSERT INTO industries (industries_id, industries_name)  VALUES (%s,%s)", args_str)
        #args_str = ",".join(self.__cur.mogrify("(%s,%s)", x).decode("utf-8") for x in Industries.dict_industries)
        #self.__cur.execute("INSERT INTO industries (industries_id, industries_name) VALUES " + args_str)

    def company_insert(self, list_companies: list) -> None:
        """Заполнение БД company"""
        args_str = [(x) for x in list_companies]
        self.__cur.executemany("INSERT INTO company VALUES (%s,%s,%s,%s)", args_str)

        #args_str = ",".join(self.__cur.mogrify("(%s,%s,%s,%s)", x).decode("utf-8") for x in list_companies)
        #self.__cur.execute("INSERT INTO company VALUES " + args_str)

    def vacancies_insert(self, vacancies: list, company_id: int) -> None:
        """Заполнение БД vacancies"""
        # Код для проверки того, что записывается в базу вакансии

        args_str = [(x) for x in vacancies]
        self.__cur.executemany("INSERT INTO vacancies VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (vacancies_id) DO NOTHING;", args_str)

        #args_str = ",".join(
         #   self.__cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in vacancies
        #)
        #self.__cur.execute("INSERT INTO vacancies VALUES " + args_str + " ON CONFLICT (vacancies_id) DO NOTHING;")

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
