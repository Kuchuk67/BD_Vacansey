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
# console_formatter = logging.Formatter(' %(message)s ')
# console_handler.setFormatter(console_formatter)
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

    # Запись в БД отраслей промышленности
    """ins = DBInsert()
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.industries_insert(cur)
        conn.commit()"""

    ins = DBInsert()

    # Подключаемся к API
    x = GetAPI()

    """# Загрузка  компаний по API  из списка в config.py
    list_company_json = []
    logger_info.info(color('white', "Загрузка компаний"))
    er = 0
    # идем по списку компаний
    for item in LIST_COMPANY:
        # загружаем компанию
        company_json = (x.company(item))
        if len(company_json) > 0: list_company_json.append(company_json)
        # проверяем ответ на ошибки
        if x.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(color('white', f"\nЗагрузка компаний завершена: {len(list_company_json)}"))
    if er > 0:
        logger_info.warning(color('yellow', f"Есть не загруженные компании: {er}"))
    list_company = (ListData.company(list_company_json))
    print(list_company)

    # Запись в БД компаний
    ins = DBInsert()
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.company_insert(cur, list_company)
        conn.commit()"""

    # загружаем вакансии по API
    logger_info.info(color('white', "Загрузка вакансий"))
    # Загрузка списка компаний
    companies = ins.select_('SELECT company_id, name FROM company;')

    ins = DBInsert()
    for company in companies:
        print("\n",company[0], company[1])

        v = x.vacancies(company[0])
        # приводим список к нормальному виду для БД
        vacancies = ListData.vacancy(v)
         # Запись в БД вакансии
        with DBInsert.connect() as conn:
            cur = conn.cursor()
            ins.vacancies_insert(cur, vacancies, company[0])
            conn.commit()








    #print(len(v))

    #print(v)
    """i=0
    for item in v: #[5]['items']:
        for item1 in item['items']:
            i+=1
            print(i, "  ",item1)"""






    # с = x.company(780654)
    # l = x.vacancies(1740)
    # print(с)


    # ненужно
    """x = Industries()
    x.load()
    print(Industries.dict_industries)"""





""" x = ins.select_('SELECT * FROM industries')
    if ins.status == 'Error':
        logger_info.error(color('red', "Ошибка SQL запроса "))
    print(x)
"""


if __name__ == "__main__":
    main()
