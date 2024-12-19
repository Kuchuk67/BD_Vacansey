import logging

from config import LIST_COMPANY
from src.color import color
from src.db_insert import DBInsert
from src.get_api import GetAPI
from src.list_data import ListData

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


def load_data() -> None:
    """
    Создать если нет БД. Подключится к БД.
    Проверить есть ли данные. Если данных нет - загрузить.
    """
    print(color('gray', "Загрузка данных:"))
    ins = DBInsert()
    # чистим таблицы
    ins.remove_db(['v', 'c', 'i'])

    # Запись в БД отраслей промышленности
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.industries_insert(cur)
        conn.commit()

    # Подключаемся к API
    data_api = GetAPI()

    # Загрузка  компаний по API  из списка в config.py
    list_company_json = []
    logger_info.info(color('grey', "Загрузка компаний по API"))
    er = 0
    # идем по списку компаний
    for item in LIST_COMPANY:
        # загружаем компанию
        company_json = (data_api.company(item))
        if len(company_json) > 0:
            list_company_json.append(company_json)
        # проверяем ответ на ошибки
        if data_api.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(color('grey', f"\nЗагрузка компаний завершена: {len(list_company_json)}"))
    if er > 0:
        logger_info.warning(color('yellow', f"Есть не загруженные компании: {er}"))
    list_company = (ListData.company(list_company_json))

    # Запись в БД компаний
    with DBInsert.connect() as conn:
        cur = conn.cursor()
        ins.company_insert(cur, list_company)
        conn.commit()

    # загружаем вакансии по API
    logger_info.info(color('grey', "Загрузка вакансий по API"))
    # Загрузка списка компаний
    companies = DBInsert.select_('SELECT company_id, name FROM company;')

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
        if DBInsert.status == 'Ok':
            print("Ok")
        else:
            print("")
    print("\n\n")
