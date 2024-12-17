from src.get_api import GetAPI
from src.list_data import ListData
from config import LIST_COMPANY
from src.indastries import Industries
from src.db_connect import DBConnect
from src.db_insert import DBInsert
from src.db_manager import DBManager
from src.color import color
import logging
from src.flie_json import FileJSON

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
    #x:list =['v', 'c', 'i']
    ins.remove_db(['v', 'c', 'i'])
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.industries_insert(cur)
        conn.commit()"""


    # Подключаемся к API
    """ data_api = GetAPI()

    # Загрузка  компаний по API  из списка в config.py
    list_company_json = []
    logger_info.info(color('white', "Загрузка компаний"))
    er = 0
    # идем по списку компаний
    for item in LIST_COMPANY:
        # загружаем компанию
        company_json = (data_api.company(item))
        if len(company_json) > 0: list_company_json.append(company_json)
        # проверяем ответ на ошибки
        if data_api.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(color('white', f"\nЗагрузка компаний завершена: {len(list_company_json)}"))
    if er > 0:
        logger_info.warning(color('yellow', f"Есть не загруженные компании: {er}"))
    list_company = (ListData.company(list_company_json))


    # Запись в БД компаний
    ins = DBInsert()
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.company_insert(cur, list_company)
        conn.commit()"""

    """data_api = GetAPI()

    # загружаем вакансии по API
    logger_info.info(color('white', "Загрузка вакансий"))
    # Загрузка списка компаний
    companies = DBConnect.select_('SELECT company_id, name FROM company;')

    ins = DBInsert()

    ins.remove_db(['v'])

    for company in companies:
        print(company[0], company[1], end="")
        # Получаем вакансии по API
        v = data_api.vacancies(company[0])
        # приводим список к нормальному виду для БД
        vacancies = ListData.vacancy(v)
         # Запись в БД вакансии
        DBInsert.status = 'Ok'
        with DBInsert.connect() as conn:
            cur = conn.cursor()
            ins.vacancies_insert(cur, vacancies, company[0])
            conn.commit()
        if DBInsert.status == 'Ok': print("Ok")
        else: print("")"""







    select = DBManager()
    file = FileJSON()
    """
    x = select.get_companies_and_vacancies_count()
    for row in x:
        print(f"{color('white',row[0])} - {row[1]} вакансий")"""


    x = select.get_all_vacancies()
    i = 0
    for row in x:
        i +=1
        if row[2] == 0: zp = ''
        else : zp = f" - {str(row[2])} руб."
        print(f"{i} {color('white',row[0])} - {row[1]}  {zp}  - https://hh.ru/vacancy/{row[3]}")

    dict_for_json = file.dict_for_json(x,['company', 'name', 'salary', 'url'])
    status = file.save(dict_for_json, 'get_all_vacancies.json')
    print(status)




    salary = select.get_avg_salary()
    print("Средняя зарплата: ", salary)


    q = select.get_vacancies_with_higher_salary(salary)
    print(f"Вакансии с зарплатой выше: {salary} руб.")
    #for row in q:
        #print(f"{color('white', row[0])}  {int(row[1])} руб.")
    dict_for_json = file.dict_for_json(x, ['name', 'salary' ])
    status = file.save(dict_for_json, 'get_vacancies_with_higher_salary.json')
    print(status)




    word = "python"
    word = f"%{word}%"
    q = select.get_vacancies_with_keyword(word)

    file = FileJSON()
    dict_for_json = file.dict_for_json(q , ['vacancies_name', 'salary_avg', 'snippet', 'responsibility', 'schedule', 'url' ])
    status = file.save( dict_for_json,'get_vacancies_with_higher_salary.json')
    print(status)

    #for row in q:
        #print(f"{color('white', row[0])}  {row[1]} ")

    #select.drop_all()





if __name__ == "__main__":
    main()
