import os
import requests
import json
from typing import Any

#from config import PATH_HOME
import re


class Industries:
    """ Класс определения id региона"""
    dict_industries = {}

    def __init__(self) -> None:

        self.__url = 'https://api.hh.ru/industries'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.status:int = 0



    @classmethod
    def industries(cls, industries: dict) -> None:
        """ Рекурсивный метод для парсинга файла отрасли промышленности"""
        for industry in industries:
            name = industry['name']
            id_ = industry['id']
            industries_ = industry.get('industries', None)
            Industries.dict_industries[id_] = name
            if industries_:
                Industries.industries(industries_)




    def load(self) -> str:
        """ загружает отрасли промышленности"""
        response = requests.get(self.__url, headers=self.__headers)
        self.status = response.status_code
        if self.status == 200:
            print("Загрузка отраслей промышленности - ОК")
            industry = response.json()
            Industries.industries(industry)
            return 'Ok'
        else:
            return f"Ошибка API запроса: {self.status}"

