import random
from .player import Player
from .player import PlayerInvalidError
from .player import PlayerTakenError


class Round:
    def __init__(self, game):
        self.player_name = None
        self.game = game
        self._reset_players()

    def play(self):
        # Round ends when all players have played; i.e. self.players_played
        # is populated and self.players_left is empty.
        while len(self.players_left) > 0 or self.game.current_round == 1:
            self.game.show_info(f"Round {self.game.current_round}")

            # Wait for player name.
            # If player exists and has unapplied changes, apply them now.
            # If round 1, create player if it doesn't exist, play turn.
            # If subsequent round, ignore player if it doesn't exist, play turn if it does.

            # Get player name from user.
            if self.player_name is None:
                self.player_name = self.game.ask_player()
            current_player = None

            # Create player on round 1 if non-existent.
            if self.game.current_round == 1:
                if self.game._get_player(self.player_name, self.game.players):
                    # Go to next round.
                    self._reset_players(keep_player_name=True)
                    self.game.current_round += 1
                    continue

                # Add new player if 1st round.
                new_player = None
                while new_player is None:
                    player = Player(self.player_name)
                    if not player._is_in_game(self.game):
                        self.game.show_info(f"Creating new player: {self.player_name}")
                        new_player = player
                        current_player = new_player
                        self.game.players.append(new_player)
                        self.players_left.append(new_player)
                    else:
                        new_player = False
                # if new_player is False:
                #     continue

            # Define current player.
            if current_player is None:
                current_player = self.game._get_player(self.player_name, self.players_left)

            if current_player is not None:
                # Check for unapplied changes for player.
                self.game.show_info(f"Updating dollars and life_points for {str(current_player)}.")
                current_player._update_dollars()
                current_player._update_life_points()
                
                # Offer to start the turn.
                if self.game.ask_start_turn() is True:
                    self._do_turn(current_player)
            
            self.player_name = None
        
        # Increment round number at the end.
        self.game.current_round += 1

    def _do_turn(self, player):
        player._update_dollars()
        player._update_life_points()
        
        roll_result = self.game._roll()
        player.earn_salary()
        self.game.show_assets(player)
        self.game.show_info(f"You rolled '{roll_result}'")
        if self.game.ask_update_player():
            raise NotImplementedError

        self.players_left.remove(player)
        self.players_played.append(player)

    def _reset_players(self, keep_player_name=False):
        if not keep_player_name:
            self.player_name = None
        self.players_left = self.game.players.copy()
        self.players_played = []


class Game:
    def __init__(self):
        self.length = None
        self._ask_length_text = "How many turns would you like to play?"
        self._ask_length_help = "Please enter a whole number from 1-20."
        self.current_round = 1

        self.all_colors = ['red', 'yellow', 'green', 'blue']
        self.all_players = [Player(c) for c in self.all_colors]

        self.available_players = self.all_players.copy()
        self.players = []
        self._ask_player_text = "Choose player color"
        self._ask_player_help = "Please choose an acceptable color."

        self._ask_start_turn_text = "Start your turn?"
        self._ask_player_changes_text = "Update player details?"

    def play(self):
        raise NotImplementedError

    def ask_player(self):
        raise NotImplementedError

    def ask_length(self):
        raise NotImplementedError

    def ask_start_turn(self):
        raise NotImplementedError

    def ask_update_player(self):
        raise NotImplementedError

    def show_assets(self):
        raise NotImplementedError

    def show_error(self):
        raise NotImplementedError

    def show_info(self):
        raise NotImplementedError

    def _roll(self, max=10, min=1):
        return random.randint(min, max)

    def _ask_length(self):
        length = None
        while length is None:
            try:
                user_input = self.ask_length()
                user_input = self._verify_length(user_input)
                length = user_input
            except (TypeError, ValueError):
                print(self._ask_length_help)
        return length

    def _verify_length(self, user_input):
        try:
            user_input = int(user_input)
        except ValueError:
            raise
        if user_input < 1 or user_input > 20:
            raise ValueError
        return user_input

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
        if self.length is None:
            self.length = self._ask_length()

    def ask_length(self) -> str:
        return self._ask_value(self._ask_length_text, vtype=int)

    def ask_player(self) -> str:
        return self._ask_value(self._ask_player_text, vtype=str)

    def ask_update_player(self) -> bool:
        return self._ask_yes_no(self._ask_player_changes_text)

    def ask_start_turn(self) -> bool:
        return self._ask_yes_no(self._ask_start_turn_text)

    def show_info(self, text) -> None:
        print(text)

    def play(self):
        if self.current_round < self.length:
            r = Round(self)
            r.play()

    def _ask_value(self, question, vtype=str) -> str|int:
        return vtype(input(f"{question}: "))

    def _ask_yes_no(self, question) -> bool:
        answer = input(f"{question} [Y/n]: ")
        if answer.lower() == 'y' or answer == '':
            return True
        else:
            return False

    def show_assets(self, player):
        for k, v in player.get_assets().items():
            print(f"\t{k}: {v}")
        print()


class Gui(Game):
    pass