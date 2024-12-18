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

    #def __init__(self):
        #super().__init__()

    def industries_insert(self, cur) -> None:
        """  Заполнение БД industries"""
        DBInsert.status = 'Ok'
        # Загрузка API отраслей промышленности
        industries = Industries()
        industries_load = industries.load()
        logger_info.info(color('green', industries_load))

        # Заполнение БД industries
        #cur.execute('delete FROM industries;')
        #DBInsert.remove_db(['v','c','i'])

        i, separate, sql = 0, "", "INSERT INTO industries VALUES "
        for key, value in Industries.dict_industries.items():
            sql = sql + f"{separate} ({key}, '{value}')"
            separate = ", "
        sql = sql + ";"
        #print(sql)
        try:
            cur.execute(sql)
        except Exception as er:
            logger_info.error(color('red', f"Ошибка записи отраслей в БД.\n {er}"))



    def company_insert(self, cur, list_companies):
        """ Заполнение БД company"""
        cur.execute('delete FROM vacancies;')
        cur.execute('delete FROM company;')

        i, separate, sql = 0, "", "INSERT INTO company VALUES "
        for list_company in list_companies:


            sql = sql + (f"{separate} ({list_company.get('company_id')}, '{list_company.get('name')}', "
                         f"'{list_company.get('site_url')}',  "
                         f"'{list_company.get('industries')}' )")
            separate = ", "
        sql = sql + ";"
        cur.execute(sql)


    def vacancies_insert(self, cur, vacancies, company_id):
        """ Заполнение БД vacancies"""
        # cur.execute('delete FROM vacancies;')
        i, separate, sql = 0, " ", "INSERT INTO vacancies VALUES "
        for vacancy in vacancies:
            #if vacancy.get('vacancies_id') not in i:
                #i.append(vacancy.get('vacancies_id'))
            i +=1
            sql = sql + (f"{separate} ( DEFAULT ,"
                             f"{vacancy.get('vacancies_id')},"
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

            #else:
                #print("+++++")
        sql = sql + ";"

        """ # Код для проверки того, что записывается в базу вакансии
        f = open(str(company_id), 'w', encoding='utf-8') 
        f.write(sql)
        f.close()"""

        if i > 0:
            try:
                cur.execute(sql)
            except Exception as er:
                DBInsert.status = 'Error'
                logger_info.error(color('red', f"Ошибка записи вакансии в БД.\n {er}"))
        else:
            print('API вернул пустую строку')


    def remove_db(self, db_for_del: list):
        """ удаляет данные из таблиц. Вход список с литерами таблиц: ['v', 'c', 'i']:
        v - удалить данные в таблице vacancies;
        c - удалить company;
        i - удалить industries;

        """

        # .connect с БД
        conn = DBConnect.connect()
        cur = conn.cursor()
        if 'v' in db_for_del:
            try:
                sql_txt = "delete FROM vacancies"
                cur.execute(sql_txt)
            except Exception as er:
                logger_info.error(color('red', f"Ошибка удаления данных таблицы vacancies.\n {er}"))
            else:
                #print("удалено vacancies")
                conn.commit()

        if 'c' in db_for_del:
            try:
                sql_txt = "delete FROM company"
                cur.execute(sql_txt)
            except Exception as er:
                logger_info.error(color('red', f"Ошибка удаления данных таблицы company.\n {er}"))
            else:
                #print("удалено company")
                conn.commit()

        if 'i' in db_for_del:
            try:
                sql_txt = "delete FROM industries"
                cur.execute(sql_txt)
            except Exception:
                logger_info.error(color('red', f"Ошибка удаления данных таблицы industries.\n {er}"))
            else:
                #print("удалено industries")
                conn.commit()




