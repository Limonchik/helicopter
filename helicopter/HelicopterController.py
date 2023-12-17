from helicopter.Helicopter import Helicopter


class HelicopterController:
    def __init__(self, field_width: int, field_height: int, game_lost_cb, helicopter_config):
        self.config = helicopter_config
        self.helicopter = Helicopter(field_width // 2, field_height // 2, self.config)
        self.field_width = field_width
        self.field_height = field_height
        self.fields_to_notify = []
        self.game_lost_cb = game_lost_cb

    def set_position(self, x, y):
        self.helicopter.set_pos(x, y)
        self._notify_fields()

    def get_position(self):
        return self.helicopter.x, self.helicopter.y

    def _notify_fields(self):
        """
        Вызывает у всех полей в списке fields_to_notify метод handle_helicopter_pos, передавая аргументом новую позицию вертолёта и текущий объект HelicopterController
        Таким образом уведомляет все поля об изменении позиции вертолёта
        """
        x, y = self.get_position()
        for field in self.fields_to_notify:
            field.handle_helicopter_pos(self, x, y)

    def add_field_to_notify(self, field):
        """
        Добавляет необходимое поле, которое в дальнейшем будет уведомлено при изменении позиции вертолёта
        :param field: объект класса Field и его подклассы
        """
        self.fields_to_notify.append(field)

    def get_hp(self):
        return self.helicopter.current_hp

    def get_max_hp(self):
        return self.helicopter.max_hp

    def get_money(self):
        return self.helicopter.money

    def get_score(self):
        return self.helicopter.score

    def get_current_tank_level(self):
        return self.helicopter.current_tank_level

    def get_tank_capacity(self):
        return self.helicopter.tank_capacity

    def decrement_hp(self):
        if self.helicopter.current_hp > 1:
            self.helicopter.current_hp -= 1
        else:
            self.game_lost_cb()

    def decrease_tank_level(self, amount):
        """
        Уменьшает количество воды в баке на заданное количество. Если передано количество воды, большее, чем текущий уровень бака, то устанавливает уровень воды в баке на 0
        :param amount: Количество воды, на которое необходимо снизить запас воды в баке
        """
        self.helicopter.current_tank_level -= amount
        if self.helicopter.current_tank_level < 0:
            self.helicopter.current_tank_level = 0

    def add_score(self, amount):
        self.helicopter.score += amount

    def add_money(self, amount):
        self.helicopter.money += amount

    def fire_extinguishing(self):
        """
        Уменьшает запас бака на то количество воды, равное необходимому для тушения пожара. Добавляет деньги и опыт игроку
        """
        self.decrease_tank_level(self.config.extinguishing_water_cost)
        self.add_money(self.config.extinguishing_monetary_reward)
        self.add_score(self.config.extinguishing_score_reward)

    def fill_tank(self):
        """
        Пополняет бак вертолёта на количество воды, равное начальному уровню максимального запаса воды вертолёта
        """
        self.helicopter.current_tank_level += self.config.initial_tank_capacity
        if self.helicopter.current_tank_level > self.helicopter.tank_capacity:
            self.helicopter.current_tank_level = self.helicopter.tank_capacity

    def buy_new_level(self):
        """
        Увеличивает уровень бака вертолёта, если у него достаточно денег для покупки улучшения
        """

        next_level = self.helicopter.current_level + 1
        next_level_price = self.config.initial_levelup_money_cost * pow(2, self.helicopter.current_level)
        if self.get_money() >= next_level_price:
            self.helicopter.tank_capacity += self.config.initial_tank_capacity
            self.helicopter.money -= next_level_price
            self.helicopter.current_level = next_level

    def buy_health(self):
        """
        Пополняет здоровье игроку, если у него достаточно денег для покупки здоровья
        """
        next_heal = self.helicopter.current_heals + 1
        next_heal_price = self.config.initial_heal_money_cost * pow(2, self.helicopter.current_heals)
        if self.get_money() >= next_heal_price:
            self.helicopter.current_hp = self.helicopter.max_hp
            self.helicopter.money -= next_heal_price
            self.helicopter.current_heals = next_heal

    def set_can_refill(self, flag: bool):
        self.helicopter.can_refill_tank = flag

    def can_refill(self):
        """
        Может ли вертолёт пополнить бак
        """
        return self.helicopter.can_refill_tank
