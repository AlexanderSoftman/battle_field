import sys
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from battle_field import real_scene
from battle_field import model_scene
from PyQt5 import uic
import math
import enum

from battle_field.items.vehicles.tank import tank
from battle_field.items.vehicles import four_wheels
from battle_field.items.vehicles import articulated
from battle_field.items.vehicles import cart


LOG = logging.getLogger(__name__)


class User(enum.Enum):
    TANK = 1
    FRONT_DRIVING_FOUR_WHEELS = 2
    ARTICULATED_FOUR_WHEELS = 3
    CART = 4


class MainWindow(QtWidgets.QMainWindow):

    obstackles_count_maximum = 5
    obstacles_pos = []
    scene_size = {
        "x": 2000,
        "y": 2000
    }
    update_freq = 30.0

    # choose one of this guys
    # TANK
    # FRONT_DRIVING_FOUR_WHEELS
    # ARTICULATED_FOUR_WHEELS
    # CART
    user = User.CART

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "battle_field.ui"),
            self)
        self.setWindowTitle("BATTLE_FIELD")
        self.setWindowIcon(
            QtGui.QIcon(
                os.path.join(
                    os.path.split(
                        __file__)[0], 'icon.png')))

        # create scenes rect:
        scene_rect = QtCore.QRectF(
            - self.scene_size["x"] / 2,
            - self.scene_size["y"] / 2,
            self.scene_size["x"],
            self.scene_size["y"],
        )

        # generate obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            self.obstacles_pos.append(QtCore.QPointF(pos_x, pos_y))

        # information_scene
        self.model_sw = model_scene.ModelScene(
            scene_rect,
            self.obstacles_pos)
        self.info_scene.setScene(self.model_sw)
        self.info_scene.installEventFilter(self.model_sw)
        self.info_scene.setRenderHints(
            QtGui.QPainter.HighQualityAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.info_scene.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.info_scene.setViewportUpdateMode(
            QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.info_scene.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.info_scene.setWindowTitle("Information")
        # self.info_scene.scale(4, 4)

        self.real_sw = real_scene.RealScene(
            scene_rect,
            self.obstacles_pos,
            self.update_freq)
        self.main_scene.setScene(self.real_sw)
        self.main_scene.installEventFilter(self.real_sw)
        self.main_scene.setRenderHints(
            QtGui.QPainter.HighQualityAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.main_scene.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.main_scene.setViewportUpdateMode(
            QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.main_scene.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.main_scene.setWindowTitle("Battleground")
        # self.main_scene.scale(4, 4)

        # create vehicle models
        self.real_vehicle = self.create_user(
            self.user,
            self.real_sw)
        self.real_sw.addItem(self.real_vehicle)

        self.model_vehicle = self.create_user(
            self.user,
            self.model_sw)
        self.model_sw.addItem(self.model_vehicle)

        # create timer for both scenes
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / self.update_freq
        self.timer.start(self.dt * 1000)
        self.time = QtCore.QTime()
        self.time.start()

    def timerEvent(self):
        self.real_sw.update()
        if isinstance(self.real_vehicle, cart.Cart):
            LOG.critical("isinstance(self.real_vehicle, cart.Cart):")
            self.model_vehicle.model.left_linear_pu = (
                self.real_vehicle.odometers[
                    "left"].count_of_strobes_with_sign *
                (2 * math.pi /
                    self.real_vehicle.odometers["left"].count_of_slots) *
                self.real_sw.vehicle.model.wheel_rad)
            self.model_vehicle.model.right_linear_pu = (
                self.real_vehicle.odometers[
                    "right"].count_of_strobes_with_sign *
                (2 * math.pi /
                    self.real_vehicle.odometers["right"].count_of_slots) *
                self.real_sw.vehicle.model.wheel_rad)
            LOG.critical("self.model_vehicle.model.left_linear_pu: %s" % (
                self.model_vehicle.model.left_linear_pu))
            LOG.critical("self.model_vehicle.model.right_linear_pu: %s" % (
                self.model_vehicle.model.right_linear_pu))
        self.model_sw.update()
        if isinstance(self.real_vehicle, cart.Cart):
            # get lidar measures first
            self.lidar_processing(
                self.real_vehicle.lidar.lidar_model.carrier_item,
                self.real_vehicle.lidar.lidar_model.memory,
                - self.real_vehicle.lidar.lidar_model.lidars_half_angle,
                self.real_vehicle.lidar.lidar_model.angle_step)

    # expect input value - list of tuples
    # [(range, measure_of_trust 0..1), (), ()]
    def lidar_processing(
            self,
            carrier_item,
            wrapped_measures_list,
            start_angle,
            angle_step):
        estimation_pos = carrier_item.pos()
        estimation_heading = -carrier_item.rotation()
        angle = start_angle
        for wrapped_measure in wrapped_measures_list:
            if wrapped_measure[0] is not None:
                # diameter = 2 * wrapped_measure[1]
                # convert measure to point
                measure_in_global = estimation_pos + QtCore.QPointF(
                    wrapped_measure[0] * math.cos(
                        math.radians(
                            angle + estimation_heading)),
                    - wrapped_measure[0] * math.sin(
                        math.radians(
                            angle + estimation_heading)))
                self.model_sw.show_on_scene(measure_in_global)
            angle += angle_step

    def create_user(self, user, user_scene):
        user_scene.vehicle = None
        if user == User.ARTICULATED_FOUR_WHEELS:
            user_scene.vehicle = articulated.Articulated(
                scene=user_scene,
                frame_length={
                    "back": 50,
                    "front": 30},
                init_pos={
                    "position": QtCore.QPointF(0, 0),
                    "heading": 0},
                wheel_size={
                    "breadth": 5,
                    "diameter": 20})
        elif user == User.FRONT_DRIVING_FOUR_WHEELS:
            user_scene.vehicle = four_wheels.FourWheels(
                user_scene,
                body_size={
                    "width": 100,
                    "height": 50
                },
                init_pos={
                    "position": QtCore.QPointF(0, 0),
                    "heading": -45
                },
                wheel_size={
                    "breadth": 10,
                    "diameter": 30
                })
        elif user == User.TANK:
            user_scene.vehicle = tank.Tank(
                user_scene, QtCore.QPointF(-100, 0), 0, False)
        elif user == User.CART:
            body_size = {
                "x": 100,
                "y": 50
            }
            wheel_size = {
                "breadth": 5,
                "diameter": 20
            }
            init_pos = {
                "position": QtCore.QPointF(0, 0),
                "heading": 0
            }
            user_scene.vehicle = cart.Cart(
                user_scene,
                self.update_freq,
                False,
                body_size=body_size,
                init_pos=init_pos,
                wheel_size=wheel_size)
        return user_scene.vehicle


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('This is a log message.')
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
