from PyQt5 import QtCore
import math
import logging

LOG = logging.getLogger(__name__)


class CartModel():
    left_rotation_ps = 0
    right_rotation_ps = 0
    left_linear_pu = 0
    right_linear_pu = 0

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
        self.left_rotation_ps += self.ws_change
        self.left_linear_pu = self.wheel_rad * (
            self.left_rotation_ps /
            self.update_freq)

    def reduce_left_ws(self):
        self.left_rotation_ps -= self.ws_change
        self.left_linear_pu = self.wheel_rad * (
            self.left_rotation_ps /
            self.update_freq)

    def increase_right_ws(self):
        self.right_rotation_ps += self.ws_change
        self.right_linear_pu = self.wheel_rad * (
            self.right_rotation_ps /
            self.update_freq)

    def reduce_right_ws(self):
        self.right_rotation_ps -= self.ws_change
        self.right_linear_pu = self.wheel_rad * (
            self.right_rotation_ps /
            self.update_freq)

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
            self.left_linear_pu == 0 and
                self.right_linear_pu == 0):
            self.delta_radius = float('Inf')
            self.radius = None
            angle_speed_degrees = 0
            return
        # find speeds diff
        speed_diff = (
            self.left_linear_pu -
            self.right_linear_pu)
        # case 2 - speed diff = 0
        if speed_diff == 0:
            self.delta_radius = float('Inf')
            self.radius_point = None
            angle_speed_degrees = 0
            self.fw_pos = QtCore.QPointF(
                self.fw_pos.x() +
                self.left_linear_pu *
                math.cos(
                    math.radians(
                        self.heading)),
                self.fw_pos.y() -
                self.right_linear_pu *
                math.sin(
                    math.radians(
                        self.heading)))
            return
        # case 3 speed diff != 0
        # delta radius count from left wheel:
        if self.left_linear_pu != 0:
            self.delta_radius = int(
                self.left_linear_pu *
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
            angle_speed_degrees = (180 / math.pi) * (
                self.left_linear_pu /
                self.delta_radius)
        elif self.delta_radius == 0:
            angle_speed_degrees = (180 / math.pi) * (
                self.right_linear_pu /
                self.body_y)
            # invert sign
            angle_speed_degrees = -angle_speed_degrees
        else:
            angle_speed_degrees = (180 / math.pi) * (
                self.left_linear_pu /
                self.delta_radius)
        # move heading:
        self.heading -= angle_speed_degrees
        # move fw_pos
        line = QtCore.QLineF(
            self.radius_point,
            self.fw_pos)
        line.setAngle(
            line.angle() - angle_speed_degrees)
        self.fw_pos = line.p2()
