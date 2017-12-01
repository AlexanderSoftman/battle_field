from PyQt5 import QtWidgets, QtGui, QtCore
from battle_field.items.vehicle_models import bicycle_model_iter
from battle_field.items.vehicle_models import bicycle_model
import logging


LOG = logging.getLogger(__name__)


class FourWheels(QtWidgets.QGraphicsItemGroup):

    wa_max = 35
    wa_change = 1
    wheel_rad = 2
    rotation_line = None
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

        super(FourWheels, self).__init__()

        self.model = bicycle_model.VehicleModel(
            axis_dist=body_size["width"],
            wa_max=self.wa_max,
            wa_change=1,
            wheel_rad=wheel_size["diameter"] / 2,
            update_freq=30,
            bw_pos=init_pos["position"],
            heading=init_pos["heading"],
            wa_start=0,
            ws_start=0)

        # 1. body
        self.body = QtWidgets.QGraphicsRectItem(
            - body_size["width"] / 2,
            - body_size["height"] / 2,
            body_size["width"],
            body_size["height"],
            self)

        # 2. front wheel right
        self.front_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)
        self.front_wheel_right.setPos(
            QtCore.QPointF(
                body_size["width"] / 2,
                body_size["height"] / 2 + wheel_size["breadth"] / 2))

        # 3. front wheel left
        self.front_wheel_left = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)
        self.front_wheel_left.setPos(
            QtCore.QPointF(
                body_size["width"] / 2,
                - body_size["height"] / 2 - wheel_size["breadth"] / 2))

        # 4. back wheel right
        self.back_wheel_right = QtWidgets.QGraphicsRectItem(
            - body_size["width"] / 2 - wheel_size["diameter"] / 2,
            body_size["height"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)

        # 5. back wheel left
        self.back_wheel_left = QtWidgets.QGraphicsRectItem(
            - body_size["width"] / 2 - wheel_size["diameter"] / 2,
            - body_size["height"] / 2 - wheel_size["breadth"],
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)

        self.setRotation(init_pos["heading"])

    def increase_wa(self):
        self.model.increase_wa()

    def reduce_wa(self):
        self.model.reduce_wa()

    def increase_wheels_speed(self):
        self.model.increase_wheels_speed()

    def reduce_wheels_speed(self):
        self.model.reduce_wheels_speed()

    def update(self):
        self.model.update()
        model_pars = self.model.get_model_parameters()
        LOG.debug("model_pars = %s" % (model_pars,))
        self.setPos(model_pars["bw_pos"])
        # LOG.debug("pos = %s" % (self.pos(),))
        self.setRotation(model_pars["heading"])
        self.front_wheel_left.setRotation(model_pars["wa"])
        self.front_wheel_right.setRotation(model_pars["wa"])
        # remove old line
        if self.rotation_line is not None:
            self.scene().removeItem(
                self.rotation_line)
            self.rotation_line = None
        if "radius" in model_pars:
            sign = 0
            if model_pars["wa"] > 0:
                sign = 1
            else:
                sign = -1
            if model_pars["radius"] is not None:
                line_angle = model_pars["heading"] + sign * 90
                line = QtCore.QLineF(
                    model_pars["bw_pos"].x(),
                    model_pars["bw_pos"].y(),
                    model_pars["bw_pos"].x() + model_pars["radius"],
                    model_pars["bw_pos"].y())
                line.setAngle(-line_angle)
                self.rotation_line = self.scene().addLine(
                    line)
