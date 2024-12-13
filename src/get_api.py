import requests
"""import logging
logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)"""

class GetAPI:
    """ Выполняет API-запрос и
    получает данные о работодателе и его вакансии """
    def __init__(self):
        #self.__status = 'init'
        self.__url_em = 'https://api.hh.ru/employers/'
        self.__url_vac = 'https://api.hh.ru/vacancies'
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'employer_id': 0}
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__status = '0'


    def company(self, id_hh) -> dict:
        """ Возвращает словарь с данными по компании"""


        response = {}
        # отправка API - запроса по компании 3 попытки
        for _ in range(3):
            response = requests.get(self.__url_em + str(id_hh), headers={'User-Agent': 'HH-User-Agent'})
            self.__status = response.status_code
            #print(self.__status)
            if self.__status == 200:
                #print('.', end='')
                break
        if self.__status == 200: result = response.json()
        else: result = {}

        return result


    @property
    def status(self) -> str:
        """ Возвращает статус API-запроса. '200' - всё хорошо """
        pass
        return self.__status



    def vacancies(self, id_hh) -> list:
        """ Возвращает список словареё с вакансиями
            список содержит словари по 100 вакансий"""
        self.__params['employer_id'] = id_hh
        response = {}
        result = []
        while  True:
            # отправка API - запроса по компании 3 попытки
            # https://api.hh.ru/vacancies?employer_id=1740
            for _ in range(3):
                response = requests.get(self.__url_vac, headers={'User-Agent': 'HH-User-Agent'}, params=self.__params)
                self.__status = response.status_code
                print('страница ', self.__params['page'], self.__status)
                if self.__status == 200:
                    break
            data = response.json()
            if len(data['items']) < 1 :
                break
            result.append(data)
            #result = response.json()
            self.__params['page'] += 1
            print(len(data['items']))
        return result