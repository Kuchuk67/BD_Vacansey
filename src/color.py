from config import COLOR
# color


def color(color_,txt) -> str:
    """ Делает выводимый текст цветным
    ввод: цвет: str, текст: str"""
    colors = {
        'white': "\033[97m".format(),
        'red': "\033[31m".format(),
        'green': "\033[32m".format(),
        'yellow': "\033[33m".format(),
        'grey': "\033[37m".format(),
        'blue': "\033[34m".format(),
        'reset': "\033[0m".format(),
    }
    cl = colors.get(color_,'')
    if COLOR:
        return f"{cl}{txt}{colors['reset']}"
    else:
        return txt