class Helicopter:
    def __init__(self, x, y, helicopter_config):
        self.x = x
        self.y = y
        self.money = 0
        self.max_hp = helicopter_config.max_health
        self.current_hp = self.max_hp
        self.score = 0
        self.tank_capacity = helicopter_config.initial_max_tank_capacity
        self.current_tank_level = helicopter_config.initial_tank_capacity
        self.current_level = 0
        self.current_heals = 0
        self.can_refill_tank = True

    def set_pos(self, x, y):
        self.x = x
        self.y = y
