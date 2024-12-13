from src.get_api import GetAPI
from src.list_data import ListData
#from config import LIST_COMPANY, WHITE, YELLOW, RESET_COLOR
from src.indastries import Industries
from src.db_connect import DBConnect

import logging

logger_info = logging.getLogger(__name__)
# Создаем хендлер для вывода в консоль
console_handler = logging.StreamHandler()
logger_info.addHandler(console_handler)
logger_info.setLevel(logging.INFO)


def main():
    """x = GetAPI()

    list_company_json = []

    logger_info.info(WHITE + "Загрузка компаний" )
    er = 0
    for item in LIST_COMPANY:
        list_company_json.append(x.company(item))
        if x.status == 200:
            print('.', end='')
        else:
            print('x', end='')
            er += 1
    logger_info.info(WHITE + "\nЗагрузка компаний завершена")
    if er > 0:
        logger_info.warning(YELLOW + "Есть не загруженные компании"+ RESET_COLOR)
     # print(ListData.company(list_company_json))"""

    q = DBConnect()


    # с = x.company(780654)
    # l = x.vacancies(1740)
    # print(с)

    # x = Industries()
    # x.load()
    # print(Industries.dict_industries)


if __name__ == "__main__":
    main()
