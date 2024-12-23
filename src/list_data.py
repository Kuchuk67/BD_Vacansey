from src.color import color


class ListData:
    """Подготавливает  список для записи в БД.
    Выбирает из json только те поля, что будут занесены в БД и список их вакансии"""

    # def __init__(self):
    #   self.__list_company = []

    @classmethod
    def company(cls, list_company_json: list) -> list:
        """Подготавливает список кампаний для записи в БД. Вывести список кампаний,
        где только те поля, что будут занесены в БД"""
        result = []
        for item in list_company_json:

            try:
                """result.append(
                    {
                        "company_id": item.get("id", "0"),
                        "name": item.get("name"),
                        "site_url": item.get("site_url"),
                        "industries": item.get("industries")[0].get("id"),
                    })"""
                result.append(
                    (item.get("id", "0"),item.get("name"),item.get("site_url"),item.get("industries")[0].get("id"),)
                )

            except Exception:
                print(color("red", "Ошибка добавления компании"), item)
        return result

    @classmethod
    def vacancy(cls, list_vacancy_json: list, company: str) -> list:
        """Подготавливает список вакансии для записи в БД.
        Выбирает из json только те поля, что будут занесены в БД вакансии
        Несуществующие адреса заменяет пробелами
        неуказанные запрлаты заменяет 0"""
        result = []
        for item in list_vacancy_json:  # [5]['items']:
            print(".", end="")
            for item1 in item["items"]:
                # i += 1

                try:
                    # item.get('address').get('city')
                    # item.get('address').get('street')
                    # item.get('address').get('city')

                    if item1.get("salary"):
                        salary_from = item1.get("salary").get("from")
                        salary_to = item1.get("salary").get("to")
                    else:
                        salary_from = 0
                        salary_to = 0
                    if not salary_from:
                        salary_from = 0
                    if not salary_to:
                        salary_to = 0

                    if item1.get("address"):
                        address = item1.get("address").get("raw")
                    else:
                        address = ""
                    if not address:
                        address = ""

                    if not item1.get("snippet").get("requirement"):
                        snippet = ""
                    else:
                        snippet = item1.get("snippet").get("requirement")
                        snippet = snippet.replace("'", " ")

                    if not item1.get("snippet").get("responsibility"):
                        responsibility = ""
                    else:
                        responsibility = item1.get("snippet").get("responsibility")
                        responsibility = responsibility.replace("'", " ")


                    if not item1.get("schedule").get("name"):
                        schedule = ""
                    else:
                        schedule = item1.get("schedule").get("name")
                        schedule = schedule.replace("'", " ")
                    a, b = salary_from, salary_to
                    if a == 0:
                        a = b
                    if b == 0:
                        b = a
                    salary_avg = (a + b) / 2

                    result.append(
                        ( item1.get("id", "0"), item1.get("name"), salary_from, salary_to,
                            salary_avg, address, snippet, responsibility, schedule, company
                        )
                    )
                except Exception as er:

                    print(color("red", f"Ошибка добавления компании {er}"))
        #print(len(result))
        return result
