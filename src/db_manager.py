from src.db_connect import DBConnect
from src.color import color
import  logging
logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
# console_formatter = logging.Formatter(' %(message)s ')
# console_handler.setFormatter(console_formatter)
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)

class DBManager(DBConnect):
    """ Класс методов работы с БД"""
    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""

        sql = """SELECT company.name, count(vacancies.vacancies_id) 
FROM vacancies RiGHT JOIN company ON company.company_id = vacancies.company_id   
GROUP BY company.name """
        DBConnect.status = ''
        result = DBConnect.select_(sql)
        DBManager.error_handling(result, DBConnect.status)
        return result


    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию. hh.ru/vacancy/112968986"""
        #sql = """SELECT AVG(vacancies.salary_avg) FROM vacancies WHERE salary_avg > 0 """
        sql = """SELECT company.name, vacancies_name, salary_avg, 'https://hh.ru/vacancy/' || vacancies_id as url          
        FROM vacancies JOIN company ON company.company_id=vacancies.company_id; """
        DBConnect.status = ''
        result = DBConnect.select_(sql)
        DBManager.error_handling(result, DBConnect.status)
        return result

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        #sql = """SELECT company.name, AVG(vacancies.salary_avg)
#FROM vacancies RiGHT JOIN company ON company.company_id = vacancies.company_id
#GROUP BY company.name """
        sql = """SELECT AVG(salary_avg)  FROM vacancies WHERE salary_avg > 0 """
        DBConnect.status = ''
        result = DBConnect.select_(sql)
        DBManager.error_handling(result, DBConnect.status)
        return int(result[0][0])


    def get_vacancies_with_higher_salary(self, salary: int):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql = """SELECT vacancies_name, salary_avg  FROM vacancies WHERE salary_avg > """  + str(salary)
        DBConnect.status = ''
        result = DBConnect.select_(sql)
        DBManager.error_handling(result, DBConnect.status)
        return result


    def get_vacancies_with_keyword(self, word:str):

        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        sql = """SELECT  vacancies_name, salary_avg, snippet, responsibility, schedule, 'https://hh.ru/vacancy/' || vacancies_id as url  FROM vacancies 
WHERE snippet  LIKE '%s'
OR responsibility  LIKE '%s'
OR schedule  LIKE '%s'
OR vacancies_name  LIKE '%s'
""" % ( word,word,word,word,)

        DBConnect.status = ''
        result = DBConnect.select_(sql)
        DBManager.error_handling(result, DBConnect.status)
        return result


    @staticmethod
    def error_handling(result, status):
        """ Выводит сообщение об ошибке при статусе отличном от 'Ok'
         или предупреждение при возвращении пустого ответа"""
        if status != 'Ok':
            logger_info.error(color('red', f"Ошибка SQL-запроса"))
        if status == 'Ok' and result == []:
            logger_info.warning(color('yellow', "SQL-запрос вернулся пустой"))