from PyQt5 import QtWidgets, QtCore
from battle_field.items.vehicle_models import cart_model
from battle_field.items.devices_models import odometer_model
from battle_field.items.devices_models import lidar
import logging
import math

LOG = logging.getLogger(__name__)


class Cart(QtWidgets.QGraphicsItemGroup):

    ws_change = 1
    radius_line = None
    count_of_odometer_slots = 100
    lidar = None

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
        update_freq,
        info_callbacks,
        show_radius,
        body_size,
        init_pos,
            wheel_size):

        super(Cart, self).__init__()

        self.scene_m = scene
        self.update_freq = update_freq
        self.show_radius = show_radius
        self.axis_dist = body_size["x"]
        self.wheel_rad = wheel_size["diameter"] / 2
        # 0. model
        self.model = cart_model.CartModel(
            body_x=self.axis_dist,
            body_y=body_size["y"],
            ws_change=self.ws_change,
            wheel_rad=self.wheel_rad,
            update_freq=self.update_freq,
            fw_pos=init_pos["position"],
            heading=(-init_pos["heading"]))

        # 1. body
        self.body = QtWidgets.QGraphicsRectItem(
            - body_size["x"] + wheel_size["diameter"] / 2,
            - body_size["y"] / 2,
            body_size["x"],
            body_size["y"],
            self)

        # 2. front wheel right
        self.front_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            body_size["y"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)

        # 3. front wheel left
        self.front_wheel_left = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] - body_size["y"] / 2,
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
            - body_size["x"] + wheel_size["diameter"], 0)

        self.setPos(init_pos["position"])
        self.setRotation(init_pos["heading"])

        # 5. create two odometers
        left_odometer_callback = None
        right_odometer_callback = None

        if info_callbacks is not None and "odometer_left" in info_callbacks:
            left_odometer_callback = info_callbacks["odometer_left"]
        if info_callbacks is not None and "odometer_right" in info_callbacks:
            right_odometer_callback = info_callbacks["odometer_right"]

        self.odometers = {
            "left": odometer_model.OdometerModel(
                self.count_of_odometer_slots,
                0,
                self.update_freq,
                left_odometer_callback,
                None),
            "right":
                odometer_model.OdometerModel(
                self.count_of_odometer_slots,
                0,
                self.update_freq,
                right_odometer_callback,
                None)
        }

        # 6. create lidar
        if info_callbacks is not None and "lidar" in info_callbacks:
            self.lidar = lidar.Lidar(
                self,
                30,
                10,
                30,
                info_callbacks["lidar"],
                180,
                800,
                None)

    def increase_left_ws(self):
        self.model.increase_left_ws()
        self.odometers["left"].change_speed(self.ws_change)

    def reduce_left_ws(self):
        self.model.reduce_left_ws()
        self.odometers["left"].change_speed(-self.ws_change)

    def increase_right_ws(self):
        self.model.increase_right_ws()
        self.odometers["right"].change_speed(self.ws_change)

    def reduce_right_ws(self):
        self.model.reduce_right_ws()
        self.odometers["right"].change_speed(-self.ws_change)

    def update(self):
        self.model.update()
        model_pars = self.model.get_model_parameters()
        self.setPos(model_pars["fw_pos"])
        self.setRotation(-model_pars["heading"])
        # LOG.debug("pos = %s" % (model_pars["fw_pos"],))
        self.odometers["left"].update()
        self.odometers["right"].update()
        # remove old line
        if self.show_radius is not True:
            return
        if self.radius_line is not None:
            self.scene_m.removeItem(
                self.radius_line)
            self.radius_line = None
        if model_pars["radius_point"] is not None:
            line = QtCore.QLineF(
                model_pars["radius_point"],
                model_pars["fw_pos"])
            self.radius_line = self.scene_m.addLine(
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
