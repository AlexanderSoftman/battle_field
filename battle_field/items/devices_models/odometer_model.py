import logging
import math
import numpy

LOG = logging.getLogger(__name__)


# OdometerModel:
# ps - per second
# pu - per update
class OdometerModel():

    # residue of rotation
    residue = 0
    speed_last_sign = 1
    callback = None

    # input values:
    # 1. count_of_slots on disk
    # 2. angle_speed - rotation speed
    # 3. update_freq
    # 4. callback function - call when we reached slot
    # 5. error_model
    def __init__(
        self,
        count_of_slots,
        angle_speed_ps,
        update_freq,
        callback,
            error_model):
        self.update_freq = update_freq
        self.count_of_slots = count_of_slots
        self.error_model = error_model
        self.angle_speed_ps = angle_speed_ps
        if self.angle_speed_ps < 0:
            self.speed_last_sign = -1
        self.angle_speed_pu = self.angle_speed_ps / self.update_freq
        self.angle_between_slots = 2 * math.pi / self.count_of_slots
        if callback is not None:
            self.callback = callback

    # called update_freq times per second
    def update(self):
        count_of_strobes = (
            math.fabs(
                (self.residue +
                    self.angle_speed_pu)) //
            self.angle_between_slots)
        sign = int(
            numpy.sign(
                self.residue +
                self.angle_speed_pu))
        self.residue = math.fmod(
            (self.residue +
                self.angle_speed_pu),
            self.angle_between_slots)

        if self.callback is not None:
            self.callback(sign * count_of_strobes)

    # speed measured in radians per second
    def change_speed(self, value):
        self.angle_speed_ps += value
        self.angle_speed_pu = self.angle_speed_ps / self.update_freq
        # we need change residue sign if sign of speed changed
        if (
            (self.speed_last_sign < 0) and
            (self.angle_speed_ps >= 0) or (
                (self.speed_last_sign > 0) and
                (self.angle_speed_ps < 0))):
            self.residue = -1 * self.residue
            self.speed_last_sign = -1 * self.speed_last_sign
