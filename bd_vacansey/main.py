import logging
from bd_vacansey.function_load import load_data
from bd_vacansey.function_menu import menu_db, menu_home
from config import OUTPUT_ON_MONITOR
from src.color import color
from src.db_connect import DBConnect
# from src.db_insert import DBInsert
from src.db_manager import DBManager
from src.flie_json import FileJSON

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


def main() -> None:
    print("\nПоиск вакансий с подключением БД\n")

    # DBInsert()
    # Загрузка списка компаний - проверка наличия данных в таблицах
    DBConnect.status = ''
    data_db = DBConnect.select_('SELECT True FROM company;')
    # Если данных нет - загрузить.
    if len(data_db) == 0 and DBConnect.status == 'Ok':
        load_data()

    # выводим меню
    while True:
        user_input = menu_home()

        if user_input == '1':  # Обновить данные в БД по API
            print(color('gray', "Обновление данных в БД"))
            load_data()

        if user_input == '9':  # Удалить БД и закончить работу
            user_input = input("БД будет полностью удалена (y/n):")
            if user_input == 'y':
                DBConnect.drop_all()

        if user_input == '2':  # Работа с вакансиями в БД
            select = DBManager()
            file = FileJSON()
            while True:
                user_input = menu_db()
                if user_input == '9':  # 9. Вернуться
                    break

                if user_input == '1':  # 1. Список компаний и количество вакансий
                    x = select.get_companies_and_vacancies_count()
                    if OUTPUT_ON_MONITOR:
                        for row in x:
                            print(f"{color('white', row[0])} - {row[1]} вакансий")
                    dict_for_json = file.dict_for_json(x, ['company', 'vacancies_count'])
                    status = file.save(dict_for_json, 'get_companies_and_vacancies_count.json')
                    print(status)

                if user_input == '2':  # 2. Все вакансии
                    x = select.get_all_vacancies()
                    if OUTPUT_ON_MONITOR:
                        i = 0
                        for row in x:
                            i += 1
                            if row[2] == 0:
                                zp = ''
                            else:
                                zp = f" - {str(row[2])} руб."
                            print(f"{i} {color('white', row[0])} - {row[1]}  {zp}  - https://hh.ru/vacancy/{row[3]}")

                    dict_for_json = file.dict_for_json(x, ['company', 'name', 'salary', 'url'])
                    status = file.save(dict_for_json, 'get_all_vacancies.json')
                    print(status)

                if user_input == '3':  # 3. Средняя зарплата по вакансиям
                    salary = select.get_avg_salary()
                    print("Средняя зарплата: ", salary)

                if user_input == '4':  # 4. Вакансии с зарплатой выше средней
                    salary = select.get_avg_salary()
                    q = select.get_vacancies_with_higher_salary(salary)
                    if OUTPUT_ON_MONITOR:
                        print(f"Вакансии с зарплатой выше: {salary} руб.")
                        for row in q:
                            print(f"{color('white', row[0])}  {int(row[1])} руб.")
                    dict_for_json = file.dict_for_json(q, ['name', 'salary'])
                    status = file.save(dict_for_json, 'get_vacancies_with_higher_salary.json')
                    print(status)

                if user_input == '5' or user_input == '6':  # 5-6. Поиск по ключевому слову
                    word = input("Введите ключевое слово: ")
                    print("\n\n")
                    word = f"%{word}%"
                    snippet = False
                    if user_input == '6':
                        snippet = True
                    q = select.get_vacancies_with_keyword(word, snippet)
                    if OUTPUT_ON_MONITOR:
                        for row in q:
                            print(f"{color('white', row[0])}  {row[1]},\n{row[2]}\n{row[3]}\n{row[4]} \n{row[5]}\n ")
                    dict_for_json = file.dict_for_json(q, ['vacancies_name', 'salary_avg', 'snippet', 'responsibility',
                                                           'schedule', 'url'])

                    status = file.save(dict_for_json, 'get_vacancies_with_keyword.json')
                    print(status)


if __name__ == "__main__":
    main()
