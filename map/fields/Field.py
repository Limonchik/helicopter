import copy

from events.EventController import EventController
from helicopter.HelicopterController import HelicopterController
from map.MapObjects import MapObjects


class Field:
    elems: [MapObjects] = []

    # Двумерный список элементов определённого типа, где 0 - незаполненная ячейка, остальные значения -
    # элементы, относящиеся к этому типу

    def __init__(self, width, height, on_change=None, event_controller: EventController = None, elems=None,
                 generation_config=None):
        """
        :param width: Ширина поля
        :param height: Высота поля
        :param on_change: Колбек, которой будет вызван при изменении элементов поля
        :param event_controller: Контроллер событий
        :param elems: Начальные элементы поля
        """
        if elems is None:
            elems = []

        self.width = width
        self.height = height
        self.notification_callback = on_change
        self.event_controller = event_controller
        if generation_config is not None:
            self.config = generation_config

        self.empty()
        for y, row in enumerate(elems):
            for x, el in enumerate(row):
                self.elems[y][x] = el

    def set_on_change(self, cb):
        """
        Устанавливает колбек, который будет вызван при изменении элементов поля
        :param cb:
        """
        self.notification_callback = cb

    def empty(self):
        """
        Заполняет всё поле пустыми элементами MapObjects.Empty
        """
        self.fill(MapObjects.Empty)

    def fill(self, elem: MapObjects):
        """
        Заполняет всё поле заданным элементом
        :param elem: Элемент, который будет заполнено всё поле
        """
        elems = []
        for y in range(self.height):
            elems.append([])
            for x in range(self.height):
                elems[y].append(elem)
        self.set_elems(elems)

    def handle_helicopter_pos(self, helicopter_controller: HelicopterController, x, y):
        """
        Обрабатывает новую позицию вертолёта
        :param helicopter_controller:
        :param x:
        :param y:
        """
        pass

    def set_elem(self, x, y, elem):
        self.elems[y][x] = elem
        if self.notification_callback is not None:
            self.notification_callback()

    def set_elems(self, elems):
        self.elems = copy.deepcopy(elems)
        if self.notification_callback is not None:
            self.notification_callback()

    def get_elems(self):
        return self.elems

    @staticmethod
    def can_be_placed(x, y, field_of_taken_elems: [[int]]):
        """
        Проверяет занята ли эта позиция элементами других полей и может ли на это место быть задан новый элемент
        :param x:
        :param y:
        :param field_of_taken_elems:
        :return:
        """
        return field_of_taken_elems[y][x] == 0
