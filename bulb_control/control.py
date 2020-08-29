#!/usr/bin/env python3
import time
import threading
from model import State
from view import Slide, TimeEntry, AutoPanel, QHLine, Main, warn


class Controller():
    def __init__(self):
        self.gui = Main()
        self.state = State(self.gui.ip, self.gui.is_simulation)
        self.gui.slide.set_value(self.brightness)
        self.__set_slots()
        if self.state.connected:
            self.__set_function_slots()
        else:
            self.__disable_function_slots()

    @property
    def brightness(self):
        return self.state.brightness

    @brightness.setter
    def brightness(self, value):
        self.state.brightness = value
        self.gui.slide.set_value(value)

    @property
    def is_daytime(self):
        after_morning = self.gui.auto.start < self.state.now
        before_evening = self.gui.auto.end > self.state.now
        return after_morning and before_evening

    @property
    def target(self):
        return self.gui.auto.target


    def __set_slots(self):
        self.gui.connection.set_button_callback(self.__connect)

    def __set_function_slots(self):
        try:
            self.gui.disconnect_function_slots()
        except TypeError:
            pass
        self.gui.slide.set_change_callback(self.__change_brightness)
        self.gui.slide.set_release_callback(self.__set_brightness)
        self.gui.auto.set_check_callback(self.__set_auto_mode)

    def __disable_function_slots(self):
        self.gui.disconnect_function_slots()
        self.gui.slide.set_change_callback(lambda: warn("Not connected to bulb"))
        self.gui.slide.set_release_callback(lambda: warn("Not connected to bulb"))
        self.gui.auto.set_check_callback(lambda: warn("Not connected to bulb"))

    def __connect(self):
        self.state = State(self.gui.ip, self.gui.is_simulation)
        self.gui.set_connection_state(self.state.connected)
        if self.state.connected:
            self.__set_function_slots()
        else:
            warn("Connection Failed!")
            self.__disable_function_slots()

    def __change_brightness(self, value):
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        value = int(value)
        self.gui.slide.set_value(value)

    def __set_brightness(self):
        self.brightness = self.gui.slide.get_value()

    def __set_auto_mode(self):
        if self.gui.is_checked:
            thread = threading.Thread(target=self.auto_control, daemon=True)
            thread.start()
        else:
            self.gui.auto.set_text("")

    def auto_control(self):
        while self.gui.is_checked:
            if self.is_daytime:
                self.gui.auto.set_text(" (Targeting {})".format(self.target))
                self.state.transit(target_value=self.target)
                time.sleep(2)
            else:
                self.gui.auto.set_text(" (Targeting 0)")
                self.state.transit(target_value=0)
                time.sleep(2)
            self.gui.slide.set_value(self.brightness)

