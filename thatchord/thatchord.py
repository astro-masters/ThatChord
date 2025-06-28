###############################################################################
###############################################################################
##                                                                           ##
##  THATCHORD ОТ ТОМА КОНТИ-ЛЕСЛИ                             thatchord.py  ##
##                                                                           ##
##  ЭТОТ ФАЙЛ ОБЪЕДИНЯЕТ ВСЕ ПОДПРОЦЕССЫ ИЗ ДРУГИХ ФАЙЛОВ И ЗАПУСКАЕТ THATCHORD  ##
##  Вы можете изменить строку "request" в этом файле, и это повлияет на     ##
##  работу, если в settings.py установлен input_type=DIRECT. Остальной код  ##
##  в этом файле менять не следует.                                         ##
##                                                                           ##
##                                                                           ##
##  Лицензия: CC BY-SA 4.0                                                  ##
##                                                                           ##
##  Контакты: tom (dot) contileslie (at) gmail (dot) com                     ##
##                                                                           ##
###############################################################################
###############################################################################

############             ВВЕДИТЕ ВАШ ЗАПРОС АККОРДА ЗДЕСЬ         ############

# --------------------------------------------------------------------------- #
#request = "Gadd9"
# --------------------------------------------------------------------------- #

import typer
from rich.console import Console

from . import interpret
from . import find
from . import output
from . import custom
from . import settings
from .errors import err

console = Console()

app = typer.Typer()

@app.command()
def main(
    request: Annotated[str, typer.Argument(help="Requested chord in WX(Y)/Z:T format")],
    configuration: Annotated[
        str,
        typer.Option(
            "-c", "--configuration", help="YAML file to load settings from"
        ),
    ] = None,
    instrument: Annotated[
        str, typer.Option("-i", "--instrument", help="Instrument preset")
    ] = None,
    ranking: Annotated[
        str, typer.Option("-r", "--ranking", help="Ranking preset")
    ] = None,
    format: Annotated[
        str, typer.Option("-f", "--format", help="Output format: text or png")
    ] = None,
    output_method: Annotated[
        str, typer.Option("-o", "--output", help="Output method: print, splash or none")
    ] = None,
    save: Annotated[
        str, typer.Option("-s", "--save", help="Save method: single, library or none")
    ] = None,
    directory: Annotated[
        str, typer.Option("-d", "--directory", help="Directory to save diagrams")
    ] = None,
):
    # Загрузка настроек из файла. Все значения по умолчанию здесь.
    override = {
        "instrument_preset": instrument,
        "ranking_preset": ranking,
        "output_format": format,
        "output_method": output_method,
        "save_method": save,
        "save_loc": directory,
    }
    if configuration:
        override["settingsfile"] = configuration

    tcsettings, kwgrargs, kwioargs = settings.get_settings(**override)

    # Специальные команды:
    if request.upper() == "SETTINGS":
        # Ввод SETTINGS открывает файл настроек.
        script_directory = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join(script_directory, "settings.yml")
        if platform.system() == "Linux":
            os.system("xdg-open " + settings_path)
        else:
            os.system("open " + settings_path)
        exit()

    # Проверка запрошенной позиции в списке. По умолчанию 1 (лучший вариант).
    listpos = 1

    if ":" in request:
        colon_positions = [i for i, x in enumerate(request) if x == ":"]
        if len(colon_positions) > 1:
            err("colons")
        # если дошли сюда, должна быть ровно одна двоеточие
        try:
            listpos = int(request[colon_positions[0] + 1:])
        except ValueError:
            err(15)
        # удаляем часть с двоеточием из запроса
        request = request[:colon_positions[0]]

    # Проверка указания минимального лада (fretspec).
    at = 0

    if "@" in request:
        at_positions = [i for i, x in enumerate(request) if x == "@"]
        if len(at_positions) > 1:
            err("ats")
        # если дошли сюда, должна быть ровно одна @
        try:
            at = int(request[at_positions[0] + 1:])
        except ValueError:
            err(22)
        # удаляем часть с @ из запроса
        request = request[:at_positions[0]]
    if at > tcsettings["nfrets"]:
        err(23)

    if request[0:6].upper() == "CUSTOM":
        # активирован пользовательский ввод. Код в "custom.py".
        chord = custom.interpret(request[6:])
        # название удаляет CUSTOM, но добавляет ! для обозначения кастомного
        title = "!" + request[6:]
        filename = request
    else:
        # Стандартный ввод. Используем обычную функцию.
        chord = interpret.interpret(request)
        # Название и имя файла аккорда (для возможного вывода) - строка запроса.
        title = request
        filename = request

    # Находим аккорд в запрошенной позиции списка.
    solution = find.find(chord,
                         nmute=tcsettings["nmute"],
                         important=tcsettings["important"],
                         index=listpos,
                         nfrets=tcsettings["nfrets"],
                         tuning=tcsettings["tuning"],
                         order=tcsettings["order"],
                         ranks=tcsettings["ranks"],
                         stringstarts=tcsettings["stringstarts"],
                         fretspec=at)

    # определяем формат вывода
    if tcsettings["output_format"] == "TEXT":
        output.text(
            solution,
            name=filename,
            title=title,
            **kwgrargs,
            **kwioargs
        )

    # TODO: нет опций для размещения названия
    elif tcsettings["output_format"] == "PNG":
        output.img(
            solution,
            name=filename,
            title=title,
            **kwgrargs,
            **kwioargs
        )

if __name__ == "__main__":
    app()
