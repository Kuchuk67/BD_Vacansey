class ListData:
        """ Создает список компаний
         выбирает из json только те поля, что будут занесены в БД и список их вакансии"""
        #def __init__(self):
        #   self.__list_company = []

        @classmethod
        def company(cls, list_company_json: list) -> list:
            """ Вывести список кампаний только те поля, что будут занесены в БД"""
            result = []
            print(list_company_json[9])
            for item in list_company_json:
                result.append({'id': item['id'],
                               'name': item['name'],
                               #'description': item['description'],
                               'site_url': item['site_url'],
                               'industries': item['industries'],
                               })
            return result



        def add(self, dict_about_company, dict_vacancies) -> None:
            """ Добавить в список кампаний новую позицию"""
            pass