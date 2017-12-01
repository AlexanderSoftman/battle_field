from battle_field.items.vehicle_models import articulated_model
from PyQt5 import QtWidgets, QtCore
import logging

LOG = logging.getLogger(__name__)


class Articulated(QtWidgets.QGraphicsItemGroup):

    wheels_dist = 40
    wheels_axis_breadth = 1
    body_breadth = 1
    front_angle_max = 60
    front_angle_change = 1
    front_angle_init = 0

    # input values:
    # 1) scene
    # 2) frame_length = {
    #   "back",
    #   "front"}
    # 3) init_pos = {
    # "position" = QPointF(),
    # "heading" = degrees
    # 4) wheel_size = {
    # "breadth"
    # "diameter" }

    def __init__(
        self,
        scene,
        frame_length,
        init_pos,
            wheel_size):

        super(Articulated, self).__init__()

        # model place
        self.model = articulated_model.ArticulatedModel(
            frame_length=frame_length,
            wheel_rad=wheel_size["diameter"] / 2,
            max_angle=self.front_angle_max,
            angle_change=1,
            update_freq=30,
            bw_pos=init_pos["position"],
            heading=init_pos["heading"])

        # 1. back wheels axis
        self.back_wheels_axis = QtWidgets.QGraphicsRectItem(
            - self.wheels_axis_breadth / 2,
            - self.wheels_dist / 2,
            self.wheels_axis_breadth,
            self.wheels_dist,
            self)
        self.back_wheels_axis.setPos(0, 0)

        # 2. back left wheel
        self.back_wheel_left = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)
        self.back_wheel_left.setPos(
            0,
            - wheel_size["breadth"] / 2 - self.wheels_dist / 2)

        # 3. back right wheel
        self.back_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self)
        self.back_wheel_right.setPos(
            0,
            wheel_size["breadth"] / 2 + self.wheels_dist / 2)

        # 4. frame_back
        self.frame_back = QtWidgets.QGraphicsRectItem(
            - frame_length["back"] / 2,
            - self.body_breadth / 2,
            frame_length["back"],
            self.body_breadth,
            self)
        self.frame_back.setPos(
            frame_length["back"] / 2 + self.wheels_axis_breadth / 2,
            0)

        # 5. point of articulation
        self.point_of_articulation = QtWidgets.QGraphicsEllipseItem(
            0 - 2.5,
            0 - 2.5,
            5,
            5,
            self)
        self.point_of_articulation.setPos(
            frame_length["back"] + self.wheels_axis_breadth / 2,
            0)

        # 6. prepare front
        self.front = QtWidgets.QGraphicsItemGroup(self)

        # 7. frame_front
        self.frame_front = QtWidgets.QGraphicsRectItem(
            - frame_length["front"] / 2,
            - self.body_breadth / 2,
            frame_length["front"],
            self.body_breadth,
            self.front)
        self.frame_front.setPos(
            frame_length["front"] / 2,
            0)

        # 8. front wheels axis
        self.front_wheels_axis = QtWidgets.QGraphicsRectItem(
            - self.wheels_axis_breadth / 2,
            - self.wheels_dist / 2,
            self.wheels_axis_breadth,
            self.wheels_dist,
            self.front)
        self.front_wheels_axis.setPos(
            frame_length["front"] + self.wheels_axis_breadth / 2,
            0)

        # 9. front right wheel
        self.front_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self.front)
        self.front_wheel_right.setPos(
            frame_length["front"] + self.wheels_axis_breadth / 2,
            wheel_size["breadth"] / 2 + self.wheels_dist / 2)

        # 10. front left wheel
        self.front_wheel_right = QtWidgets.QGraphicsRectItem(
            - wheel_size["diameter"] / 2,
            - wheel_size["breadth"] / 2,
            wheel_size["diameter"],
            wheel_size["breadth"],
            self.front)
        self.front_wheel_right.setPos(
            frame_length["front"] + self.wheels_axis_breadth / 2,
            - wheel_size["breadth"] / 2 - self.wheels_dist / 2)

        # 11. setup all front position
        self.front.setPos(
            frame_length["back"],
            0)

        # 12. setup front angle initial
        self.front_angle = self.front_angle_init
        self.front.setRotation(self.front_angle)

        # 13. initial heading
        self.setRotation(init_pos["heading"])

        # 14. rotation line
        self.rotation_line = None

    # Positive values for the angles mean counter-clockwise
    def increase_angle(self):
        self.model.increase_angle()

    def reduce_angle(self):
        self.model.reduce_angle()

    def increase_wheels_speed(self):
        self.model.increase_wheels_speed()

    def reduce_wheels_speed(self):
        self.model.reduce_wheels_speed()

    def update(self):
        self.model.update()
        model_pars = self.model.get_model_parameters()
        self.setPos(model_pars["bw_pos"])
        self.setRotation(model_pars["heading"])
        self.front.setRotation(model_pars["angle"])
        # remove old line
        if self.rotation_line is not None:
            self.scene().removeItem(
                self.rotation_line)
            self.rotation_line = None
        if "radius" in model_pars:
            sign = 0
            if model_pars["angle"] > 0:
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
