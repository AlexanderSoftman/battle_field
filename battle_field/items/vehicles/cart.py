from PyQt5 import QtWidgets, QtCore
from battle_field.items.vehicle_models import cart_model
import logging
import math

LOG = logging.getLogger(__name__)


class Cart(QtWidgets.QGraphicsItemGroup):

    wa_change = 1
    radius_line = None

    # input values:
    # 1) scene
    # 2) body size = {
    #   "widht",
    #   "height"}
    # 3) init_pos = {
    # "position" = QPointF(),
    # "heading" = degrees
    # 4) wheel_size = {
    # "breadth"
    # "diameter" }
    def __init__(
        self,
        scene,
        body_size,
        init_pos,
            wheel_size):

        super(Cart, self).__init__()

        self.scene = scene
        self.axis_dist = body_size["width"]

        # 0. model
        self.model = cart_model.CartModel(
            body_x=self.axis_dist,
            body_y=body_size["height"],
            ws_change=1,
            wheel_rad=wheel_size["diameter"] / 2,
            update_freq=30,
            fw_pos=init_pos["position"],
            heading=(-init_pos["heading"]))

        # 1. body
        self.body = QtWidgets.QGraphicsRectItem(
            - body_size["width"] + wheel_size["diameter"] / 2,
            - body_size["height"] / 2,
            body_size["width"],
            body_size["height"],
            self)

        # 2. front wheel right
        self.front_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            body_size["height"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)

        # 3. front wheel left
        self.front_wheel_left = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] - body_size["height"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)

        # 4. back wheel
        self.back_wheel = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)
        self.back_wheel.setPos(
            - body_size["width"] + wheel_size["diameter"], 0)

        self.setPos(init_pos["position"])
        self.setRotation(init_pos["heading"])

    def increase_left_ws(self):
        self.model.increase_left_ws()

    def reduce_left_ws(self):
        self.model.reduce_left_ws()

    def increase_right_ws(self):
        self.model.increase_right_ws()

    def reduce_right_ws(self):
        self.model.reduce_right_ws()

    def update(self):
        self.model.update()
        model_pars = self.model.get_model_parameters()
        self.setPos(model_pars["fw_pos"])
        self.setRotation(-model_pars["heading"])
        # remove old line
        if self.radius_line is not None:
            self.scene.removeItem(
                self.radius_line)
            self.radius_line = None
        if model_pars["radius_point"] is not None:
            line = QtCore.QLineF(
                model_pars["radius_point"],
                model_pars["fw_pos"])
            self.radius_line = self.scene.addLine(
                line)
            if model_pars["delta_radius"] == 0:
                self.back_wheel.setRotation(90)
            else:
                self.back_wheel.setRotation(
                    - math.degrees(
                        math.atan(
                            self.axis_dist /
                            model_pars["delta_radius"])))
        else:
            self.back_wheel.setRotation(0)
