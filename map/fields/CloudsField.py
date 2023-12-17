from map.MapObjects import MapObjects
from map.fields.Field import Field
from utils import utils


class CloudsField(Field):

    def __init__(self, width, height, on_change=None, event_controller=None):
        super().__init__(width, height, on_change, event_controller)

    def generate_random(self, quantity, lightning_chance, field_of_taken_elems: [[int]]):
        """
        Генерирует нужное количество облаков основываясь на списке занятых элементов
        :param lightning_chance:
        :param quantity:
        :param field_of_taken_elems:
        :return:
        """
        self.empty()
        counter = 0
        while counter < quantity:
            counter += self._generate_one_random(field_of_taken_elems)
        self.generate_lightning(lightning_chance)

    def _generate_one_random(self, field_of_taken_elems: [[int]]):
        """
        Если облако было успешно создано, то возвращает 1, иначе 0
        :return: 1 или 0
        """
        x, y = utils.random_cord(self.width, self.height)
        if self.can_be_placed(x, y, field_of_taken_elems):
            self.set_elem(x, y, MapObjects.Cloud)
            return 1
        return 0

    def generate_lightning(self, chance):
        """
        Генерирует на позициях облаков MapObjects.Cloud с шансом chance молнии MapObjects.Lightning
        :param chance: Шанс, с которым будет сгенерирована молния на месте облака
        """
        for y, row in enumerate(self.get_elems()):
            for x, el in enumerate(row):
                if el == MapObjects.Cloud and utils.random_chance(chance):
                    self.set_elem(x, y, MapObjects.Lightning)

    def handle_helicopter_pos(self, helicopter_controller, x, y):
        """
        Если игрок становится на клетку с молнией, то у него снимаются очки здоровья
        :param helicopter_controller:
        :param x:
        :param y:
        """
        if self.get_elems()[y][x] == MapObjects.Lightning:
            helicopter_controller.decrement_hp()
