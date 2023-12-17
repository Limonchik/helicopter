from helicopter.HelicopterController import HelicopterController
from map.MapObjects import MapObjects
from map.fields.Field import Field
from utils import utils


class TreesField(Field):
    def __init__(self, width, height, on_change=None, event_controller=None, generation_config=None):
        super().__init__(width, height, on_change, event_controller, generation_config=generation_config)

    def generate_random(self, tree_chance, field_of_taken_elems: [[int]]):
        """
        Генерирует деревья на свободных клетках с шансом chance
        :param tree_chance: шанс генерации дерева
        :param field_of_taken_elems: двумерный список занятых клеток
        """
        self.empty()

        for y, row in enumerate(field_of_taken_elems):
            for x, el in enumerate(row):
                if self.can_be_placed(x, y, field_of_taken_elems) and utils.random_chance(tree_chance):
                    self.set_elem(x, y, MapObjects.Tree)

    def generate_fires(self, chance, helicopter_controller: HelicopterController):
        """
        На месте клеток, занятых деревьями MapObjects.Tree, генерирует пожары с шансом chance

        Создаёт события, которое через fire_duration_sec вызовет функцию process_fire с helicopter_controller.decrement_hp в качестве аргумента
        :param chance:
        :param helicopter_controller:
        """
        for y, row in enumerate(self.get_elems()):
            for x, el in enumerate(row):
                if el == MapObjects.Tree and utils.random_chance(chance):
                    self.set_elem(x, y, MapObjects.Fire)
                    self.event_controller.create_event_in(
                        self.config.fire_duration_sec,
                        lambda _x=x, _y=y: self.process_fire(_x, _y, helicopter_controller.decrement_hp)
                    )

    def generate_some(self, count, field_of_taken_elems: [[int]]):
        """
        На случайных незанятых клетках генерирует count количество деревьев
        :param count: необходимое количество сгенерированных деревьев
        :param field_of_taken_elems:
        """
        while count > 0:
            x, y = utils.random_cord(self.width, self.height)
            if field_of_taken_elems[y][x] == 0:
                self.set_elem(x, y, MapObjects.Tree)
                count -= 1

    def handle_helicopter_pos(self, helicopter_controller, x, y):
        """
        Если игрок стал на клетку с пожаром и у него достаточное количество воды в баке,
        элемент огня MapObjects.Fire заменяется деревом MapObjects.Tree и
        вызывается функция обработки тушения пожара у helicopter_controller.fire_extinguishing()
        :param helicopter_controller:
        :param x:
        :param y:
        """
        current_field = self.get_elems()
        if current_field[y][x] == MapObjects.Fire and helicopter_controller.get_current_tank_level() > 0:
            self.set_elem(x, y, MapObjects.Tree)
            helicopter_controller.fire_extinguishing()

    def process_fire(self, x, y, on_burn_out=None):
        """
        Если в ячейке с координатами x, y элемент огня MapObjects.Fire, заменяет его пустой клеткой и
        вызывает колбек on_burn_out если он передан аргументом
        :param x:
        :param y:
        :param on_burn_out: callback
        """
        elems = self.get_elems()
        if elems[y][x] == MapObjects.Fire:
            self.set_elem(x, y, MapObjects.Empty)
            if on_burn_out is not None:
                on_burn_out()
