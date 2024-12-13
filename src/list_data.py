from src.color import color

class ListData:
        """ Создает список компаний
         выбирает из json только те поля, что будут занесены в БД и список их вакансии"""
        #def __init__(self):
        #   self.__list_company = []

        @classmethod
        def company(cls, list_company_json: list) -> list:
            """ Вывести список кампаний, где только те поля, что будут занесены в БД"""
            result = []
            for item in list_company_json:
                #if item.get('id','0') != 0:
                try:
                    result.append({'id': item.get('id','0'),
                                   'name': item['name'],
                                   #'description': item['description'],
                                   'site_url': item['site_url'],
                                   'industries': item.get('industries')[0].get('id'),
                                   })
                except Exception:
                    print(color("Ошибка добавления компании"),item)
            return result



        def add(self, dict_about_company, dict_vacancies) -> None:
            """ Добавить в список кампаний новую позицию"""
            pass