import math
import kivy
kivy.require('1.0.1')
from kivy.app import App  # noqa: E402
from kivy.uix.button import Button  # noqa: E402


class LifePodApp(App):
    pass


class BlueButton(Button):
    pass


class EnterButton(BlueButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)
    
    def callback(self, instance):
        print(instance.text)


class SpinButton(BlueButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)
    
    def callback(self, instance):
        print(instance.text)


class UndoButton(BlueButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)
    
    def callback(self, instance):
        print(instance.text)


class DollarUnitButton(BlueButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)
    
    def callback(self, instance):
        print(instance.text)


class LifePointsUnitButton(BlueButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)
    
    def callback(self, instance):
        print(instance.text)


class RedButton(Button):
    pass


class MinusButton(RedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        print(instance.text)


class PlusButton(RedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        print(instance.text)


class NumButton(Button):
    # NOTE: Several attributes are set with methods after __init__ because they
    # depend on the 'self.idx' value, which is set in the KV file after
    # __init__ is run.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.callback)

    def callback(self, instance):
        print(self.get_id())

    def get_id(self):
        # Sets instance attribute here, and is used to set value in KV file.
        self.id = f"n{str(self.idx)}"
        return self.id

    def get_text(self):
        # Sets instance attribute here, and is used to set value in KV file.
        self.text = str(self.idx)
        return self.text

    def get_pos_hint(self):
        # Sets instance attribute here, and is used to set value in KV file.
        self.pos_hint = {'center_x': 0.5 + self.x_offset(), 'center_y': 0.5 + self.y_offset()}
        return self.pos_hint

    def x_offset(self):
        rads = math.radians(360*(1 - self.idx) / 11)
        offset = -0.4 * math.sin(rads)
        return offset

    def y_offset(self):
        rads = math.radians(360*(1 - self.idx) / 11)
        offset = 0.4 * math.cos(rads)
        return offset
