from config import LIST_COMPANY
from src.color import color
from src.db_insert import DBInsert
from src.get_api import GetAPI
from src.list_data import ListData
from typing import Any


def load_data(connect: Any) -> None:
    """
    Создать если нет БД. Подключится к БД.
    Проверить есть ли данные. Если данных нет - загрузить.
    """
    print(color("gray", "Загрузка данных:"))

    ins = DBInsert(connect.conn)

    # чистим таблицы
    ins.remove_db(connect.conn)

    # Запись в БД отраслей промышленности
    ins.industries_insert()

    # Подключаемся к API
    data_api = GetAPI()

    # Загрузка  компаний по API  из списка в config.py
    list_company_json = []
    print(color("grey", "Загрузка компаний по API"))
    er = 0
    # идем по списку компаний
    for item in LIST_COMPANY:
        # загружаем компанию
        company_json = data_api.company(item)
        if len(company_json) > 0:
            list_company_json.append(company_json)
        # проверяем ответ на ошибки
        if data_api.status == 200:
            print(".", end="")
        else:
            print("x", end="")
            er += 1
    print(color("grey", f"\nЗагрузка компаний завершена: {len(list_company_json)}"))
    if er > 0:
        print(color("yellow", f"Есть не загруженные компании: {er}"))
    list_company = ListData.company(list_company_json)

    # Запись в БД компаний

    ins.company_insert(list_company)
    connect.conn.commit()

    # загружаем вакансии по API
    print(color("grey", "Загрузка вакансий по API\n"))
    # Загрузка списка компаний
    companies = connect.select_("SELECT company_id, name FROM company;")

    for company in companies:
        print(company[0], company[1], end="")
        # Получаем вакансии по API
        v = data_api.vacancies(company[0])
        # приводим список к нормальному виду для БД
        vacancies = ListData.vacancy(v, company[0])
        # Запись в БД вакансии

        ins.vacancies_insert(vacancies, company[0])
        connect.conn.commit()

        if connect.status == "Ok":
            print("Ok")
        else:
            print("")
    ins.close()
    print("\n\n")
