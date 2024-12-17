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
    """ Подключается к БД
    Содержит методы для записи данных в таблицы"""
    # def __init__(self):
    # super.__init__()

    def industries_insert(self, cur) -> None:
        """  Заполнение БД industries"""
        DBInsert.status = 'Ok'
        # Загрузка API отраслей промышленности
        industries = Industries()
        logger_info.info(color('white', industries.load()))

        # Заполнение БД industries
        cur.execute('delete FROM industries;')

        i, separate, sql = 0, "", "INSERT INTO industries VALUES "
        for key, value in Industries.dict_industries.items():
            sql = sql + f"{separate} ({key}, '{value}')"
            separate = ", "
        sql = sql + ";"
        cur.execute(sql)


    def company_insert(self, cur, list_companies):
        """ Заполнение БД company"""
        cur.execute('delete FROM vacancies;')
        cur.execute('delete FROM company;')

        i, separate, sql = 0, "", "INSERT INTO company VALUES "
        for list_company in list_companies:
            sql = sql + (f"{separate} ({list_company.get('company_id')}, '{list_company.get('name')}', "
                         f"'{list_company.get('site_url')}', '{list_company.get('description')}', "
                         f"'{list_company.get('industries')}' )")
            separate = ", "
        sql = sql + ";"
        cur.execute(sql)

    def vacancies_insert(self, cur, vacancies, company_id):
        """ Заполнение БД vacancies"""
        #cur.execute('delete FROM vacancies;')
        i, separate, sql = 0, " ", "INSERT INTO vacancies VALUES "
        for vacancy in vacancies:

            sql = sql + (f"{separate} ({vacancy.get('vacancies_id')},"
                         f"'{vacancy.get('vacancies_name')}',"
                         f"{vacancy.get('salary_from')},"
                         f"{vacancy.get('salary_to')},"
                         f"{vacancy.get('salary_avg')},"
                         f"'{vacancy.get('address')}',"
                         f"'{vacancy.get('snippet')}',"
                         f"'{vacancy.get('responsibility')}', "
                         f"'{vacancy.get('schedule')}', "
                         f"{int(company_id)} )")
            separate = ", "
        sql = sql + ";"
        try:
            cur.execute(sql)
        except Exception as er:
            DBInsert.status  = 'Error'
            logger_info.error(color('red', f"Error: Ошибка записи вакансии в БД {er}"))



    def delete(self):
        """ удаляет данные из таблиц"""
        sql_txt = "delete FROM vacancies"
        # .connect с БД
        conn = DBConnect.connect()
        cur = conn.cursor()
        try:
            cur.execute(sql_txt)
        except Exception:
            pass
        else:
            print("удалено vacancies")
            conn.commit()

    def reset(self):
        """удаляет полностью БД"""
        pass
