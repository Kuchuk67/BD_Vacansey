from config import OUTPUT_IN_FILES
from src.flie_json import FileJSON

file = FileJSON()


def output_in_files(x: list, list_colum: list, name_file: str) -> None:

    if OUTPUT_IN_FILES:
        dict_for_json = file.dict_for_json(x, list_colum)
        status = file.save(dict_for_json, name_file)
        print(status, "\n")
