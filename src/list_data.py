class ListData:
        """ Создает список компаний и список их вакансии"""
        def __init__(self):
            self.__list_company = []

        @property
        def list_company(self) -> list:
            """ Вывести список кампаний"""
            return self.__list_company

        @list_company.deleter
        def list_company(self):
            """ Очистить список кампаний"""
            self.__list_company = []

        def add(self, dict_about_company, dict_vacancies) -> None:
            """ Добавить в список кампаний новую позицию"""
            pass