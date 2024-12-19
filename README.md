# BD_Vacansey
## Программа работы с вакансиями с продключением БД 

* Соединение с Базой Данных.
* Выполняет API-запрос и получает данные о работодателе и его вакансии 
* Содержит методы для записи данных в таблицы
* Класс методов работы с БД с выводом в JSON-файлы


## Структура проекта

### файл .env
Приватные настройки доступа к БД 
Для работы необходимо создать файл .env 
заполнив его согласно примеру: файл .env.example
### модуль bd_vacansey
Модуль пользовательской оболочки для работы с программой
### модуль src
Классы работы  с данными
### каталог data
Каталог хранения данных пользователя
### файл config.py
[Дополнительные настройки](#config) программы и API запросов 


## Содержание

* [class DBConnect()](#DBConnect) db_connect.py
* [class DBInsert (DBConnect)](#DBInsert)  db_insert.py
* [class DBManager (DBConnect)](#DBManager)  db_manager.py
* [class GetAPI](#GetAPI)   get_api.py 
* [class ListData](#ListData)  list_data.py
* [библиотека color](#color) color.py
  

# DBConnect
Соединение с Базой Данных, если нет БД, то создадим.
Проверяем есть ли таблицы в БД, если нет - создаем.
Создается таблица industries.
Создается таблица company.
Создается таблица vacancies.

##  connect
#### staticmethod
```with DBConnect.connect() as conn:```

Устанавливает соединение с БД.

## select_ 
#### staticmethod
Соединяется с БД и отправляет SQL запрос.
Возвращает список строк или пустой список.
Записывает статус ответа в DBConnect.status
Закрывает соединение.

## drop_all
удаляет полностью БД

# DBInsert
### наследник DBConnect
Подключается к БД.
Содержит методы для записи данных в таблицы.

``` 
ins = DBInsert() 
with DBInsert.connect() as conn:
```

## industries_insert
Заполнение таблицы БД industries данными, которые предварительно
подготовлены классом ListData
``` 
cur = conn.cursor()
ins.industries_insert(cur)
conn.commit()
```


## company_insert
Заполнение таблицы БД company(list_company), которые предварительно
подготовлены классом ListData
```
cur = conn.cursor()
ins.company_insert(cur, list_company)
conn.commit()
```

## vacancies_insert
Заполнение таблицы БД vacancies(vacancies), которые предварительно
подготовлены классом ListData
company_id поле-ключ для связи с таблицей  company (id компании)
```
cur = conn.cursor()
ins.vacancies_insert(cur, vacancies, company_id)
conn.commit()
```

##  remove_db
удаляет данные из таблиц. 
Получает список с литерами таблиц: ['v', 'c', 'i']:
v - удалить данные в таблице vacancies;
c - удалить company;
i - удалить industries;

``` ins.remove_db(['v', 'c', 'i']) ```
 

# DBManager
### наследник DBConnect
Класс методов организации запросов к БД

## get_companies_and_vacancies_count
Получает список всех компаний и количество вакансий у каждой компании.
Возвращает список строк и DBConnect.status = 'Ok'
```
 x = select.get_companies_and_vacancies_count()
```

## get_all_vacancies
Получает список всех вакансий с указанием названия компании,
вакансии и зарплаты и ссылки на вакансию. 
Возвращает список строк и DBConnect.status = 'Ok'
```
x = select.get_all_vacancies()
```

## get_avg_salary
Получает среднюю зарплату по вакансиям.
Возвращает int и DBConnect.status = 'Ok'
```
salary = select.get_avg_salary()
```

## get_vacancies_with_higher_salary
Получает список всех вакансий, у которых зарплата выше указанной
по всем вакансиям.
Принимает salary: int - зарплата.
Возвращает список строк и DBConnect.status = 'Ok'
```
х = select.get_vacancies_with_higher_salary(salary)
```

## get_vacancies_with_keyword
Получает список всех вакансий, в названии и описании которых 
содержатся переданные в метод слова, например 'python'.
Принимает word: str - поисковый запрос.
Возвращает список строк и DBConnect.status = 'Ok'
```
x = select.get_vacancies_with_keyword(word)
```

## error_handling
#### staticmethod
Обрабатывает выходные данные выше указанных методов.
Выводит сообщение об ошибке запроса (при статусе отличном от 'Ok') 
или предупреждение при возвращении пустого ответа
Принимает: результат запроса и статус запроса. 
```
DBManager.error_handling(result, DBConnect.status)
```

# FileJSON
Класс методов сохранения словарей в json-файл

## dict_for_json
Преобразовывает список строк (полученных с SQL-запросом)
в словарь для JSON-а
принимает словарь данных и список индексов для словаря json
```
file = FileJSON()
q = [('Softline', 169), ('HeadHunter', 55),]
dict_for_json = file.dict_for_json(q, ['name', 'salary'])
print(dict_for_json)
>>> [
{'company': 'Softline', 'vacancies_count': 169},
{'company': 'HeadHunter', 'vacancies_count': 55}
]
```

## save
Добавляет вакансии в файл 
Принимает: список словарей с вакансиями, имя файла.
При удачной записи возвращает фразу: "имя файла - Сохранено"
```
file = FileJSON()
status = file.save(dict_for_json, 'имя_файла.json')
```



# GetAPI
Выполняет API-запрос и получает данные о работодателе и его вакансии 
```
data_api = GetAPI()
```

## company
Получает данные по компаниях по API.
отправка API - запроса по компании 3 попытки.
Принимает id компании на hh.ru
Выводит на монитор символ '.' при успешной загрузке
и символ 'х' при неудачной загрузке.
Неудачная загрузка не останавливает работу программы.
Возвращает словарь с данными по данной компании.
Ответ API сервера сохраняется в атрибуте data_api.status,
так при успешной загрузке data_api.status = 200
```
company_json = (data_api.company(item))
```

## vacancies
Принимает id компании на hh.ru
Возвращает список словарей с вакансиями.
Список содержит словари по 100 вакансий каждый.
Прогресс-бар загрузки словарей отображается выводом на экран символа '.'

```
vac = data_api.vacancies(company_id)
```

## status
Возвращает статус API-запроса. '200' - всё хорошо
```
 if data_api.status == 200:
 ....
```


# Industries
Класс для получения данных, обработки и загрузки отраслей промышленности
Выходные данные содержатся в атрибуте Industries.dict_industries
```
industries = Industries()
```

## load
загружает JSON формат с данными по отраслям промышленности
Обрабатывает его с помощью статической функции industries
Выходные данные (список словарей с отраслями промышленности и их id)
содержатся в атрибуте Industries.dict_industries
```
industries_load = industries.load()
```

## industries
#### staticmethod
Рекурсивная функция для метода load для парсинга файла отрасли промышленности
Выходные данные (список словарей с отраслями промышленности и их id)
содержатся в атрибуте Industries.dict_industries
```
Industries.industries(industry)
```


# ListData
Подготавливает список для записи в БД.
Выбирает из json только те поля, что будут занесены в БД
и список их вакансии

## company
#### staticmethod
Подготавливает список кампаний для записи в БД. Вывести список кампаний,
где только те поля, что будут занесены в БД"""
```
list_company = (ListData.company(list_company_json))
```     

## vacancy
#### staticmethod
Подготавливает список вакансии для записи в БД.
Выбирает из json только те поля, что будут занесены в БД вакансии
Несуществующие адреса заменяет пробелами
неуказанные зарплаты заменяет 0
```
vacancies = ListData.vacancy(vac)
```


## color
Делает выводимый текст цветным
ввод: цвет: str, текст: str 
При работе из командной строки, где не поддерживается вывод цветом,
можно отключить цвета в файле config.py - COLOR = False
Поддерживаются цвета:
'white'
'red'
'green'
'yellow'
'grey'
'blue'
```
print(color('red', "красный цвет")
```


# config
config.py содержит настройки программы с комментариями-описанием 
LIST_COMPANY - константа содержит список id:int загружаемых компаний с hh.ru 
