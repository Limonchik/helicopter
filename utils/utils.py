import random
import json
from os import system, name

from exceptions.IvanlidArgsException import InvalidArgsException


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def random_chance(chance):
    """
    Случайным образом возвращает True с шансом chance, в остальном случае возвращает False
    :param chance: шанс от 0 до 1, с которым выпадет True
    :return: boolean
    """
    return chance >= random.random()


def neighboring_cord(x, y, width, height):
    """
    На основе размеров поля и текущей координаты, выбирает случайную соседнюю клетку, гарантируя, что она не выходит за пределы поля
    :param x:
    :param y:
    :param width: ширина поля
    :param height: ширина высоты
    :return: координаты случайной соседней клетки
    """

    if not (0 <= x < width and 0 <= y < height):
        raise InvalidArgsException("Cords cannot be outside field")

    cords_arr = []

    # добавляем все координаты клеток, соседствующих с заданной клеткой, проверяя не выходят ли они за пределы поля
    if x == width - 1:
        cords_arr.append([x - 1, y])
    elif x == 0:
        cords_arr.append([x + 1, y])
    else:
        cords_arr.append([x - 1, y])
        cords_arr.append([x + 1, y])

    if y == height - 1:
        cords_arr.append([x, y - 1])
    elif y == 0:
        cords_arr.append([x, y + 1])
    else:
        cords_arr.append([x, y - 1])
        cords_arr.append([x, y + 1])

    # выбираем случайные координаты из списка соседних клеток
    return cords_arr[random.randint(0, len(cords_arr) - 1)]


def random_cord(width, height):
    """
    Генерирует координаты случайной клетки, гарантируя, что она находится в пределах поля
    :param width: ширина поля
    :param height: высота поля
    :return: координаты случайной клетки
    """
    return random.randint(0, width - 1), random.randint(0, height - 1)


def stringify_lists_in_dict(dictionary: dict):
    """
    Преобразовывает все списки в качестве значений в словаре в строки списков
    :param dictionary: словарь
    """
    # итерируем все ключи переданного списка
    for key in dictionary.keys():
        # если тип значения по этому ключу является списком, то преобразовываем это значение в строку
        if isinstance(dictionary[key], list):
            dictionary[key] = json.dumps(dictionary[key])
        # если тип значения по этому ключу является другим словарём, то вызываем эту же функцию для словаря
        elif isinstance(dictionary[key], dict):
            stringify_lists_in_dict(dictionary[key])
