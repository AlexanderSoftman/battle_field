from battle_field.items import obstacle
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import math
import logging
import time

LOG = logging.getLogger(__name__)


# scene show us position of tank at (0, 0) point
class InfoSceneWrapper(QtWidgets.QGraphicsScene):
    # lidar_ellipses = []
    # sc_start = None
    colour = QtGui.QColor(255, 0, 0, 255)
    pen = QtGui.QPen(colour)
    brush = QtGui.QBrush(colour, QtCore.Qt.SolidPattern)
    debug_only_count_of_true_dots = 0
    vehicle = None
    callbacks = None

    # input values:
    # 1) block_side = size of block for creating
    # dict with points (int value)
    # 2) show_block_freq = freq of showed points, Hz
    # f.e. 10 Hz -> show every 10 point, other skipped
    # 3) scene_rect -> QRectF, that will be foundation
    # for scene
    def __init__(
        self,
        block_side,
        show_block_freq,
        scene_rect,
        *xxx,
            **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)

        self.callbacks = {
            "odometer_left":
                self.left_odometer_callback,
            "odometer_right":
                self.right_odometer_callback,
            "lidar":
                self.lidar_callback
        }
        self.setSceneRect(scene_rect)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.show_block_freq = show_block_freq
        self.block_side = block_side
        # tuple of x blocks count and y blocks count
        blocks_count = {
            'x': math.ceil(scene_rect.height() / self.block_side),
            'y': math.ceil(scene_rect.width() / self.block_side)}
        blocks_offset = {
            'x': math.ceil(scene_rect.x() / self.block_side),
            'y': math.ceil(scene_rect.y() / self.block_side)
        }
        LOG.debug("block_count = %s" % (blocks_count,))
        LOG.debug("blocks_offset = %s" % (blocks_offset,))
        # blocks_memory = {('x', 'y') = False or True, ... }
        # ('x', 'y') - top left corner of rect
        self.blocks_memory = dict()
        for x in range(blocks_count['x']):
            for y in range(blocks_count['y']):
                ellipse = QtWidgets.QGraphicsEllipseItem(
                    (x + blocks_offset['x']) * self.block_side,
                    (y + blocks_offset['y']) * self.block_side,
                    self.block_side,
                    self.block_side)
                ellipse.setPen(
                    self.pen)
                ellipse.setBrush(self.brush)
                ellipse.setVisible(False)
                self.addItem(ellipse)
                self.blocks_memory[
                    (x + blocks_offset['x'],
                        y + blocks_offset['y'])] = ellipse
        # debug only
        self.create_field()

    def left_odometer_callback(self, odometer, count_of_strobes):
        self.vehicle.model.left_linear_pu = (
            count_of_strobes * (
                2 * math.pi / odometer.count_of_slots) *
            self.vehicle.model.wheel_rad)

    def right_odometer_callback(self, odometer, count_of_strobes):
        self.vehicle.model.right_linear_pu = (
            count_of_strobes * (
                2 * math.pi / odometer.count_of_slots) *
            self.vehicle.model.wheel_rad)

    def update(self):
        if self.vehicle:
            self.vehicle.update()

    # expect input value - list of tuples
    # [(range, measure_of_trust 0..1), (), ()]
    def lidar_callback(
            self,
            carrier_item,
            wrapped_measures_list,
            start_angle,
            angle_step):
        estimation_pos = self.vehicle.pos()
        LOG.debug("estimation_pos = %s" % (estimation_pos ,))
        estimation_heading = -self.vehicle.rotation()
        LOG.debug("estimation_heading = %s" % (estimation_heading ,))
        angle = start_angle
        for wrapped_measure in wrapped_measures_list:
            if wrapped_measure[0] is not None:
                diameter = 2 * wrapped_measure[1]
                # convert measure to point
                measure_in_global = estimation_pos + QtCore.QPointF(
                    wrapped_measure[0] * math.cos(
                        math.radians(
                            angle + estimation_heading)),
                    - wrapped_measure[0] * math.sin(
                        math.radians(
                            angle + estimation_heading)))
                self.show_on_scene(measure_in_global)
            angle += angle_step

    def show_on_scene(self, point):
        # find nearest block in memory:
        # LOG.debug("point = %s" % (point, ))
        x = math.ceil(point.x() / self.block_side) - 1
        y = math.ceil(point.y() / self.block_side) - 1
        if self.blocks_memory[(x, y)].isVisible() is True:
            return
        else:
            if not (
                x % self.show_block_freq == 0 or
                    y % self.show_block_freq == 0):
                return
            # LOG.debug("set visible")
            self.blocks_memory[(x, y)].setVisible(True)
            self.debug_only_count_of_true_dots += 1

    def create_field(self):
        return
        # simple field
        Obstacle_1 = obstacle.Obstacle(
            self, QtCore.QPointF(500, 0), 0)
        self.addItem(Obstacle_1)
        Obstacle_1.setVisible(True)
        Obstacle_2 = obstacle.Obstacle(
            self, QtCore.QPointF(300, 100), 0)
        Obstacle_3 = obstacle.Obstacle(
            self, QtCore.QPointF(300, -100), 0)
        self.addItem(Obstacle_2)
        self.addItem(Obstacle_3)
        Obstacle_2.setVisible(True)
        Obstacle_3.setVisible(True)

