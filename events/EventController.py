class EventController:
    event_loop = {}
    current_tick = 0

    def __init__(self, render_config):
        self.fps = render_config.fps

    def create_event(self, tick, callback):
        """
        Создаёт событие, которое произойдёт через tick тиков
        :param tick:
        :param callback:
        """
        if str(tick) in self.event_loop:
            self.event_loop[str(tick)].append(callback)
            return
        self.event_loop[str(tick)] = [callback]

    def create_event_in(self, seconds, callback):
        """
        Создаёт событие, которое произойдёт через seconds секунд
        :param seconds:
        :param callback:
        """
        self.create_event(self.current_tick + int(seconds * self.fps), callback)

    def run_events(self):
        """
        Выполняет все добавленные события в event_loop в текущий тик current_tick
        """
        tick = self.current_tick
        if not str(tick) in self.event_loop:
            return
        for callback in self.event_loop[str(tick)]:
            callback()
        del self.event_loop[str(tick)]

    def get_current_tick(self):
        return self.current_tick

    def inc_tick(self):
        """
        Инкрементирует текущий тик current_tick
        """
        self.current_tick += 1
