from random import randint


class Player:
    def __init__(self, game, color):
        self.game = game
        self.actions = {
            'roll':  self._do_turn,
            'update-dollars': self._update_dollars,
            'update-life-points': self._update_life_points,
            'done': self._end,
        }
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

        self.turns_taken = 0

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

    def play(self):
        self.__end = False
        while self.__end is not True:
            action = self.game.ask_player_action(self)
            func = self.actions.get(action)
            func()

    def __str__(self):
        return self.color

    def _do_turn(self):
        if self.turns_taken == self.game.current_round:
            self.game.show_info(f"{str(self)} already played this round.")
            return

        self._update_dollars(auto=True)
        self._update_life_points(auto=True)
        
        roll_result = self._roll()
        self.turns_taken += 1
        self.earn_salary()
        self.game.show_assets(self)

        self.game.show_info(f"You rolled '{roll_result}'")

    def _is_in_game(self, game) -> bool:
        return str(self) in [str(p) for p in game.players]

    def _end(self):
        self.__end = True

    def _roll(self):
        # TODO: Change 'min' depending on car ownership.
        min = 1
        return randint(min, 10)

    def _update_dollars(self, auto=False):
        if auto is False:
            value = int(self.game._ask_value("+ or - how many dollars?"))
            self.dollars += value
            self.game.show_assets(self)
        else:
            # if houses, cars, family, etc.; apply "interest" income or losses
            pass

    def _update_life_points(self, auto=False):
        if auto is False:
            value = int(self.game._ask_value("+ or - how many life points?"))
            self.life_points += value
            self.game.show_assets(self)
        else:
            # if houses, cars, family, etc.; apply "interest" income or losses
            pass


class PlayerInvalidError(ValueError):
    pass


class PlayerTakenError(ValueError):
    pass