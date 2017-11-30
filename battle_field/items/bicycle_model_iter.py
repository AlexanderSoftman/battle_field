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
            heading=0):
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
        self.wa = 0
        self.ws = 0

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
        dist = self.distance_per_update()
        #distance_projections = {
            #"to_heading": dist *
            #math.cos(self.wa * math.pi / 180),
            #"perpendicularly_heading": dist *
            #math.sin(self.wa * math.pi / 180)}
        # LOG.debug("dist projections = %s" % (distance_projections,))
        # new front wheels position
        fw_pos_cur = QtCore.QPointF(
            self.bw_pos.x() + self.axis_dist * math.cos(
                self.heading * math.pi / 180),
            self.bw_pos.y() + self.axis_dist * math.sin(
                self.heading * math.pi / 180))
        fw_pos_delta = {
            "x": dist * math.cos(
                (self.wa + self.heading) * math.pi / 180),
            "y": dist * math.sin(
                (self.wa + self.heading) * math.pi / 180)
        }
        fw_pos_new = QtCore.QPointF(
            fw_pos_cur.x() + fw_pos_delta["x"],
            fw_pos_cur.y() + fw_pos_delta["y"])
        #fw_pos = (
            #self.bw_pos +
            #QtCore.QPointF(
                #self.axis_dist * math.cos(
                    #self.heading * math.pi / 180),
                #self.axis_dist * math.sin(
                    #self.heading * math.pi / 180)) +
            #QtCore.QPointF(
                #distance_projections["to_heading"] * math.cos(
                    #self.heading * math.pi / 180),
                #distance_projections["perpendicularly_heading"] *
                #math.sin(
                    #self.heading * math.pi / 180)))

        # recalculated back point coordinates
        bw_dist = dist * math.cos(
            self.wa * math.pi / 180)
        bw_pos_new = QtCore.QPointF(
            self.bw_pos.x() + bw_dist * math.cos(
                self.heading * math.pi / 180),
            self.bw_pos.y() + bw_dist * math.sin(
                self.heading * math.pi / 180))

        #self.bw_pos += QtCore.QPointF(
            #distance_projections["to_heading"] *
            #math.cos(self.heading * math.pi / 180),
            #distance_projections["to_heading"] *
            #math.sin(self.heading * math.pi / 180))
        self.bw_pos = bw_pos_new
        # recalculate heading
        LOG.debug("heading old = %s" % (self.heading,))
        LOG.debug("bw_pos_new = %s" % (bw_pos_new,))
        LOG.debug("fw_pos_new = %s" % (fw_pos_new,))
        self.heading = - QtCore.QLineF(
            bw_pos_new, fw_pos_new).angle()
        LOG.debug("heading new = %s" % (self.heading,))

    # return tuple of:
    # bw_pos - QPointF
    # fw_pos - QPointF
    # heading - QVector2D
    # wheels_angle - degrees
    def get_model_parameters(self):
        return {
            "bw_pos": self.bw_pos,
            "fw_pos": self.fw_pos,
            "heading": self.heading,
            "wa": self.wa
        }
