import os
import typing
from config import PATH_HOME
import json

class FileJSON():
    def __init__(self):
        if not os.path.exists(os.path.join(PATH_HOME, "data")):
            os.mkdir(os.path.join(PATH_HOME, "data"))
        #self.__path_to_file = os.path.join(PATH_HOME, "data")

    def save(self, dict_object: list, file_name: str) -> str:
        """ Добавляет вакансии в файл """
        file_name = os.path.join(PATH_HOME, "data", file_name)

        if typing.TYPE_CHECKING:
            from _typeshed import SupportsWrite
            files: SupportsWrite[str]
        try:
            with open(file_name, 'w', encoding='utf-8') as files:
                json.dump(dict_object, fp=files, indent=4, ensure_ascii=False)
        except Exception as er:
            return f"Ошибка записи файла; {er}"
        else:
            return file_name + ' - Сохранено'

    def dict_for_json(self, q: list, name_colum: list) -> list:
        """
        Преобазовывает список в словарь для JSON-а
        принимает словарь данных и
        список индексов для словаря json
        """
        result = []
        for item in q:
            dict_row = {}
            for i in range(len(name_colum)):
                dict_row[name_colum[i]] = item[i]
            result.append(dict_row)
        #print(result)
        return result