from src.color import color


def menu_home() -> str:
    """ Функция выводит пользовательское меню - основное меню.
    Возвращает выбранный пункт"""
    while True:
        print(color('blue', """1. Обновить данные в БД по API
2. Работа с вакансиями в БД
3. Выход
9. Удалить БД и закончить работу"""))
        user_input = input("Выберите номер пункта меню: ")
        if user_input == '3':
            quit(print("\nЗавершение работы программы"))
        elif user_input in ['1', '2', '9']:
            return user_input
        print("\n\n")


def menu_db() -> str:
    """ Функция выводит пользовательское меню - меню работы с БД.
    Возвращает выбранный пункт"""
    print(color('blue', """\n\n1. Список компаний и количество вакансий
2. Все вакансии (файл JSON)
3. Средняя зарплата по вакансиям
4. Вакансии с зарплатой выше средней (файл JSON)
5. Поиск по ключевому слову в названиях (файл JSON)
6. Поиск по ключевому слову в названиях и описаниях (файл JSON)
9. Вернуться """))

    user_input = input("Выберите номер пункта меню: ")
    print("\n\n")
    if user_input in ['1', '2', '3', '4', '5', '6', '9']:
        return user_input

    return '0'
