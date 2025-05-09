from random import randint

from .gui import LifePodApp
from .player import Player
from .player import PlayerInvalidError
from .player import PlayerTakenError
from .round import Round


class Game:
    def __init__(self):
        self.length = None
        self._ask_length_text = "# of turns:"
        self._ask_length_help = "Please enter a whole number from 1-20."
        self.current_player = None
        self.current_round = 0

        self.all_colors = ['red', 'yellow', 'green', 'blue']

        self.players = None
        self._ask_which_players_text = "Which colors will be playing?"
        self._ask_which_players_help = f"Valid colors are {', '.join(self.all_colors)}."
        self._ask_player_text = "Choose player color"
        self._ask_player_help = "Please choose an acceptable color."
        self._ask_update_salary = "New salary:"

        self._ask_start_turn_text = "Start your turn?"
        self._ask_player_changes_text = "Update player details?"

    def play(self):
        raise NotImplementedError

    def ask_length(self) -> str:
        raise NotImplementedError

    def ask_player(self) -> str:
        raise NotImplementedError

    def ask_player_action(self, player):
        raise NotImplementedError

    def ask_which_players(self) -> str:
        raise NotImplementedError

    def ask_update_player(self):
        raise NotImplementedError

    def show_assets(self):
        raise NotImplementedError

    def show_error(self, text):
        raise NotImplementedError

    def show_info(self, text):
        raise NotImplementedError

    def _round_complete(self):
        """All players have taken as many turns as rounds that have been played."""
        return all([p.turns_taken == self.current_round for p in self.players])

    def _game_complete(self):
        """Current round is complete and current round is last round."""
        if self._round_complete():
            return self.current_round == self.length

    def _chance(self):
        return self._roll(min=0, max=2)
    
    def _lottery(self):
        return self._roll(min=1, max=10)

    def _roll(self, min=1, max=10):
        return randint(min, max)

    def _ask_length(self):
        length = None
        while length is None:
            try:
                user_input = self.ask_length()
                length = self._verify_length(user_input)
            except (TypeError, ValueError):
                self.show_info(self._ask_length_help)
        return length

    def _ask_which_players(self):
        which_players = None
        while which_players is None:
            try:
                user_input = self.ask_which_players()
                which_players = self._verify_which_players(user_input)
            except (TypeError, ValueError):
                self.show_info(self._ask_which_players_help)
        return which_players

    def _verify_length(self, user_input):
        try:
            user_input = int(user_input)
        except ValueError:
            raise
        if user_input < 1 or user_input > 20:
            raise ValueError
        return user_input

    def _verify_which_players(self, user_input):
        user_input_items = user_input.lower().replace(',', ' ').split()
        # print(f"{user_input_items=}")
        players = []
        for c in self.all_colors:
            if c.lower() in user_input_items:
                players.append(Player(self, c))
        return players

    def _ask_player(self):
        player = None
        while player is None:
            try:
                user_input = self.ask_player()
                user_input = self._verify_player(user_input)
                player = Player(user_input)
            except ValueError:
                self.show_info(self._ask_player_help)
        return player

    def _verify_player(self, user_input):
        if user_input not in [str(p) for p in self.all_players]:
            raise PlayerInvalidError
        elif user_input not in [str(p) for p in self.available_players]:
            raise PlayerTakenError
        return user_input
    
    def _get_player(self, name, iterable):
        for p in iterable:
            if name == str(p):
                return p


class Cli(Game):
    def __init__(self):
        super().__init__()

    def ask_length(self) -> str:
        return self._ask_value(self._ask_length_text, vtype=int)

    def ask_player(self) -> str:
        return self._ask_value(self._ask_player_text, vtype=str)

    def ask_player_action(self, player):
        return self._ask_player_action(player)

    def ask_update_player(self) -> bool:
        return self._ask_yes_no(self._ask_player_changes_text)

    def ask_which_players(self) -> list:
        return self._ask_value(self._ask_which_players_text)

    def show_info(self, text) -> None:
        print(text)

    def play(self):
        if self.length is None:
            self.length = self._ask_length()
        
        if self.players is None:
            self.players = self._ask_which_players()

        if self.current_round < self.length:
            r = Round(self)
            r.play_loop()

    def _ask_player_action(self, player) -> str:
        return input(f"Choose action for {str(player)}: {', '.join(player.actions.keys())}: ")

    def _ask_value(self, question, vtype=str) -> str|int:
        return vtype(input(f"{question}: "))

    def _ask_yes_no(self, question) -> bool:
        answer = input(f"{question} [Y/n]: ")
        if answer.lower() == 'y' or answer == '':
            return True
        else:
            return False

    def show_assets(self):
        player = self.current_player
        for k, v in player.get_assets().items():
            print(f"\t{k}: {v}")
        print()


class Gui(Game):
    def __init__(self):
        super().__init__()
        self.app = LifePodApp(self)

        # Add all players initially; remove any that have not played by the
        # start of Round 2.
        self.players = []
        for p in self.all_colors:
            self._add_player(p)

    def play(self):
        self.app.run()

    def ask_length(self):
        # self.app.root_window.children[0]._ask_length(self._ask_length_text)
        self.app.ask_length(self._ask_length_text)

    def round_is_complete(self):
        """This is evaluated right after any player is selected."""
        # All players have taken as many turns as rounds that have been played.
        return all([p.turns_taken == self.current_round for p in self.players])

    def show_assets(self, *args):
        """Shows assets of current player."""
        self.app.show_assets()

    def show_error(self, text):
        self.app.show_error(text)

    def show_game_over(self):
        self.conversion_factor = randint(80, 120)
        self.app.show_game_over()

    def show_info(self, *args, **kwargs):
        self.app.show_info(*args, **kwargs)

    def start_next_round(self):
        self.current_round += 1
        self.app.update_remaining_rounds(self._get_remaining_rounds())

    def _add_player(self, color):
        self.players.append(Player(self, color))

    def _get_remaining_rounds(self):
        return self.length - self.current_round + 1

    def _remove_nonplayers(self):
        for p in self.players[:]:
            if p.turns_taken == 0:
                self.players.remove(p)