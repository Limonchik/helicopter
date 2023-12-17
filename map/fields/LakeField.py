from helicopter.HelicopterController import HelicopterController
from map.MapObjects import MapObjects
from map.fields.Field import Field
from utils import utils


class LakeField(Field):
    def __init__(self, width, height, on_change=None, event_controller=None):
        super().__init__(width, height, on_change, event_controller)

    def generate_random(self, lake_size, field_of_taken_elems: [[int]]):
        """
        Генерирует озеро определённого размера в случайном месте карты

        Генерирует клетку озера на случайной незанятой позиции на карте и на случайной клетке,
        соседней последней сгенерированной, до тех пор,
        пока общее количество клеток воды на карте не будет равным заданному размеру озера lake_size
        :param lake_size: размер генерируемого озера
        :param field_of_taken_elems: двумерный список занятых элементов
        """
        self.empty()
        counter = 0
        # генерируем первую клетку озера на случайной позиции
        x, y = utils.random_cord(self.width, self.height)
        # если эта позиция занята, то генерируем каждый раз новые координаты до тех пор, пока не найдём свободную клетку
        while not self.can_be_placed(x, y, field_of_taken_elems):
            x, y = utils.random_cord(self.width, self.height)
        self.set_elem(x, y, MapObjects.Lake)
        # генерируем новые элементы озера до тех пор, пока их количество не превышает lake_size
        while counter < lake_size:
            # генерируем координаты случайной клетки соседствующей текущей позиции x, y
            x_new, y_new = utils.neighboring_cord(x, y, self.width, self.height)
            # проверяем свободна ли клетка на новой позиции
            if self.can_be_placed(x, y, field_of_taken_elems):
                counter += 1
                self.set_elem(x, y, MapObjects.Lake)
                # новые координаты, вокруг которых будет генерироваться следующая клетка
                x, y = x_new, y_new

    def handle_helicopter_pos(self, helicopter_controller: HelicopterController, x, y):
        """
        Если игрок встал на ячейку с водой, то его бак будет пополнен

        Проверяет, может ли в текущий момент времени вертолёт набирать воду can_refill().
        Набирает воду и устанавливает флаг can_refill на false. Через cooldown_fill_tank_sec секунд проверяет, остался ли игрок на прежней клетке, и в таком случае рекурсивно выполняет текущую функцию.
        :param helicopter_controller:
        :param x:
        :param y:
        """
        # получаем текущую позицию вертолёта
        cur_x, cur_y = helicopter_controller.get_position()
        # из объекта настроек получаем cooldown на заполнение бака
        cooldown = helicopter_controller.config.cooldown_fill_tank_sec
        # сверяем текущую позицию вертолёта с той, которая была передана функции
        # проверяем может ли в текущий момент вертолёт набрать бак
        if (x == cur_x and y == cur_y
                and self.get_elems()[y][x] == MapObjects.Lake
                and helicopter_controller.can_refill()):
            helicopter_controller.fill_tank()
            # устанавливаем флаг can_refill на false, что означает, что вертолёт не может мгновенно ещё раз набрать бак
            helicopter_controller.set_can_refill(False)
            # создаём событие на установку can_refill на true через cooldown секунд, позволяя вертолёту снова набрать бак
            self.event_controller.create_event_in(
                cooldown,
                lambda: helicopter_controller.set_can_refill(True)
            )
            # создаём событие, которое проверит, остался ли вертолёт на прежней позиции и ещё раз наберёт бак
            self.event_controller.create_event_in(
                cooldown + 0.1,
                lambda _x=x, _y=y: self.handle_helicopter_pos(helicopter_controller, _x, _y)
            )
