from helicopter.HelicopterController import HelicopterController
from map.MapObjects import MapObjects
from map.fields.Field import Field
from utils import utils


class HelicopterPointsField(Field):
    def __init__(self, width, height, on_change=None, event_controller=None):
        super().__init__(width, height, on_change, event_controller)

    def generate_random_hospital(self, field_of_taken_elems: [[int]]):
        """
        В случайной пустой клетке генерирует госпиталь
        :param field_of_taken_elems:
        """
        self._generate_random_elem(field_of_taken_elems, MapObjects.Hospital)

    def generate_random_shop(self, field_of_taken_elems: [[int]]):
        """
        В случайной пустой клетке генерирует магазин
        :param field_of_taken_elems:
        """
        self._generate_random_elem(field_of_taken_elems, MapObjects.Shop)

    def _generate_random_elem(self, field_of_taken_elems: [[int]], elem: MapObjects):
        """
        В случайной пустой клетке генерирует заданный элемент elem
        :param field_of_taken_elems: двумерный список занятых позиций
        :param elem: генерируемый элемент
        """
        x, y = utils.random_cord(self.width, self.height)
        while not self.can_be_placed(x, y, field_of_taken_elems):
            x, y = utils.random_cord(self.width, self.height)
        self.set_elem(x, y, elem)

    def handle_helicopter_pos(self, helicopter_controller: HelicopterController, x, y):
        """
        Если игрок становится на клетку с магазином, то вызывается функция для покупки нового уровня бака
        Если игрок становится на клетку с госпиталем, то вызывается функция для пополнения очков здоровья
        :param helicopter_controller:
        :param x:
        :param y:
        """
        elem = self.get_elems()[y][x]
        if elem == MapObjects.Shop:
            helicopter_controller.buy_new_level()
        elif elem == MapObjects.Hospital:
            helicopter_controller.buy_health()
