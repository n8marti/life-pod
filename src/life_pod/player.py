from random import randint

from . import assets as a


class Player:
    def __init__(self, game, name):
        self.game = game
        self.actions = {
            'roll':  self.do_turn,
            'update-dollars': self.update_dollars,
            'update-life-points': self.update_life_points,
            'done': self._end,
        }
        self.name = name
        self.salary = 5000
        self.salary_reduction = None

        self.dollars = 0
        self.life_points = 0

        self.married = False
        self.babies = 0
        self.assets = []

        self.turns_taken = 0

    def buy(self, name):
        print(f"buying: {name}")
        match name:
            case 'economy-car':
                asset = a.EconomyCar()
            case 'sports-car':
                asset = a.SportsCar()
            case 'modest-house':
                asset = a.ModestHouse()
            case 'midsized-house':
                asset = a.MidSizedHouse()
            case 'mansion-house':
                asset = a.Mansion()
        self.dollars -= asset.value
        self.assets.append(asset)

    def sell(self, name):
        asset = self._retrieve_asset(name)
        self.dollars += asset.value

    def convert_assets(self, factor):
        self._convert_dollars(factor)

    def earn_salary(self):
        if self.salary_reduction is not None:
            salary = self.salary - self.salary_reduction
        else:
            salary = self.salary
        self.dollars += salary

    def set_salary(self, salary):
        self.salary = int(salary)

    def get_assets(self):
        return {
            'cars': self._get_cars(),
            'houses': self._get_houses(),
            'babies': self.babies,
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
            self.game.show_game_over()
            return

        if self.turns_taken == self.game.current_round:
            # Player already played.
            self.game.show_error(f"{self} already played")
            return

        self._update_from_assets()
        
        roll_result = self._roll()
        self.turns_taken += 1
        self.earn_salary()
        self.game.show_assets()

        self.game.show_info(str(roll_result), clear=True)

    def update_dollars(self, value):
        self.dollars += value

    def update_life_points(self, value=None):
        self.life_points += value

    def _convert_dollars(self, factor):
        extra_life_points = int(round(self.dollars / factor, 0))
        self.dollars = 0
        self.update_life_points(extra_life_points)

    def _get_cars(self):
        return [asset for asset in self.assets if 'car' in asset.name]

    def _get_houses(self):
        houses = []
        for asset in self.assets:
            if 'house' in asset.name:
                houses.append(asset)
            elif 'mansion' in asset.name:
                houses.append(asset)
        return houses

    def _is_in_game(self, game) -> bool:
        return str(self) in [str(p) for p in game.players]

    def _end(self):
        self.__end = True

    def _retrieve_asset(self, name):
        for i, asset in enumerate(self.assets[:]):
            if asset.name == name:
                return self.assets.pop(i)

    def _roll(self):
        # NOTE: LIFE says that cars add +1 or +2 to the spin "average". We're
        # just changing the minimum roll here for simplicity's sake.
        min = 1
        if len(self._get_cars()) == 2:
            min += 2
        elif len(self._get_cars()) == 1:
            min += self._get_cars()[0].roll_modifier
        return randint(min, 10)
    
    def _update_from_assets(self):
        if self.dollars < 0:
            # Pay 10% interest on debt.
            self.dollars = int(round(1.1 * self.dollars, 0))

        for asset in self.assets:
            # Update asset's own value.
            asset.do_turn()

            # Account for any salary reduction.
            if hasattr(asset, 'salary_reduction'):
                if self.salary_reduction is None:
                    self.salary_reduction = 0
                self.salary_reduction += int(round(self.salary * asset.salary_reduction))

            # Account for any additional life points.
            if hasattr(asset, 'life_points_modifier'):
                self.life_points += asset.life_points_modifier

        if self.married:
            raise NotImplementedError
        
        if self.babies > 0:
            raise NotImplementedError


class PlayerInvalidError(ValueError):
    pass


class PlayerTakenError(ValueError):
    pass