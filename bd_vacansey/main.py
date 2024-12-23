from bd_vacansey.function_load import load_data
from bd_vacansey.function_menu import menu_db, menu_home
from bd_vacansey.output_in_files import output_in_files
from src.color import color
from src.db_connect import DBConnect
from src.db_manager import DBManager

def is_salary_null(salary:int) -> str:
    """ Обработка вывода зарплаты.
    Возвращает строку '- 123 руб.' если на входе число больше нуля,
    иначе пустая строка"""
    if salary == 0:
        return ""
    else:
        return f" - {str(salary)} руб."


def main() -> None:
    print("\nПоиск вакансий с подключением БД\n")
    connect = DBConnect()
    connect.connect()
    # Загрузка списка компаний - проверка наличия данных в таблицах
    data_db = connect.select_("SELECT True FROM company;")
    # Если данных нет - загрузить.
    if len(data_db) == 0 and connect.status == "Ok":
        load_data(connect)

    # выводим меню
    while True:
        user_input = menu_home()

        if user_input == "9":  # Удалить БД и закончить работу
            user_input = input("БД будет полностью удалена (y/n):")
            if user_input == "y":
                connect.drop_all()

        if user_input == "1":  # Обновить данные в БД по API
            print(color("gray", "Обновление данных в БД"))
            load_data(connect)

        if user_input == "2":  # Работа с вакансиями в БД
            select = DBManager()

            while True:   # Подменю
                user_input = menu_db()
                if user_input == "9":  # 9. Вернуться
                    break

                # 1. Список компаний и количество вакансий
                if user_input == "1":
                    x = select.get_companies_and_vacancies_count(connect)
                    output_in_files(x, ["company", "vacancies_count"],"get_companies_and_vacancies_count.json")
                    for row in x:
                        print(f"{color('white', row[0])} - {row[1]} вакансий")

                # 2. Все вакансии
                if user_input == "2":
                    x = select.get_all_vacancies(connect)
                    output_in_files(x, ["company", "name", "salary", "url"], "get_all_vacancies.json")
                    number = 0
                    for row in x:
                        number += 1
                        print(f"{number} {color('white', row[0])} - {row[1]}  {is_salary_null(row[2])}  - https://hh.ru/vacancy/{row[3]}")

                # 3. Средняя зарплата по вакансиям
                if user_input == "3":
                    salary = select.get_avg_salary(connect)
                    print("Средняя зарплата: ", salary)

                # 4. Вакансии с зарплатой выше средней
                if user_input == "4":
                    salary = select.get_avg_salary(connect)
                    q = select.get_vacancies_with_higher_salary(connect, salary)
                    output_in_files(q, ["name", "salary"], "get_vacancies_with_higher_salary.json")

                    print(f"Вакансии с зарплатой выше: {salary} руб.")
                    for row in q:
                        print(f"{color('white', row[0])}  {int(row[1])} руб.")

                # 5-6. Поиск по ключевому слову
                if user_input == "5" or user_input == "6":
                    word = input("Введите ключевое слово: ")
                    print("\n\n")
                    word = f"%{word}%"
                    snippet = False
                    if user_input == "6":
                        snippet = True
                    q = select.get_vacancies_with_keyword(connect, word, snippet)
                    output_in_files(q,
                        ["vacancies_name", "salary_avg", "snippet", "responsibility", "schedule", "url"],
                         "get_vacancies_with_keyword.json")
                    number = 0
                    for row in q:
                        number+=1
                        print(f"{number}. {color('white', row[0])}  {is_salary_null(row[1])}\n{row[2]}\n{row[3]}\n{row[4]} \n{row[5]}\n ")


        if user_input == "3":
            connect.close()
            quit(print("\nЗавершение работы программы"))

if __name__ == "__main__":
    main()
