class Player:
    def __init__(self, color):
        self.color = color
        self.salary = 5000

        self.dollars = 0
        self.life_points = 0
        self.unapplied_dollars = None
        self.unapplied_life_points = None

        self.married = False
        self.children = 0
        self.houses = []
        self.cars = []
        self.degrees = 0

    def earn_salary(self):
        self.dollars += self.salary

    def set_salary(self, salary):
        self.salary = int(salary)

    def get_assets(self):
        return {
            'dollars': self.dollars,
            'life points': self.life_points,
            'married': self.married,
            'children': self.children,
            'houses': self.houses,
            'cars': self.cars,
            'degrees': self.degrees,
        }

    def __str__(self):
        return self.color

    def _is_in_game(self, game) -> bool:
        return str(self) in [str(p) for p in game.players]
    
    def _update_dollars(self, delta=None):
        deltas = []
        if self.unapplied_dollars:
            deltas.append(self.unapplied_dollars)
        if delta:
            deltas.append(delta)
        self._update_integer_value(self.dollars, deltas)
        # if houses, cars, family, etc.; apply "interest" income or losses

    def _update_life_points(self, delta=None):
        deltas = []
        if self.unapplied_life_points:
            deltas.append(self.unapplied_life_points)
        if delta:
            deltas.append(delta)
        self._update_integer_value(self.life_points, deltas)
        # if houses, cars, family, etc.; apply "interest" income or losses
    
    def _update_integer_value(self, attrib, deltas):
        for delta in deltas:
            print(f"Updating {self.color=}: {attrib=}, {delta=}")
            attrib += delta
            print(f"Updataed {attrib=}")

class PlayerInvalidError(ValueError):
    pass


class PlayerTakenError(ValueError):
    pass