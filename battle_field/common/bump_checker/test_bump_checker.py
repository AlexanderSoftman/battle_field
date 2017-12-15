from PyQt5 import QtWidgets, QtCore
import unittest
import logging
import math
import sys

from battle_field.common.bump_checker import bump_checker_new


LOG = logging.getLogger(__name__)


# measure
class BumpCheckerNewTestCase(unittest.TestCase):

    rounding_error = 0.001
    bump_checker_new_m = bump_checker_new.BumpCheckerNew()
    small_rect_half_sides = {
        "x": 50,
        "y": 50,
    }
    big_rect_half_sides = {
        "x": 100,
        "y": 100,
    }
    small_rect = QtCore.QRectF(
        - small_rect_half_sides["x"],
        - small_rect_half_sides["y"],
        2 * small_rect_half_sides["x"],
        2 * small_rect_half_sides["y"])
    big_rect = QtCore.QRectF(
        - big_rect_half_sides["x"],
        - big_rect_half_sides["y"],
        2 * big_rect_half_sides["x"],
        2 * big_rect_half_sides["y"])

    # test_bump_checker_N_test - high level testing of functionality
    # angle item come inside angle obstacle
    def test_complex_bump_checker_new_(self):
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        main_window.show()
        test_scene = QtWidgets.QGraphicsScene(
            QtCore.QRectF(
                -1000, -1000, 2000, 2000))
        obstacle = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(obstacle)
        obstacle.setPos(QtCore.QPointF(0, 0))
        item = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(item)
        item.setPos(0, 0)
        rotation_line = QtCore.QLineF(
            QtCore.QPointF(
                self.small_rect_half_sides["x"],
                - self.small_rect_half_sides["y"]),
            QtCore.QPointF(0, 0))
        for item_angle in range(0, 360, 1):
            for offset_x in range(
                (int)(- 3 * self.small_rect_half_sides["x"]),
                (int)(3 * self.small_rect_half_sides["x"]),
                    (int)(0.1 * self.small_rect_half_sides["x"])):
                for offset_y in range(
                    (int)(- 3 * self.small_rect_half_sides["y"]),
                    (int)(3 * self.small_rect_half_sides["y"]),
                        (int)(0.1 * self.small_rect_half_sides["y"])):
                    LOG.critical("item_angle: %s, offset_x: %s, offset_y: %s" % (
                        item_angle, offset_x, offset_y))
                    item.setPos(offset_x, offset_y)
                    LOG.critical("item_pos: %s" % (
                        item.pos()))
                    item.setRotation(
                        item_angle)
                    # preparation finished
                    new_pos = self.bump_checker_new_m.bump_reaction(
                        item)
                    item.setPos(new_pos)
                    # expectation -> item not collide with obstacle
                    colliding_items = item.scene().collidingItems(item)
                    self.assertTrue(len(colliding_items) == 0)

    # find moving vector
    def test_find_edges_normals(self):
        return
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        main_window.show()
        test_scene = QtWidgets.QGraphicsScene(
            QtCore.QRectF(
                -1000, -1000, 2000, 2000))
        item = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(item)
        item.setPos(0, 0)
        obstackle = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(obstackle)
        obstackle.setPos(0, 0)
        obstackle.setRotation(-45)

        # check that degrees offset = 90 degrees)
        normals_inverted = self.bump_checker_new_m.normals_for_edges(
            item, True)
        for normal in normals_inverted:
            self.assertTrue(
                normal.angle() -
                normals_inverted[normals_inverted.index(normal) - 1].angle() <
                90 +
                self.rounding_error)

        # check that we have item.rotation and item rotation +
        # 180 angles in list
        normals_inverted_angles = []
        for normal in normals_inverted:
            normals_inverted_angles.append((int)(normal.angle()))
        self.assertTrue(
            (int)(item.rotation()) in normals_inverted_angles)
        self.assertTrue(
            (int)(item.rotation() + 180) in normals_inverted_angles)

        # check that degrees offset = 90 degrees)
        normals = self.bump_checker_new_m.normals_for_edges(
            obstackle)
        for normal in normals:
            self.assertTrue(
                normal.angle() -
                normals[normals.index(normal) - 1].angle() <
                90 +
                self.rounding_error)

        # check that we have obstacle.rotation and item rotation +
        # 180 angles in list
        normals_angles = []
        for normal in normals:
            normals_angles.append((int)(normal.angle()))
        self.assertTrue(
            (int)(obstackle.rotation() + 360) in normals_angles)
        self.assertTrue(
            (int)(obstackle.rotation() + 180) in normals_angles)

    def test_ejection_vect_for_single_dot(self):
        dot = QtCore.QPointF(0, 0)
        direction = QtCore.QLineF(
            QtCore.QPointF(10, 0),
            QtCore.QPointF(20, 0))
        ejection_vect = self.bump_checker_new_m.ejection_vect_for_single_dot(
            dot,
            direction)
        self.assertTrue(
            math.fabs(
                ejection_vect.x() - 10) <
            self.rounding_error)
        self.assertTrue(
            math.fabs(
                ejection_vect.y()) <
            self.rounding_error)

    def test_filter_normal_by_centers_correllation(self):
        return
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        main_window.show()
        test_scene = QtWidgets.QGraphicsScene(
            QtCore.QRectF(
                -1000, -1000, 2000, 2000))
        obstacle = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(obstacle)
        obstacle.setPos(QtCore.QPointF(0, 0))
        item = QtWidgets.QGraphicsRectItem(
            self.small_rect)
        test_scene.addItem(item)
        item.setPos(100, 100)
        normals = [
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(10, 10)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(- 10, - 10)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(- 5, - 10)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(- 10, - 5)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(100, 0)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(0, 100)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(100, 50)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(50, 100))]
        result_normals = (
            self.bump_checker_new_m.filter_normal_by_centers_correllation(
                normals, item, obstacle))
        expected_normals = [
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(10, 10)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(100, 0)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(0, 100)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(100, 50)),
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(50, 100))]
        self.assertTrue(
            len(expected_normals) == len(result_normals))
        for result_normal in result_normals:
            self.assertTrue(
                result_normal in expected_normals)


if __name__ == '__main__':
    unittest.main()
