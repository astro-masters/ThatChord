import settings
from errors import err
import interpret
import find
import custom


def init_settings(instrument='guitar', ranking='guitar', format='text', output='splash', tuning='E A D G B E'):
    override = {
        "instrument_preset": instrument,
        "ranking_preset": ranking,
        "output_format": format,
        "output_method": output,
        "tuning": tuning,
    }

    return settings.get_settings(**override)


def prepare_request(request: str, settings):
    tcsettings = settings[0]
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

    return {
        "chord": chord,
        "title": title,
        "filename": filename,
        "listpos": listpos,
        "at": at,
    }


# #tuning='D G D G B D'
# setup = init_settings(
#     tuning='D G D G B D'
# )
# tcsettings = setup[0]
# print(f'========== settings ==========\n{tcsettings}')
#
# chord_shapes = []
#
# for fret in range(9):
#     chord_fret = f'E7@{fret}'
#
#     for i in range(5):
#         chord = f'{chord_fret}:{i + 1}'
#         request = prepare_request(chord, setup)
#         print(f'========== request ==========\n{request}')
#         solution = find.find(request['chord'],
#                              nmute=tcsettings["nmute"],
#                              important=tcsettings["important"],
#                              index=request['listpos'],
#                              nfrets=tcsettings["nfrets"],
#                              tuning=tcsettings["tuning"],
#                              order=tcsettings["order"],
#                              ranks=tcsettings["ranks"],
#                              stringstarts=tcsettings["stringstarts"],
#                              fretspec=request['at'])
#         chord_shapes.append(solution)
#
# unique_shapes = []
# seen = set()
# for shape in chord_shapes:
#     t = tuple(shape)
#     if t not in seen:
#         unique_shapes.append(shape)
#         seen.add(t)
#
# print(f'========== solution ==========\n{unique_shapes}')

# request = prepare_request('C', setup)
# print(f'========== request ==========\n{request}')
# solution = find.find(request['chord'],
#                      nmute=tcsettings["nmute"],
#                      important=tcsettings["important"],
#                      index=request['listpos'],
#                      nfrets=tcsettings["nfrets"],
#                      tuning=tcsettings["tuning"],
#                      order=tcsettings["order"],
#                      ranks=tcsettings["ranks"],
#                      stringstarts=tcsettings["stringstarts"],
#                      fretspec=request['at'])
#
# print(f'========== solution ==========\n{solution}')
