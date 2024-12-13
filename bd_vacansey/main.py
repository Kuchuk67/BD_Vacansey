from src.get_api import GetAPI
from src.list_data import ListData
from config import LIST_COMPANY
from src.indastries import Industries
from src.db_connect import DBConnect
from src.db_insert import DBInsert
from src.color import color
import logging

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
#console_formatter = logging.Formatter(' %(message)s ')
#console_handler.setFormatter(console_formatter)
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)

"""logger_er = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler_er = logging.StreamHandler()
console_formatter = logging.Formatter('Error %(filename)s строка %(lineno)d')
console_handler_er.setFormatter(console_formatter)
logger_er.addHandler(console_handler_er)
logger_er.setLevel(logging.INFO)"""

def main():
    x = GetAPI()

    list_company_json = []

    logger_info.info(color('white', "Загрузка компаний") )
    er = 0
    for item in LIST_COMPANY:
        company_json = (x.company(item))
        if len(company_json) > 0: list_company_json.append(company_json)
        if x.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(color('white', f"\nЗагрузка {len(list_company_json)} компаний завершена"))
    if er > 0:
        logger_info.warning(color('yellow',  "Есть не загруженные компании"))
    xx = (ListData.company(list_company_json))
    print(xx)

    #q = DBInsert()

    '''x = q.select_('SELECT * FROM industries')
    if q.status == 'Error':
        logger_er.error(color('red', "Ошибка SQL запроса "))

    print(x)'''


    # с = x.company(780654)
    # l = x.vacancies(1740)
    # print(с)

    # x = Industries()
    # x.load()
    # print(Industries.dict_industries)


if __name__ == "__main__":
    main()
