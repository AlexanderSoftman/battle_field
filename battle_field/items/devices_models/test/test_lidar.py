from battle_field.items.devices_models import lidar
from battle_field.items import obstacle
from PyQt5 import QtWidgets, QtCore
import unittest
import math
import logging
import sys

LOG = logging.getLogger(__name__)


# measure
class LidarTestCase(unittest.TestCase):

    # lidar carrier size
    lc_size = {
        "pos_x": 0,
        "pos_y": 0,
        "x": 50,
        "y": 50
    }
    # lidar half sector angle in degrees
    lidar_half_sector_angle = 60
    lidar_pos = QtCore.QPointF(0, 0)
    dist_lidar_obstacle = 500
    lidar_result = None

    def test_lidar_simple(self):
        # 0. preparation before work
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        main_window.show()
        # 1. create test scene
        scene_rect = QtCore.QRectF(
            -1000, -1000, 2000, 2000)
        # self.info_scene.setScene(isw)
        test_scene = QtWidgets.QGraphicsScene()
        # return
        test_scene.setSceneRect(scene_rect)
        # 2. create test obstacles
        obstacles = [
            obstacle.Obstacle(
                self, QtCore.QPointF(0, 0), 0),
            obstacle.Obstacle(
                self, QtCore.QPointF(0, 0), 0),
            obstacle.Obstacle(
                self, QtCore.QPointF(0, 0), 0)]
        for item in obstacles:
            test_scene.addItem(item)
            item.setVisible(True)
        obstacle_half_x = QtCore.QPointF(
            obstacles[0].boundingRect().width() / 2, 0)
        obstacle_half_x = obstacles[0].mapToScene(obstacle_half_x).x()
        # 3. find obstacles coordinates:
        angles = [
            self.lidar_half_sector_angle,
            0,
            - self.lidar_half_sector_angle]
        for angle, obst in zip(angles, obstacles):
            obst.setPos(
                self.lidar_pos.x() + math.cos(
                    math.radians(angle)) *
                self.dist_lidar_obstacle +
                obstacle_half_x,
                self.lidar_pos.y() + math.sin(
                    math.radians(angle)) *
                self.dist_lidar_obstacle)
        # 3. create test carrier item
        self.lidar_carrier = QtWidgets.QGraphicsRectItem(
            self.lc_size["pos_x"] - self.lc_size["x"] / 2,
            self.lc_size["pos_y"] - self.lc_size["y"] / 2,
            self.lc_size["x"],
            self.lc_size["y"])
        self.lidar_carrier.setScale(0.1)
        test_scene.addItem(self.lidar_carrier)
        # 4. create lidar
        self.lidar = lidar.Lidar(
            self.lidar_carrier,
            1,
            1,
            2 * self.lidar_half_sector_angle,
            self.lidar_callback,
            3,
            800,
            None)
        self.lidar.update()

    def lidar_callback(
        self,
        carrier,
        wrapped_measures_list,
        start_angle,
            angle_step):
        self.assertTrue(
            len(wrapped_measures_list) == 3)
        for measure in wrapped_measures_list:
            LOG.critical(measure)
            self.assertTrue(
                math.fabs(
                    measure[0] - self.dist_lidar_obstacle) <
                0.0001)


if __name__ == '__main__':
    unittest.main()
