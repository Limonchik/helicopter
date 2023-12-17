from events.EventController import EventController
from helicopter.HelicopterController import HelicopterController
from map.MapObjects import MapObjects
from map.fields.CloudsField import CloudsField
from map.fields.Field import Field
from map.fields.HelicopterPointsField import HelicopterPointsField
from map.fields.LakeField import LakeField
from map.fields.TreesField import TreesField


class Map:
    def __init__(self, width, height,
                 helicopter_controller: HelicopterController,
                 rendering_field,
                 event_controller: EventController,
                 generation_config
                 ):

        self.width = width
        self.height = height
        self.config = generation_config
        self.rendering_field = rendering_field
        self.helicopter_controller = helicopter_controller
        self.event_controller = event_controller

        self.clouds_field = CloudsField(width, height, event_controller=event_controller)
        self.lake_field = LakeField(width, height, event_controller=event_controller)
        self.trees_field = TreesField(width, height, event_controller=event_controller, generation_config=self.config)
        self.helicopter_points_field = HelicopterPointsField(width, height, event_controller=event_controller)

        self.composed_field = Field(width, height)
        # прикрепляем поля к прослушиванию изменений позиции вертолёта
        self._attach_fields_to_helicopter_controller()
        # устанавливаем функцию compose_fields в качестве колбека, который будет вызываться при изменении элементов в прикреплённых полях
        self.set_fields_callback(self.compose_fields)
        self.compose_fields()
        # генерируем начальные элементы карты
        self.generate_init_map_elems()
        # запускаем бесконечный цикл генерации новых элементов карты
        self.cycle_generation()

    def set_fields_callback(self, cb):
        """
        Устанавливает функцию, вызываемую при изменении элементов на полях
        :param cb: Функция
        """
        self.clouds_field.set_on_change(cb)
        self.lake_field.set_on_change(cb)
        self.trees_field.set_on_change(cb)

    def generate_init_map_elems(self):
        """
        Генерирует начальные элементы карты

        Генерирует озеро, госпиталь и магазин, деревья
        """
        self.lake_field.generate_random(self.config.lake_size, self.field_of_taken_elems())
        self.helicopter_points_field.generate_random_hospital(self.field_of_taken_elems())
        self.helicopter_points_field.generate_random_shop(self.field_of_taken_elems())
        self.trees_field.generate_random(
            self.config.tree_chance,
            self.field_of_taken_elems()
        )

    def cycle_generation(self):
        """
        Запускает рекурсию создания событий для генерации новых элементов карты
        """

        def generate_trees():
            """
            Генерирует два новых дерева на незанятых позициях

            Создаёт новое событие, которое через tree_generation_sec секунд так же выполнит текущую функцию
            """
            self.trees_field.generate_some(
                count=2,
                field_of_taken_elems=self.field_of_taken_elems()
            )
            self.event_controller.create_event_in(
                self.config.tree_generation_sec,
                generate_trees
            )

        def generate_clouds():
            """
            Генерирует новые облака на незанятых позициях

            Создаёт новое событие, которое через clouds_update_sec секунд так же выполнит текущую функцию
            """
            self.clouds_field.generate_random(
                self.config.clouds_quantity,
                self.config.lightning_chance,
                self.field_of_taken_elems()
            )
            self.event_controller.create_event_in(
                self.config.clouds_update_sec,
                generate_clouds
            )

        def generate_fire():
            """
            Генерирует пожары на клетках деревьев с шансом fire_chance

            Создаёт новое событие, которое через tree_generation_sec секунд так же выполнит текущую функцию
            """
            self.trees_field.generate_fires(self.config.fire_chance, self.helicopter_controller)
            self.event_controller.create_event_in(self.config.tree_generation_sec, generate_fire)

        # выполняем все функции выше, чтобы зациклить выполнение этих функций
        generate_fire()
        generate_trees()
        generate_clouds()

    def _attach_fields_to_helicopter_controller(self):
        """
        Добавляет все поля в список объектов, которые будут уведомлены при изменении позиции вертолёта

        В добавленных полях будет вызван метод handle_helicopter_pos
        """
        self.helicopter_controller.add_field_to_notify(self.clouds_field)
        self.helicopter_controller.add_field_to_notify(self.lake_field)
        self.helicopter_controller.add_field_to_notify(self.trees_field)
        self.helicopter_controller.add_field_to_notify(self.helicopter_points_field)

    def get_rendering_field(self):
        return self.rendering_field

    def _helicopter_change_pos(self, x, y):
        """
        Устанавливает новую позицию вертолёта, если её координаты не выходят за пределы текущего поля
        :param x: Позиция вертолёта по горизонтали
        :param y: Позиция вертолёта по вертикали
        """
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.helicopter_controller.set_position(x, y)
            self.compose_fields()

    def compose_fields(self):
        """
        Составляет из всех полей одно поле, в котором собраны элементы всех полей

        Список элементов результирующего поле задаёт полю для отображения RenderService'ом. При необходимости также добавляет элемент вертолёта на нужную позицию, если он в текущий момент времени виден
        """
        self.composed_field.empty()
        self._compose_field(self.lake_field)
        self._compose_field(self.clouds_field)
        self._compose_field(self.trees_field)
        self._compose_field(self.helicopter_points_field)
        self.rendering_field.set_elems(self.composed_field.get_elems())
        x, y = self.helicopter_controller.get_position()
        # Если вертолёт видимый, то переносим его элемент в rendering_field
        if self.is_helicopter_visible(x, y):
            self.rendering_field.set_elem(x, y, MapObjects.Helicopter)

    def is_helicopter_visible(self, x, y):
        """
        Проверяет виден ли вертолёт в текущий момент времени, в зависимости от текущего состояния ComposedField

        Если на позиции вертолёта не находятся элементы облака MapObjects.Cloud или молнии MapObjects.Lightning, то в текущий момент времени вертолёт виден и может быть отображён на rendering_field
        :param x: Позиция вертолёта по горизонтали
        :param y: Позиция вертолёта по вертикали
        :return: Виден ли вертолёт
        """
        composed_field = self.composed_field.get_elems()
        return composed_field[y][x] != MapObjects.Cloud and composed_field[y][x] != MapObjects.Lightning

    def _compose_field(self, field: Field):
        """
        Накладывает элементы поля field на поле composed_field
        :param field: Поле, элементы которого необходимо наложить
        """
        for y, row in enumerate(field.get_elems()):
            for x, el in enumerate(row):
                if el != MapObjects.Empty:
                    self.composed_field.set_elem(x, y, el)

    def field_of_taken_elems(self):
        """
        Создаёт двумерный список занятых элементом отображаемого поля.

        На месте незанятой позиции MapObjects.Empty будет 0, а на занятых позиция - 1
        :return: Двумерный список 0 и 1
        """
        taken_field = []

        for y, row in enumerate(self.rendering_field.get_elems()):
            taken_field.append([])
            for x, el in enumerate(row):
                taken_field[y].append(0 if el == MapObjects.Empty else 1)

        return taken_field

    def move_helicopter_down(self):
        x, y = self.helicopter_controller.get_position()
        self._helicopter_change_pos(x, y + 1)

    def move_helicopter_right(self):
        x, y = self.helicopter_controller.get_position()
        self._helicopter_change_pos(x + 1, y)

    def move_helicopter_up(self):
        x, y = self.helicopter_controller.get_position()
        self._helicopter_change_pos(x, y - 1)

    def move_helicopter_left(self):
        x, y = self.helicopter_controller.get_position()
        self._helicopter_change_pos(x - 1, y)
