import copy
import os
import string
from configparser import ConfigParser

import configdot

from utils.utils import stringify_lists_in_dict


def write_config(configparser: ConfigParser, filepath: string):
    with open(filepath, 'w') as file:
        configparser.write(file)


def read_config(configparser: ConfigParser, filepath: string):
    with open(filepath, 'r') as file:
        configparser.read_file(file)


def get_config(default_config: dict, filepath):
    # копируем словарь
    config_dict = copy.deepcopy(default_config)

    # преобразовываем все списки в словаре в json-строку
    stringify_lists_in_dict(config_dict)

    # создаём объект конфига
    config = ConfigParser()

    # читаем из словаря все ключи-значения
    config.read_dict(config_dict)

    # если файл конфига уже существует, то перезаписываем дефолтные значения значениями из файла
    if not os.path.exists(filepath):
        write_config(config, filepath)
    else:
        # записываем получившийся конфиг объект в файл
        read_config(config, filepath)
        write_config(config, filepath)

    config = configdot.parse_config(filepath)
    return config
