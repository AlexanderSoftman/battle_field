from PyQt5 import QtCore, QtGui
import math
import logging

LOG = logging.getLogger(__name__)


class CartModel():
    left_rotation_speed = 0
    right_rotation_speed = 0
    radius_point = None
    delta_radius = 0

    def __init__(
        self,
        body_x=100,
        body_y=50,
        ws_change=1,
        wheel_rad=2,
        update_freq=30,
        fw_pos=QtCore.QPointF(0, 0),
            heading=0):
        self.body_x = body_x
        self.body_y = body_y
        self.ws_change = ws_change
        self.wheel_rad = wheel_rad
        self.update_freq = update_freq
        # initial model values:
        self.heading = heading
        self.fw_pos = fw_pos
        self.back_wheel_angle = self.heading

    def increase_left_ws(self):
        self.left_rotation_speed += self.ws_change

    def reduce_left_ws(self):
        self.left_rotation_speed -= self.ws_change

    def increase_right_ws(self):
        self.right_rotation_speed += self.ws_change

    def reduce_right_ws(self):
        self.right_rotation_speed -= self.ws_change

    def speed_per_update(self, ws):
        speed = self.wheel_rad * (
            ws / self.update_freq)
        return speed

    def get_model_parameters(self):
        return {
            "fw_pos": self.fw_pos,
            "heading": self.heading,
            "radius_point": self.radius_point,
            "delta_radius": self.delta_radius - self.body_x / 2
        }

    def update(self):
        # 1 case speeds == 0
        if (
            self.left_rotation_speed == 0 and
                self.right_rotation_speed == 0):
            self.delta_radius = float('Inf')
            self.radius = None
            angle_speed = 0
            return
        # find speeds diff
        speed_diff = self.speed_per_update(
            self.left_rotation_speed -
            self.right_rotation_speed)
        # case 2 - speed diff = 0
        if speed_diff == 0:
            self.delta_radius = float('Inf')
            self.radius_point = None
            angle_speed = 0
            self.fw_pos = QtCore.QPointF(
                self.fw_pos.x() +
                self.speed_per_update(self.left_rotation_speed) *
                math.cos(
                    math.radians(
                        self.heading)),
                self.fw_pos.y() -
                self.speed_per_update(self.right_rotation_speed) *
                math.sin(
                    math.radians(
                        self.heading)))
            return
        # case 3 speed diff != 0
        # delta radius count from left wheel:
        if self.left_rotation_speed != 0:
            self.delta_radius = int(
                self.speed_per_update(
                    self.left_rotation_speed) *
                self.body_y /
                speed_diff)
        else:
            self.delta_radius = 0
        left_wheel = QtCore.QPointF(
            self.fw_pos.x() -
            self.body_y / 2 * math.cos(math.radians(
                180 - 90 - self.heading)),
            self.fw_pos.y() -
            self.body_y / 2 * math.sin(math.radians(
                180 - 90 - self.heading)))
        # radius point
        self.radius_point = QtCore.QPointF(
            left_wheel.x() +
            self.delta_radius * math.sin(math.radians(
                self.heading)),
            left_wheel.y() +
            self.delta_radius * math.cos(math.radians(
                self.heading)))
        # angle speeds
        if self.delta_radius == self.body_y:
            angle_speed = (
                self.left_rotation_speed *
                self.update_freq /
                self.delta_radius)
        elif self.delta_radius == 0:
            angle_speed = - (
                self.right_rotation_speed *
                self.update_freq /
                self.body_y)
        else:
            angle_speed = (
                self.left_rotation_speed *
                self.update_freq /
                self.delta_radius)
        # move heading:
        self.heading -= angle_speed
        # move fw_pos
        line = QtCore.QLineF(
            self.radius_point,
            self.fw_pos)
        line.setAngle(
            line.angle() - angle_speed)
        self.fw_pos = line.p2()
