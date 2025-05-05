class Round:
    def __init__(self, game):
        self.game = game

    def start_turn(self):
        if not self._round_is_complete():
            self.game.current_player.play()

    def play_loop(self):
        while not self._round_is_complete():
            self.game.show_info(f"Round {self.game.current_round}")

            # Get player name from user.
            player_name = self.game.ask_player()
            self.game.current_player = self.game._get_player(player_name, self.game.players)
            self.game.current_player.play_loop()
        
        # Increment round number at the end.
        self.game.current_round += 1

    def _round_is_complete(self):
        # All players have taken as many turns as rounds that have been played.
        return all([p.turns_taken == self.game.current_round for p in self.game.players])