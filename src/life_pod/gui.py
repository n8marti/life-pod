import math
import kivy
kivy.require('2.0.0')
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.properties import NumericProperty  # noqa: E402
from kivy.properties import StringProperty  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.checkbox import CheckBox  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402


class LifePodWin(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def handle_num_input(self, instance):
        """Add digit to pending user input."""
        self._keypress(instance.text)
        # TODO: Add alternate button functions.
        if self.app.active_input:
            value = instance.text
            self.app.user_input += value
            self.ids.display2.text += value
        else:
            value = instance.parent.children[0].text
            self._set_secondary_action(value.lower())
        return value

    def handle_enter(self):
        """Signal that user input has stopped; get current value(s) of user input."""
        self._keypress('enter')
        self.app._stop_input()
        self.app.pending_input = self._concat_input()
        self.clear_display()
        
    def handle_spin(self):
        """Return random number based on player's car type(s)."""
        # TODO: simplify to only show "spin" animation and return number.
        self._keypress('spin')
        if self.app.game.current_player is not None:
            if self.app.game.current_round == 1 and self.app.game.current_player.turns_taken == 1:
                # Player is playing for the 2nd time; remove other players.
                self.app.game._remove_nonplayers()

            if self.app.game.round_is_complete():
                self.app.game.start_next_round()
            self.clear_display()
            self.app.game.current_player.do_turn()

    def handle_undo(self):
        """Remove last character from user input."""
        self._keypress('undo')
        if len(self.ids.display2.text) > 0:
            self.ids.display2.text = self.ids.display2.text[:-1]

    def handle_minus(self):
        """Set sign of pending user input as "-"."""
        self._keypress('-')
        self.clear_display()
        self._show_sign("-")
        self.app._start_input()
        self.app._set_sign("-")

    def handle_plus(self):
        """Set sign of pending user input as "+"."""
        self._keypress('+')
        self.clear_display()
        self._show_sign("+")
        self.app._start_input()
        self.app._set_sign("+")

    def handle_dollars(self):
        """Set pending action to update dollars."""
        self._keypress('$')
        self._show_dollar()
        self.app._wait_input()
        self.app.pending_action = self.app.update_player_dollars
    
    def handle_life_points(self):
        """Set pending action to update life points."""
        self._keypress('life points')
        self._show_heart()
        self.app._wait_input()
        self.app.pending_action = self.app.update_player_life_points

    def handle_player_choice(self, obj):
        """Set current player."""
        self._keypress(obj.name)
        if obj.active:
            self.app.root.clear_display()

            # Evaluate player choice.
            self.app.game.player_name = obj.name
            if obj.name == 'none':
                self.app.game.current_player = None
            elif obj.name not in [p.name for p in self.app.game.players]:
                # Non-player was removed and can't play.
                self.app.game.current_player = None
                self.app.show_error(f"({obj.name} not playing)")
            else:
                # Load player.
                self.app.game.current_player = self.app.game._get_player(obj.name, self.app.game.players)
                self.app.show_assets(self.app.game.current_player)

    def clear_display(self):
        self._reset_houses()
        self._reset_cars()
        self._reset_babies()
        
        self._hide_dollar()
        self.set_display1_text('')
        self._reset_married()
        self._reset_sign()

        self._hide_heart()
        self.reset_input_field()
        self._reset_turns()

    def reset_input_field(self):
        self.ids.display2.text = ''

    def set_display1_text(self, text):
        self.ids.display1.text = str(text).upper()

    def show_game_over(self):
        self.set_display1_text("game over")

    def _hide_dollar(self):
        self.ids.dollar.source= 'img/blank.png'

    def _show_dollar(self):
        self.ids.dollar.source = 'img/dollar.png'

    def _hide_heart(self):
        self.ids.heart.source = 'img/blank.png'

    def _show_heart(self):
        self.ids.heart.source = 'img/heart.png'

    def _reset_houses(self):
        self.ids.house_modest.source = 'img/blank.png'
        self.ids.house_midsized.source = 'img/blank.png'
        self.ids.house_mansion.source = 'img/blank.png'
    
    def _reset_cars(self):
        self.ids.car_economy.source = 'img/blank.png'
        self.ids.car_sports.source = 'img/blank.png'
    
    def _reset_babies(self):
        self.ids.babies.source = 'img/blank.png'
        self.ids.baby_count.text = ""

    def _reset_married(self):
        self.ids.married.source = 'img/blank.png'

    def _reset_sign(self):
        self.ids.sign.text = ''
    
    def _show_sign(self, value):
        self.ids.sign.text = str(value)

    def _reset_turns(self):
        self.ids.turns.source = 'img/blank.png'
        self.ids.remaining_rounds.text = ""

    def _show_turns(self, value=None):
        self.ids.turns.source = 'img/clock.png'
        if value is None:
            value = self.app.game._get_remaining_rounds()
        self.ids.remaining_rounds.text = str(value)

    def _concat_input(self):
        user_input = ''
        if self.app.pending_sign:
            user_input += self.app.pending_sign
        user_input += self.ids.display2.text
        return user_input

    def _keypress(self, value):
        print(f"keypress: {value}")
    
    def _set_secondary_action(self, name):
        match name:
            case 'years':
                pass
            case 'salary':
                self.clear_display()
                self.app.ask_player_salary()
            case 'lottery':
                pass
            case 'chance':
                pass
            case 'marriage':
                pass
            case 'baby':
                pass
            case 'car':
                pass
            case 'house':
                pass


class LifePodApp(App):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        self.active_input = False
        self.pending_input = None
        self.pending_sign = None
        self.pending_action = None

    def build(self):
        return LifePodWin()

    def on_start(self):
        self.root.clear_display()
        self.game.ask_length()

    def process_input(self, dt):
        if not self.active_input:
            print(f"input received; running: {self.pending_action.__name__}")
            self.pending_action()
            self.reset_pending()
            return False

    def show_assets(self, player):
        self.root._show_turns()
        for k, v in player.get_assets().items():
            match k:
                case 'cars':
                    self._show_cars(v)
                case 'children':
                    self._show_children(v)
                case 'houses':
                    self._show_houses(v)
                case 'married':
                    self._show_married(v)
                case 'dollars':
                    self._show_dollars(v)
                case 'life points':
                    self._show_life_points(v)

    def show_error(self, text):
        self.reset_pending()
        self.show_info(text)

    def show_game_over(self):
        self.root.show_game_over()
        self._run_after(self._convert_assets, 3)

    def show_info(self, text, clear=False):
        if clear:
            self.root.clear_display()
        self.root.set_display1_text(text)

    def reset_pending(self):
        self.pending_input = None
        self.pending_sign = None
        self.pending_action = None

    def update_player_dollars(self):
        if self._verify_player():
            self.game.current_player.update_dollars(int(self.pending_input))
            self.show_assets(self.game.current_player)

    def update_player_life_points(self):
        if self._verify_player():
            self.game.current_player.update_life_points(int(self.pending_input))

    def ask_length(self, text):
        self.show_info(text, clear=True)
        self.pending_action = self.set_game_length
        self._wait_input()

    def set_game_length(self):
        self.game.length = int(self.pending_input)
        self.game.start_next_round()

    def ask_player_salary(self):
        if self._verify_player():
            self.show_info(self.game._ask_update_salary)
            self.pending_action = self.set_player_salary
            self._wait_input()
    
    def set_player_salary(self):
        if self._verify_player():
            self.game.current_player.set_salary(int(self.pending_input))
            self.show_assets(self.game.current_player)

    def update_remaining_rounds(self, value):
        self.root._show_turns(value)

    def _convert_assets(self, dt):
        for p in self.game.players:
            p.convert_assets(self.game.conversion_factor)
        self.show_assets(self.game.current_player)

    def _run_after(self, func, delay):
        # NOTE: func must accept 'dt' kwargs.
        Clock.schedule_once(func, delay)

    def _set_sign(self, value):
        self.pending_sign = value

    def _show_cars(self, value):
        pass

    def _show_children(self, value):
        pass

    def _show_houses(self, value):
        pass

    def _show_married(self, value):
        pass

    def _show_dollars(self, value):
        self.root._show_dollar()
        self.show_info(str(value))

    def _show_life_points(self, value):
        self.root._show_heart()
        self.root.ids.display2.text = str(value)

    def _start_input(self):
        self.active_input = True
        self.user_input = ''
        self.root.reset_input_field()

    def _stop_input(self):
        self.active_input = False

    def _verify_player(self):
        if self.game.current_player is None:
            self.show_error("No player selected; try again.")
            return False
        return True

    def _wait_input(self):
        print("waiting on user input")
        self._start_input()
        Clock.schedule_interval(self.process_input, 0.1)


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

class NumLayout(BoxLayout):
    number = NumericProperty(None)
    text = StringProperty(None)

    def _get_pos_hint(self):
        # Sets instance attribute here, and is used to set value in KV file.
        dx, dy = self._offsets(self.number)
        return {'center_x': 0.5 + dx, 'center_y': 0.5 + dy}

    def _offsets(self, idx):
        rads = math.radians(360*(1 - idx) / 11)
        dx = -0.4 * math.sin(rads)
        dy = 0.4 * math.cos(rads)
        return (dx, dy)
