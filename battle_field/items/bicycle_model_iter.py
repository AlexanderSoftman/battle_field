from PyQt5 import QtCore, QtGui
import math


# wa = wheel angle
# bw = back wheels
# fw = front wheels
# ws = wheel speed
class VehicleModel():

    def __init__(
        self,
        axis_dist=10,
        fw_dist=3,
        bw_dist=3,
        wa_max=30,
        wa_change=1,
        wheel_rad=2,
        update_freq=30,
        bw_pos=0,
            heading=QtGui.QVector2D(1, 0)):
        self.axis_dist = axis_dist
        self.fw_dist = fw_dist
        self.bw_dist = bw_dist
        self.wa_max = wa_max
        self.wa_change = wa_change
        self.wheel_length = (2 * math.pi * wheel_rad)
        self.update_freq = update_freq
        # initial model values:
        self.heading = heading
        self.bw_pos = bw_pos
        self.fw_pos = (self.bw_pos + QtCore.QPointF(
            self.axis_dist * self.heading.x(),
            self.axis_dist * self.heading.y()))
        self.wa = 0
        self.ws = 0

    # Positive values for the angles mean counter-clockwise
    def increase_wa(self):
        if (self.wa_max <
                self.wa + self.wa_change):
            self.wa += self.wa_change

    def reduce_wa(self):
        if (self.wa_max >
                self.wa - self.wa_change):
            self.wa -= self.wa_change

    def increase_wheels_speed(self):
        self.ws += 1

    def reduce_wheels_speed(self):
        self.ws -= 1

    def distance_per_update(self):
        return (self.ws / self.update_freq *
                self.wheel_length)

    def update(self):
        dist = self.distance_per_update()
        distance_projections = {
            "to_heading": dist *
            math.cos(self.wa * math.pi / 180),
            "perpendicularly_heading": dist *
            math.sin(self.wa * math.pi / 180)}

        # new front wheels position
        fw_pos = (
            self.bw_pos +
            QtCore.QPointF(
                self.axis_dist * self.heading.x(),
                self.axis_dist * self.heading.y()) +
            QtCore.QPointF(
                distance_projections["to_heading"] * self.heading.x(),
                distance_projections["perpendicularly_heading"] *
                self.heading.y()))

        # recalculated back point coordinates
        self.bw_pos += QtCore.QPointF(
            distance_projections["to_heading"] *
            self.heading.x(),
            distance_projections["to_heading"] *
            self.heading.y())

        # recalculate heading
        self.heading = QtGui.QVector2D(
            self.bw_pos, fw_pos)

        # normalize heading:
        self.heading = self.heading.normalized()

    # return tuple of:
    # bw_pos - QPointF
    # fw_pos - QPointF
    # heading - QVector2D
    # wheels_angle - degrees
    def get_model_parameters(self):
        return (
            self.bw_pos,
            self.fw_pos,
            self.heading,
            self.wa)
