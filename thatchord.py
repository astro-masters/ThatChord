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
request = "Gadd9"
# --------------------------------------------------------------------------- #


# НЕ МЕНЯЙТЕ СЛЕДУЮЩИЙ КОД. ЗДЕСЬ ПРОИСХОДИТ ВСЯ МАГИЯ.

# смена текущей директории
import os
import platform  # Для различия платформ

# Загрузка других файлов
import interpret
import find
import rank
import output
import custom
import settings
from errors import err

# Загрузка настроек из файла. Все значения по умолчанию здесь.
tcsettings, kwgrargs, kwioargs = settings.get_settings()

# Сначала определим, что представляет собой запрос.
if tcsettings["input_type"] == "CONSOLE":
    request = input("Введите запрос здесь: ")
elif tcsettings["input_type"] == "TERMINAL":
    import sys
    import argparse

    # Терминальный ввод позволяет использовать параметры командной строки.
    parser = argparse.ArgumentParser(prog="thatchord.py",
                                     usage=("python3 thatchord.py <запрос> " +
                                            "[ОПЦИИ]"))

    parser.add_argument("request", nargs=1, type=str,
                        help=("запрошенный аккорд в формате WX(Y)/Z:T, " +
                              "где W - основная нота, " +
                              "X - качество аккорда, " +
                              "Y - список изменений, " +
                              "Z - басовая нота, " +
                              "и T - желаемая позиция в списке"))

    parser.add_argument("-c", "--configuration", nargs="?", type=str,
                        help=("файл .yml для загрузки настроек; его настройки" +
                              " могут быть переопределены опциями ниже"))

    parser.add_argument("-i", "--instrument", nargs="?", type=str,
                        help="пресет инструмента")

    parser.add_argument("-r", "--ranking", nargs="?", type=str,
                        help="пресет ранжирования")

    parser.add_argument("-f", "--format", nargs="?", type=str,
                        help="формат вывода: text или png")

    parser.add_argument("-o", "--output", nargs="?", type=str,
                        help="метод вывода: print, splash или none")

    parser.add_argument("-s", "--save", nargs="?", type=str,
                        help="метод сохранения: single, library или none")

    parser.add_argument("-d", "--directory", nargs="?", type=str,
                        help="директория для сохранения диаграмм")

    args = parser.parse_args()

    request = args.request[0]

    # заполнение словаря параметрами
    override = {"instrument_preset": args.instrument,
                "ranking_preset": args.ranking,
                "output_format": args.format,
                "output_method": args.output,
                "save_method": args.save,
                "save_loc": args.directory}
    if args.configuration:
        override["settingsfile"] = args.configuration

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
