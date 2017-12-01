from PyQt5 import QtCore, QtGui
import math
import logging

LOG = logging.getLogger(__name__)


# wa = wheel angle
# bw = back wheels
# fw = front wheels
# ws = wheel speed
class VehicleModel():

    def __init__(
        self,
        axis_dist=10,
        wa_max=35,
        wa_change=1,
        wheel_rad=2,
        update_freq=30,
        bw_pos=QtCore.QPointF(0, 0),
        heading=0,
        wa_start=0,
            ws_start=0):
        self.axis_dist = axis_dist
        self.wa_max = wa_max
        self.wa_change = wa_change
        self.wheel_length = (2 * math.pi * wheel_rad)
        self.update_freq = update_freq
        # initial model values:
        self.heading = heading
        self.bw_pos = bw_pos
        self.fw_pos = (self.bw_pos + QtCore.QPointF(
            self.axis_dist * math.cos(self.heading),
            self.axis_dist * math.sin(self.heading)))
        self.wa = wa_start
        self.ws = ws_start
        self.radius_of_turning = 0
        self.update()

    # Positive values for the angles mean counter-clockwise
    def increase_wa(self):
        if not self.wa + self.wa_change > self.wa_max:
            self.wa += self.wa_change
        LOG.debug("increase_wa: wa = %s" % (self.wa,))

    def reduce_wa(self):
        if not abs(self.wa - self.wa_change) > abs(self.wa_max):
            self.wa -= self.wa_change
        LOG.debug("reduce_wa: wa = %s" % (self.wa,))

    def increase_wheels_speed(self):
        self.ws += 1
        LOG.debug("increase_ws: ws = %s" % (self.ws,))

    def reduce_wheels_speed(self):
        self.ws -= 1
        LOG.debug("reduce_ws: ws = %s" % (self.ws,))

    def distance_per_update(self):
        return (self.ws / self.update_freq *
                self.wheel_length)

    def update(self):
        dist_pu = self.distance_per_update()
        wa_tan = math.tan(self.wa * math.pi / 180)
        # LOG.debug("wa_tan = %s" % (wa_tan, ))
        if wa_tan == 0:
            self.radius_of_turning = None
        else:
            self.radius_of_turning = self.axis_dist / wa_tan
        # display radius of turning
        bw_dist_pu = dist_pu * math.cos(
            self.wa * math.pi / 180)
        # find rotation speed in radians
        omega_bw_pu = bw_dist_pu * wa_tan / self.axis_dist
        # convert omega from rad per sec to degrees per sec
        omega_bw_pu = 180 * omega_bw_pu / math.pi
        self.heading += omega_bw_pu
        bw_pos_new = QtCore.QPointF(
            self.bw_pos.x() + bw_dist_pu * math.cos(
                self.heading * math.pi / 180),
            self.bw_pos.y() + bw_dist_pu * math.sin(
                self.heading * math.pi / 180))
        self.bw_pos = bw_pos_new

    # return tuple of:
    # bw_pos - QPointF
    # fw_pos - QPointF
    # heading - QVector2D
    # wheels_angle - degrees
    # radius of turning
    def get_model_parameters(self):
        return {
            "bw_pos": self.bw_pos,
            "heading": self.heading,
            "wa": self.wa,
            "radius": self.radius_of_turning
        }
