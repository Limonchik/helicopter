from pynput import keyboard


class InputController:

    def __init__(self):
        self._keys_callbacks = {}

        listener = keyboard.Listener(
            on_press=self.press_func)
        listener.start()

    def press_func(self, key):
        """
        Вызывает все обработчики события, заданные для нажатия на переданную клавишу key
        :param key: Нажатая клавиша
        """
        try:
            if key.char in self._keys_callbacks:
                for callback in self._keys_callbacks[key.char]:
                    callback()
        except AttributeError:
            pass

    def add_key_event(self, key, callback):
        """
        Добавляет новый колбек, которые будет вызван при нажатии на заданную клавишу
        :param key: Клавиша для которой будет сработан обработчик события
        :param callback: Колбек
        """
        if key in self._keys_callbacks:
            self._keys_callbacks[key] = self._keys_callbacks[key] + callback
        else:
            self._keys_callbacks[key] = [callback]
