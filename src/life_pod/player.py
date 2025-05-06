from random import randint


class Player:
    def __init__(self, game, name):
        self.game = game
        self.actions = {
            'roll':  self.do_turn,
            'update-dollars': self.update_dollars,
            'update-life-points': self.update_life_points,
            'done': self._end,
        }
        # self.update_operator = None  # +/-
        self.name = name
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
            'cars': self.cars,
            'houses': self.houses,
            'children': self.children,
            'married': self.married,
            'dollars': self.dollars,
            'life points': self.life_points,
        }

    def play_loop(self):
        self.__end = False
        while self.__end is not True:
            action = self.game.ask_player_action(self)
            func = self.actions.get(action)
            func()

    def __str__(self):
        return self.name

    def do_turn(self):
        print(f"{self.game.current_round=}; player: {self}; {self.turns_taken=}")
        if self.game.current_round > self.game.length:
            # Game over; show assets.
            self.game.show_assets(self)
            return

        if self.turns_taken == self.game.current_round:
            # Player already played.
            self.game.show_error(f"{self} already played")
            return

        self.update_dollars()
        self.update_life_points()
        
        roll_result = self._roll()
        self.turns_taken += 1
        self.earn_salary()
        self.game.show_assets(self)

        self.game.show_info(f"You rolled \"{roll_result}\"")

    def _is_in_game(self, game) -> bool:
        return str(self) in [str(p) for p in game.players]

    def _end(self):
        self.__end = True

    def _roll(self):
        # TODO: Change 'min' depending on car ownership.
        min = 1
        return randint(min, 10)

    def update_dollars(self, value=None):
        if value:
            # value = int(self.game._ask_value("+ or - how many dollars?"))
            
            self.dollars += value
            self.game.show_assets(self)
        else:
            # if houses, cars, family, etc.; apply "interest" income or losses
            pass

    def update_life_points(self, value=None):
        if value:
            # value = int(self.game._ask_value("+ or - how many life points?"))
            self.life_points += value
            self.game.show_assets(self)
        else:
            # if houses, cars, family, etc.; apply "interest" income or losses
            pass


class PlayerInvalidError(ValueError):
    pass


class PlayerTakenError(ValueError):
    pass