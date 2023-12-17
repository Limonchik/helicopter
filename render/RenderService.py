import string
import time

from config.Config import render_config
from events.EventController import EventController
from game_symbols.GameSymbols import GameSymbols
from helicopter.HelicopterController import HelicopterController
from map.fields.Field import Field
from utils.utils import clear


class RenderService:

    def __init__(self, rendering_field: Field,
                 event_controller: EventController,
                 helicopter_controller: HelicopterController,
                 symbols_dict: {string: string}):
        self.field = rendering_field
        self.symbols_dict = symbols_dict
        self.event_controller = event_controller
        self.event_loop = []
        self.helicopter_controller = helicopter_controller
        self.break_render = False

    def render(self):
        while True:
            # если флаг break_render равен true, то выходим из цикла рендера
            if self.break_render:
                break
            # делаем ререндер текущего тика
            self._rerender()
            # таким образом добиваемся, что у нас будет выполняться render_config.fps ФПС в секунду
            time.sleep(1 / render_config.fps)

    def stop_render(self):
        """
        Устанавливаем флаг для break_render на true, для обозначения конца рендера
        """
        self.break_render = True

    def _rerender(self):
        """
        Делает ререндер в консоль
        """
        # очищаем консоль
        clear()
        # выводим текущий тик
        print(self.event_controller.get_current_tick())
        # запускаем все события на текущем тики
        self.event_controller.run_events()
        # выводим статистику игрока
        self.print_helicopter_stats()
        # конвертируем объекты карты в эмодзи
        converted_elems = self.convert_field_elems_to_symbols(
            [[el.value for el in row] for row in self.field.get_elems()]
        )
        # выводим поле
        self.print_field(converted_elems)
        # инкрементируем тик
        self.event_controller.inc_tick()

    @staticmethod
    def print_field(elems):
        """
        Выводит двумерный список в консоль без разделителей
        :param elems:
        """
        for row in elems:
            print(''.join(row))

    def print_helicopter_stats(self):
        """
        Выводит текущую статистику игрока
        """
        print(self.convert_string_to_emoji(
            GameSymbols.Tank.value) + f": {self.helicopter_controller.get_current_tank_level()} / {self.helicopter_controller.get_tank_capacity()}")
        print(self.convert_string_to_emoji(
            GameSymbols.Heart.value) + f": {self.helicopter_controller.get_hp()} / {self.helicopter_controller.get_max_hp()}")
        print(self.convert_string_to_emoji(
            GameSymbols.Score.value) + f": {self.helicopter_controller.get_score()}")
        print(self.convert_string_to_emoji(
            GameSymbols.Money.value) + f": {self.helicopter_controller.get_money()}")

    def convert_field_elems_to_symbols(self, elems: [[string]]):
        """
        Конвертирует весь список элементов в эмодзи
        :param elems: двумерный список элементов
        :return:
        """
        converted_elems = []
        for i in range(len(elems)):
            converted_elems.append([])
            for el in elems[i]:
                converted_elems[i].append(self.convert_string_to_emoji(el))
        return converted_elems

    def convert_string_to_emoji(self, elem: string):
        """
        Пытается конвертировать символ в эмодзи, иначе возвращает начальную строку
        :param elem: строка конвертируемого элемента
        :return:
        """
        try:
            return self.symbols_dict[elem]
        except IndexError:
            return elem
