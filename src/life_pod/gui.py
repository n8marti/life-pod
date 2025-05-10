import math
import kivy
kivy.require('2.0.0')
from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.properties import BooleanProperty  # noqa: E402
from kivy.properties import NumericProperty  # noqa: E402
from kivy.properties import StringProperty  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.checkbox import CheckBox  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.image import Image  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from pathlib import Path  # noqa: E402

from .assets import Car  # noqa: E402
from .assets import House  # noqa: E402


class LifePodWin(BoxLayout):
    img_dir = StringProperty(str(Path(__file__).parent / 'img'))
    title = StringProperty("LIFE Pod")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.prev_choice = None

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
        if self.app.active_input:
            self.app._stop_input()
            self.app.pending_input = self._concat_input()
        elif self.app.pending_choice:
            self.app.active_choice = False
            self.prev_choice = None
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
        # TODO: Also handle last non-input operation?
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
        self.ids.dollar.show()
        self.app._wait_input()
        self.app.pending_action = self.app.update_player_dollars
    
    def handle_life_points(self):
        """Set pending action to update life points."""
        self._keypress('life points')
        self.ids.heart.show()
        self.app._wait_input()
        self.app.pending_action = self.app.update_player_life_points

    def handle_player_choice(self, obj):
        """Set current player."""
        self._keypress(obj.name)
        if obj.active:
            self.clear_display()

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
                self.app.show_assets()

    def handle_reset(self):
        """Ask user to confirm whether or not to reset the game."""
        # Find & dismiss popup window among parent window children.
        for c in self.get_parent_window().children:
            if c is not self:
                c.dismiss()
                break
        self.app.game.restart()

    def clear_display(self):
        self._hide_houses()
        self._hide_cars()
        self._reset_babies()
        
        self.ids.dollar.hide()
        self.ids.display1.clear()
        self.ids.married.hide()
        self.ids.sign.clear()

        self.ids.heart.hide()
        self.ids.display2.clear()
        self._reset_turns()

    def set_display1_text(self, text):
        self.ids.display1.text = str(text).upper()

    def show_game_over(self):
        self.set_display1_text("game over")

    def _choose_baby(self):
        self.clear_display()
        if self.app.pending_action is None:
            self.app.pending_action = self.app.update_player_babies
            self.app._wait_choice()
        if self.prev_choice is True:
            self.ids.babies.hide()
            self.app.pending_choice = False
            self.prev_choice = False
        else:
            self.ids.babies.show()
            self.app.pending_choice = True
            self.prev_choice = True

    def _choose_car(self):
        self.clear_display()
        if self.app.pending_action is None:
            self.app.pending_action = self.app.buy_sell_player_asset
            self.app._wait_choice()
        # Use "CAR" to cycle through car options.
        if self.prev_choice is self.ids.car_economy:
            self.ids.car_sports.show()
            self.app.pending_choice = Car.SPORTS
            self.prev_choice = self.ids.car_sports
        else:
            self.ids.car_economy.show()
            self.app.pending_choice = Car.ECONOMY
            self.prev_choice = self.ids.car_economy

    def _choose_house(self):
        self.clear_display()
        if self.app.pending_action is None:
            self.app.pending_action = self.app.buy_sell_player_asset
            self.app._wait_choice()
        # Use "HOUSE" to cycle through car options.
        if self.prev_choice is self.ids.house_modest:
            self.ids.house_midsized.show()
            self.app.pending_choice = House.MIDSIZED
            self.prev_choice = self.ids.house_midsized
        elif self.prev_choice is self.ids.house_midsized:
            self.ids.house_mansion.show()
            self.app.pending_choice = House.MANSION
            self.prev_choice = self.ids.house_mansion
        else:
            self.ids.house_modest.show()
            self.app.pending_choice = House.MODEST
            self.prev_choice = self.ids.house_modest

    def _choose_marriage(self):
        self.clear_display()
        if self.app.pending_action is None:
            self.app.pending_action = self.app.update_player_marriage
            self.app._wait_choice()
        if self.prev_choice is True:
            self.ids.married.hide()
            self.app.pending_choice = False
            self.prev_choice = False
        else:
            self.ids.married.show()
            self.app.pending_choice = True
            self.prev_choice = True

    def _hide_houses(self):
        self.ids.house_modest.hide()
        self.ids.house_midsized.hide()
        self.ids.house_mansion.hide()
    
    def _hide_cars(self):
        self.ids.car_economy.hide()
        self.ids.car_sports.hide()
    
    def _reset_babies(self):
        self.ids.babies.hide()
        self.ids.baby_count.clear()

    def _show_cars(self, cars=None):
        if cars is None:
            cars = [c.name for c in self.app.game.current_player.cars]
        for car in cars:
            match car:
                case Car.ECONOMY:
                    self.ids.car_economy.show()
                case Car.SPORTS:
                    self.ids.car_sports.show()
    
    def _show_sign(self, value):
        self.ids.sign.text = str(value)

    def _reset_turns(self):
        self.ids.turns.hide()
        self.ids.remaining_rounds.clear()

    def _show_turns(self, value=None):
        self.ids.turns.show()
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
                self._choose_marriage()
            case 'baby':
                self._choose_baby()
            case 'car':
                self._choose_car()
            case 'house':
                self._choose_house()


