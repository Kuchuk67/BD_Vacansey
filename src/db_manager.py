from db_connect import DBConnect

class DBManager(DBConnect):
    def get_companies_and_vacancies_count(self):
        """ получает список всех компаний и количество вакансий у каждой компании."""
        """ SELECT company.name, count(vacancies.vacancies_id) 
FROM vacancies JOIN company ON company.company_id=vacancies.company_id   
GROUP BY company.name """
        pass
    def get_all_vacancies(self):
        """ получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        """ SELECT company.name, vacancies_name, salary_from, salary_to  
FROM vacancies JOIN company ON company.company_id=vacancies.company_id; """
        pass
    def get_avg_salary(self):
        """ получает среднюю зарплату по вакансиям."""
        """ SELECT AVG(salary_from) FROM vacancies; """
        pass
    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        """ SELECT vacancies_name,salary_from  FROM vacancies WHERE salary_from > 56737 """
        pass
    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        """ SELECT vacancies_name,snippet, responsibility, schedule  FROM vacancies 
WHERE snippet  LIKE '%python%'
OR responsibility  LIKE '%python%'
OR schedule  LIKE '%python%'"""
        pass