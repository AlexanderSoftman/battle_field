from PyQt5 import QtCore
import logging
import math

LOG = logging.getLogger(__name__)


class ArticulatedModel():

    wheels_speed = 0
    angle = 0

    def __init__(
        self,
        frame_length={
            "back",
            "front"},
        wheel_rad=2,
        max_angle=35,
        angle_change=1,
        update_freq=30,
        bw_pos=QtCore.QPointF(0, 0),
            heading=0):

        self.frame_length = frame_length
        self.max_angle = max_angle
        self.angle_change = angle_change
        self.wheel_rad = wheel_rad
        self.wheel_length = (2 * math.pi * wheel_rad)
        self.update_freq = update_freq
        # initial model values:
        self.heading = heading
        self.bw_pos = bw_pos
        # LOG.debug("before create new bicycle model")
        # self.create_new_bicycle_model()

    # Positive values for the angles mean counter-clockwise
    def increase_angle(self):
        if not (
            self.angle +
            self.angle_change >
                self.max_angle):
            self.angle += self.angle_change

    def reduce_angle(self):
        if not (
            abs(self.angle -
                self.angle_change) >
                abs(self.max_angle)):
            self.angle -= self.angle_change

    def increase_wheels_speed(self):
        self.wheels_speed += 1

    def reduce_wheels_speed(self):
        self.wheels_speed -= 1

    def distance_per_update(self):
        return (self.wheels_speed / self.update_freq *
                self.wheel_length)

    def update(self):
        dist_pu = self.distance_per_update()
        angle_tan = math.tan(self.angle * math.pi / 180)
        equivalent_axis_dist = (
            self.frame_length["back"] +
            self.frame_length["front"] / math.cos(
                self.angle * math.pi / 180))
        if angle_tan == 0:
            self.radius_of_turning = None
        else:
            self.radius_of_turning = equivalent_axis_dist / angle_tan
        # display radius of turning
        bw_dist_pu = dist_pu * math.cos(
            self.angle * math.pi / 180)
        # find rotation speed in radians
        omega_bw_pu = bw_dist_pu * angle_tan / equivalent_axis_dist
        # convert omega from rad per sec to degrees per sec
        omega_bw_pu = 180 * omega_bw_pu / math.pi
        self.heading += omega_bw_pu
        bw_pos_new = QtCore.QPointF(
            self.bw_pos.x() + bw_dist_pu * math.cos(
                self.heading * math.pi / 180),
            self.bw_pos.y() + bw_dist_pu * math.sin(
                self.heading * math.pi / 180))
        self.bw_pos = bw_pos_new

    def get_model_parameters(self):
        return {
            "bw_pos": self.bw_pos,
            "heading": self.heading,
            "angle": self.angle,
            "radius": self.radius_of_turning,
        }
