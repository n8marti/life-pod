class Asset:
    def __init__(self):
        self.name = 'asset'
        self.value = None
        self.life_points_modifier = None

    def __str__(self):
        return self.name

    def do_turn(self):
        self._update_value()

    def _update_value(self):
        raise NotImplementedError


class Car(Asset):
    ECONOMY = 'economy-car'
    SPORTS = 'sports-car'


class EconomyCar(Car):
    def __init__(self):
        self.name = self.ECONOMY
        self.value = 10000
        self.life_points_modifier = 100
        self.salary_reduction = 0.1
        self.roll_modifier = 1
        self.value_modifier = -1000

    def _update_value(self):
        self.value = max([self.value + self.value_modifier, 0])


class SportsCar(Car):
    def __init__(self):
        self.name = self.SPORTS
        self.value = 50000
        self.life_points_modifier = 200
        self.salary_reduction = 0.1
        self.roll_modifier = 2
        self.value_modifier = -5000
        self.age = 0
        
    def do_turn(self):
        self._add_year()
        self._update_value()

    def _add_year(self):
        self.age += 1

    def _update_value(self):
        if self.age < 15:
            self.value = max([self.value + self.value_modifier, 0])
        else:
            self.value += (-1 * self.value_modifier)  # reverse modifier sign


class House(Asset):
    MODEST = 'modest-house'
    MIDSIZED = 'midsized-house'
    MANSION = 'mansion-house'

    def _update_value(self):
        self.value = int(round(self.value * self.value_modifier, 0))


class ModestHouse(House):
    def __init__(self):
        self.name = self.MODEST
        self.life_points_modifier = 100
        self.value_modifier = 1.06
        self.value = 200_000


class MidSizedHouse(House):
    def __init__(self):
        self.name = self.MIDSIZED
        self.life_points_modifier = 100
        self.value_modifier = 1.06
        self.value = 500_000


class Mansion(House):
    def __init__(self):
        self.name = self.MANSION
        self.life_points_modifier = 100
        self.value_modifier = 1.06
        self.value = 1_000_000
