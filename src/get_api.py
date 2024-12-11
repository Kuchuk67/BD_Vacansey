class GetAPI:
    """ Выполняет API-запрос и
    получает данные о работодателе и его вакансии """
    def __init__(self):
        self.__status = 'init'
        pass


    @property
    def status(self) -> str:
        """ Возвращает статус API-запроса. '200' - всё хорошо """
        pass
        return self.__status


    @property
    def company(self) -> dict:
        """ Возвращает словарь с данными по компании"""
        result = {}
        pass
        return result


    @property
    def vacancies(self) -> dict:
        """ Возвращает словарь с вакансиями"""
        result = {}
        pass
        return result

