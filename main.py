from map.Map import Map
from map.fields.Field import Field
from helicopter.HelicopterController import HelicopterController
from events.EventController import EventController
from input.InputController import InputController
from render.RenderService import RenderService
from config.Config import helicopter_config, render_config, emoji_config, generation_config, keybindings_config

from utils.utils import clear


class HelicopterGame:
    def __init__(self):

        field_width = generation_config.field_size
        field_height = generation_config.field_size

        self.helicopter_controller = HelicopterController(
            field_width,
            field_height,
            self.game_lost,
            helicopter_config
        )

        self.rendering_field = Field(
            field_width,
            field_height
        )
        self.event_controller = EventController(render_config)
        self.map = Map(
            field_width,
            field_height,
            self.helicopter_controller,
            self.rendering_field,
            self.event_controller,
            generation_config
        )
        self.render_service = RenderService(
            self.rendering_field,
            self.event_controller,
            self.helicopter_controller,
            emoji_config
        )
        self.input_controller = InputController()
        self.set_controls()
        self.render_service.render()

    def game_lost(self):
        """
        Останавливает рендер поля и выводит итоговый счёт игрока
        """
        self.render_service.stop_render()
        clear()
        print("Game lost, your score: " + str(self.helicopter_controller.get_score()))
        exit(0)

    def set_controls(self):
        """
        Устанавливает колбеки управления вертолётом для клавиш управления, заданных в keybindings_config
        """
        for key in keybindings_config.move_up:
            self.input_controller.add_key_event(key, self.map.move_helicopter_up)

        for key in keybindings_config.move_down:
            self.input_controller.add_key_event(key, self.map.move_helicopter_down)

        for key in keybindings_config.move_left:
            self.input_controller.add_key_event(key, self.map.move_helicopter_left)

        for key in keybindings_config.move_right:
            self.input_controller.add_key_event(key, self.map.move_helicopter_right)


HelicopterGame()
