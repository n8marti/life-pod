import math
import kivy
kivy.require('2.0.0')
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.properties import StringProperty  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.checkbox import CheckBox  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402


class LifePodWin(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def handle_num_input(self, value):
        if self.app.active_input:
            self.app.user_input += value
            self.ids.display2.text += value
        return value

    def handle_enter(self):
        self.app._stop_input()
        user_input = self.ids.display2.text
        self.ids.display2.text = ''
        return user_input

    def handle_spin(self):
        self.app.game.current_player.do_turn()

    def handle_undo(self):
        """Remove last character from user input."""
        self.ids.display2.text = self.ids.display2.text[:-1]

    def handle_minus(self):
        print('minus')

    def handle_plus(self):
        print('plus')

    def handle_dollars(self):
        print('$')
    
    def handle_life_points(self):
        print('life points')

    def handle_player_choice(self, obj):
        """Start player's turn or any inter-turn actions."""
        if obj.active:
            if self.app.game._game_complete():
                print('game complete')
                self.app.show_info("Game complete!")
            elif self.app.game._round_complete():
                self.app.game.current_round += 1

            self.app.game.player_name = obj.name
            if obj.name == 'none':
                self.app.game.current_player = None
            else:
                self.app.game.current_player = self.app.game._get_player(obj.name, self.app.game.players)
    
    def reset_display(self):
        self.ids.display1.text = ''
        self.ids.display2.text = ''


class LifePodApp(App):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        self.active_input = False
        self.user_input = None

    def build(self):
        return LifePodWin()

    def on_start(self):
        self.game.ask_length()

    def show_assets(self, player):
        pass

    def show_info(self, text):
        # TODO: Increase text size; truncate text at X characters.
        self.root.ids.display1.text = text

    def ask_length(self, text):
        self.root.ids.display1.text = text
        self._start_input()
        Clock.schedule_interval(self._get_length, 0.1)

    def _get_length(self, dt):
        if not self.active_input:
            self.game.length = self._get_input()

    def _set_length(self, length):
        self.game.length = length

    def _start_input(self):
        self.active_input = True
        self.user_input = ''

    def _stop_input(self):
        self.active_input = False

    def _get_input(self):
        user_input = self.user_input
        self.user_input = None
        self.root.reset_display()
        return user_input

    # def ask_player(self):
    #     # w = PickPlayerWindow()
    #     # w.win.wait_window()
    #     return player

    # def ask_start_turn(self):
    #     return self._ask_yes_no(self._ask_start_turn_text)

    # def ask_update_player(self):
    #     return self._ask_yes_no(self._ask_player_changes_text)

    # def show_assets(self, player):
    #     pass
    #     # p = PlayerWindow(str(player))
    #     # p.win.wait_window()

    # def show_error(self, text):
    #     pass
    #     # messagebox.showerror("Error", text)


class AppButton(Button):
    def _get_win(self):
        return self.get_root_window().children[0]


class AppCheckBox(CheckBox):
    name = StringProperty(None)

    def _get_win(self):
        return self.get_root_window().children[0]


class BlueButton(AppButton):
    pass

class RedButton(AppButton):
    pass


class NumButton(AppButton):
    # NOTE: The attribute '.pos_hint' is set by '._get_pos_hint' after
    # __init__ because it depends on the 'self.text' value, which is set in the
    # KV file after __init__ is run.
    def _get_pos_hint(self):
        # Sets instance attribute here, and is used to set value in KV file.
        dx, dy = self._offsets(int(self.text))
        return {'center_x': 0.5 + dx, 'center_y': 0.5 + dy}

    def _offsets(self, idx):
        rads = math.radians(360*(1 - idx) / 11)
        dx = -0.4 * math.sin(rads)
        dy = 0.4 * math.cos(rads)
        return (dx, dy)
