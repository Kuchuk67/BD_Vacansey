from src.get_api import GetAPI
from src.list_data import ListData
#from config import LIST_COMPANY, WHITE, YELLOW, RESET_COLOR
from src.indastries import Industries
from src.db_connect import DBConnect
from src.color import color
import logging

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)

logger_er = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler_er = logging.StreamHandler()
console_formatter = logging.Formatter('Error %(filename)s строка %(lineno)d')
console_handler_er.setFormatter(console_formatter)
logger_er.addHandler(console_handler_er)
logger_er.setLevel(logging.INFO)

def main():
    """x = GetAPI()

    list_company_json = []

    logger_info.info(WHITE + "Загрузка компаний" )
    er = 0
    for item in LIST_COMPANY:
        list_company_json.append(x.company(item))
        if x.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(WHITE + "\nЗагрузка компаний завершена")
    if er > 0:
        logger_info.warning(YELLOW + "Есть не загруженные компании"+ RESET_COLOR)
     # print(ListData.company(list_company_json))"""
    q = DBConnect()

    # Заполнение БД industries
    industries = Industries()
    print(industries.load())
    conn = DBConnect.connect()
    cur = conn.cursor()
    cur.execute('delete FROM industries;')
    conn.commit()
    sql = ''
    for key , value in Industries.dict_industries.items():
        if i == 0: sql = "INSERT INTO industries VALUES "
        sql = sql + f"({key}, '{value}')"
        i += 1
        if i == 10:
            sql = sql + ", "
        else:
            i = 0
            sql = sql + ";"
            cur.execute(sql)
    conn.commit()


    x = q.select('SELECT * FROM industries')
    if q.status == 'Error':
        logger_er.error(color('red', "Ошибка SQL запроса "))

    print(x)


    # с = x.company(780654)
    # l = x.vacancies(1740)
    # print(с)

    # x = Industries()
    # x.load()
    # print(Industries.dict_industries)


if __name__ == "__main__":
    main()