class LifePodApp(App):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def ask_length(self, text):
        self.show_info(text, clear=True)
        self.pending_action = self.set_game_length
        self._wait_input()

    def ask_player_salary(self):
        if self._verify_player():
            self.show_info(self.game._ask_update_salary)
            self.pending_action = self.set_player_salary
            self._wait_input()

    def build(self):
        return LifePodWin()

    def buy_sell_player_asset(self):
        asset_name = self.pending_choice
        if asset_name in [a.name for a in self.game.current_player.assets]:
            # Sell asset.
            self.game.current_player.sell(asset_name)
        else:
            # Buy asset.
            self.game.current_player.buy(asset_name)
        self.show_assets()

    def on_start(self):
        self.start_game()

    def process_input(self, dt):
        if self.pending_input and not self.active_input:
            print(f"received input: {self.pending_input}; running: {self.pending_action.__name__}")
            # NOTE: pending_action must rely on reading self.pending_input or
            # self.pending_choice.
            self.pending_action()
            self.reset_pending()
            return False

        if self.pending_choice is not None and not self.active_choice:
            print(f"received choice: {self.pending_choice}; running: {self.pending_action.__name__}")
            # NOTE: pending_action must rely on reading self.pending_input or
            # self.pending_choice.
            self.pending_action()
            self.reset_pending()
            return False

    def reset(self):
        self.root.clear_display()
        self.active_choice = False
        self.active_input = False
        self.reset_pending()

    def reset_pending(self):
        self.pending_choice = None
        self.pending_input = None
        self.pending_sign = None
        self.pending_action = None

    def set_game_length(self):
        self.game.length = int(self.pending_input)
        self.game.start_next_round()

    def set_player_salary(self):
        if self._verify_player():
            self.game.current_player.set_salary(int(self.pending_input))
            self.show_assets()

    def show_assets(self):
        self.root._show_turns()
        for k, v in self.game.current_player.get_assets().items():
            match k:
                case 'cars':
                    self._show_assets(v)
                case 'babies':
                    self._show_babies(v)
                case 'houses':
                    self._show_assets(v)
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

    def start_game(self):
        self.reset()
        self.ask_length(self.game._ask_length_text)

    def update_player_babies(self):
        if self._verify_player():
            if self.pending_choice is True:
                self.game.current_player.add_baby(self.pending_choice)
            self.reset_pending()
            self.show_assets()

    def update_player_dollars(self):
        if self._verify_player():
            self.game.current_player.update_dollars(int(self.pending_input))
            self.show_assets()

    def update_player_life_points(self):
        if self._verify_player():
            self.game.current_player.update_life_points(int(self.pending_input))
            self.show_assets()

    def update_player_marriage(self):
        if self._verify_player():
            self.game.current_player.set_marriage(self.pending_choice)
            self.reset_pending()
            self.show_assets()

    def update_remaining_rounds(self, value):
        self.root._show_turns(value)

    def _clear_input_field(self):
        self.root.ids.display2.clear()

    def _convert_assets(self, dt):
        for p in self.game.players:
            p.convert_assets(self.game.conversion_factor)
        self.show_assets()

    def _run_after(self, func, delay):
        # NOTE: func must accept 'dt' arg.
        Clock.schedule_once(func, delay)

    def _set_sign(self, value):
        self.pending_sign = value

    def _show_assets(self, iterable):
        for asset in iterable:
            match asset.name:
                case Car.ECONOMY:
                    self.root.ids.car_economy.show()
                case Car.SPORTS:
                    self.root.ids.car_sports.show()
                case House.MODEST:
                    self.root.ids.house_modest.show()
                case House.MIDSIZED:
                    self.root.ids.house_midsized.show()
                case House.MANSION:
                    self.root.ids.house_mansion.show()

    def _show_babies(self, value):
        self.root.ids.babies.show()
        self.root.ids.baby_count.text = str(value)

    def _show_married(self, value):
        if value is True:
            self.root.ids.married.show()

    def _show_dollars(self, value):
        self.root.ids.dollar.show()
        self.show_info(str(value))

    def _show_life_points(self, value):
        self.root.ids.heart.show()
        self.root.ids.display2.text = str(value)

    def _start_input(self):
        self.active_input = True
        self.user_input = ''
        self._clear_input_field()

    def _stop_input(self):
        self.active_input = False

    def _verify_player(self):
        if self.game.current_player is None:
            self.show_error("No player selected; try again.")
            return False
        return True

    def _wait_choice(self):
        print("waiting on user choice")
        self.active_choice = True
        Clock.schedule_interval(self.process_input, 0.1)

    def _wait_input(self):
        print("waiting on user input")
        self._start_input()
        Clock.schedule_interval(self.process_input, 0.1)


class AppButton(Button):
    pass


class AppCheckBox(CheckBox):
    name = StringProperty(None)


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


class ScreenImage(Image):
    shown = BooleanProperty()
    source_shown = StringProperty(None)
    source_hidden = StringProperty(f"{Path(__file__).parent}/img/blank.png")

    def hide(self):
        self.shown = False
        self.source = self.source_hidden

    def show(self):
        self.shown = True
        self.source = self.source_shown


class ScreenLabel(Label):
    def clear(self):
        self.text = ''
