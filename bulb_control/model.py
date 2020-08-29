import json
import datetime
from tplight import LB130, Fake


class State:
    def __init__(self, ip, is_simulation):
        self.connected = False
        if is_simulation:
            self.bulb = Fake()
            self.connected = True
        else:
            try:
                self.bulb = LB130(ip)
                self.connected = True
            except:
                self.bulb = Fake()
        self.bulb.transition_period = 0
        self.target_brightness = None

    @property
    def now(self):
        return datetime.datetime.now().time()

    @property
    def brightness(self):
        state = json.loads(self.bulb.status())
        return int(state['system']['get_sysinfo']['light_state']['brightness'])

    @brightness.setter
    def brightness(self, value):
        self.bulb.brightness = value

    def transit(self, target_value):
        """
        Args:
            target_value (int): traget brightness value
            period (int): the transition time, unit is second
        """
        diff = target_value - self.brightness
        if diff == 0:
            return
        else:
            diff = int(diff / abs(diff))  # change 1 per second
            self.brightness = self.brightness + diff
            return
