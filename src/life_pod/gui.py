import math
import kivy
kivy.require('2.0.0')
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.properties import ObjectProperty  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402


class LifePod(FloatLayout):
    display0 = ObjectProperty(None)
    display1 = ObjectProperty(None)
    display2 = ObjectProperty(None)
    player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.active_input = False
        self.user_input = None

    def _get_length(self, dt):
        if not self.active_input:
            self.app.game.length = self._get_input()

    def _ask_length(self, text):
        self.display1.text = text
        self._start_input()
        Clock.schedule_interval(self._get_length, 0.1)

    def show_info(self, text):
        # TODO: Increase text size; truncate text at X characters.
        self.display1.text = text

    def handle_enter(self):
        self._stop_input()
        user_input = self.ids.display2.text
        self.ids.display2.text = ''
        return user_input

    def handle_minus(self):
        print('minus')

    def handle_plus(self):
        print('plus')

    def handle_num_input(self, value):
        if self.active_input:
            self.user_input += value
            self.ids.display2.text += value
        return value

    def handle_player_dropdown(self):
        self.app.game.player_name = self.ids.player.text

    def _start_input(self):
        self.active_input = True
        self.user_input = ''

    def _stop_input(self):
        self.active_input = False

    def _get_input(self):
        user_input = self.user_input
        self.user_input = None
        return user_input

    def ask_player(self):
        # w = PickPlayerWindow()
        # w.win.wait_window()
        return player

    def ask_start_turn(self):
        return self._ask_yes_no(self._ask_start_turn_text)

    def ask_update_player(self):
        return self._ask_yes_no(self._ask_player_changes_text)

    def show_assets(self, player):
        pass
        # p = PlayerWindow(str(player))
        # p.win.wait_window()

    def show_error(self, text):
        pass
        # messagebox.showerror("Error", text)


class LifePodApp(App):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def build(self):
        return LifePod()

    def on_start(self):
        self.game.ask_length()

    def _set_length(self, length):
        self.game.length = length


class AppButton(Button):
    def _get_win(self):
        return self.get_root_window().children[0]


class BlueButton(AppButton):
    pass

class EnterButton(BlueButton):
    def on_press(self):
        self._get_win().handle_enter()

class SpinButton(BlueButton):
    def on_press(self):
        print(self.text)

class UndoButton(BlueButton):
    def on_press(self):
        print(self.text)


class DollarUnitButton(BlueButton):
    def on_press(self):
        print(self.text)


class LifePointsUnitButton(BlueButton):
    def on_press(self):
        print(self.text)


class RedButton(AppButton):
    pass


class MinusButton(RedButton):
    def on_press(self):
        return self._get_win().handle_minus()


class PlusButton(RedButton):
    def on_press(self):
        return self._get_win().handle_plus()


class NumButton(AppButton):
    # NOTE: Several attributes are set with methods after __init__ because they
    # depend on the 'self.idx' value, which is set in the KV file after
    # __init__ is run.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kv_id = None

    def on_press(self):
        self._get_win().handle_num_input(self.text)

    def _get_pos_hint(self):
        # Sets instance attribute here, and is used to set value in KV file.
        dx, dy = self._offsets(int(self.text))
        return {'center_x': 0.5 + dx, 'center_y': 0.5 + dy}

    def _offsets(self, idx):
        rads = math.radians(360*(1 - idx) / 11)
        dx = -0.4 * math.sin(rads)
        dy = 0.4 * math.cos(rads)
        return (dx, dy)
