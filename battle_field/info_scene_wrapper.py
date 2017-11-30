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
        self.show_block_freq = show_block_freq
        self.block_side = block_side
        # tuple of x blocks count and y blocks count
        blocks_count = {
            'x': math.ceil(scene_rect.height() / block_side),
            'y': math.ceil(scene_rect.width() / block_side)}
        blocks_offset = {
            'x': math.ceil(scene_rect.x() / block_side),
            'y': math.ceil(scene_rect.y() / block_side)
        }
        # blocks_memory = {('x', 'y') = False or True, ... }
        # ('x', 'y') - top left corner of rect
        self.blocks_memory = dict()
        for x in range(blocks_count['x']):
            for y in range(blocks_count['y']):
                ellipse = QtWidgets.QGraphicsEllipseItem(
                    x + blocks_offset['x'],
                    y + blocks_offset['y'],
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
        self.setSceneRect(scene_rect)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        tank_bound = QtWidgets.QGraphicsRectItem(-10, -10, 20, 20)
        self.addItem(tank_bound)
        # debug only
        x_bound = QtWidgets.QGraphicsRectItem(10, 0, 5, 5)
        y_bound = QtWidgets.QGraphicsRectItem(0, 20, 5, 5)
        self.addItem(x_bound)
        self.addItem(y_bound)

    # expect input value - list of tuples
    # [(range, measure_of_trust 0..1), (), ()]
    def show_lidar_info(
            self,
            carrier_item,
            wrapped_measures_list,
            start_angle,
            angle_step):
        start_time = time.time()
        # clean previous dots
        # for measure in self.lidar_ellipses:
            # self.removeItem(measure)
        # self.lidar_ellipses[:] = []
        # position of carrier item in scene sc
        # LOG.debug("dots = %s" % (self.debug_only_count_of_true_dots,))
        # LOG.debug("len(wrapped_measures_list): %s" % (
            # len(wrapped_measures_list),))
        # LOG.debug("start_angle: %s, angle_step: %s" % (
            # start_angle, angle_step))
        angle = start_angle
        for wrapped_measure in wrapped_measures_list:
            if wrapped_measure[0] is not None:
                #LOG.debug("angle: %s, measure: %s" % (
                    #angle, wrapped_measure[0]))
                diameter = 2 * wrapped_measure[1]
                # convert measure to point
                measure_in_carrier_sc = QtCore.QPointF(
                    wrapped_measure[0] * math.cos(
                        angle * math.pi / 180),
                    wrapped_measure[0] * math.sin(
                        angle * math.pi / 180))
                # LOG.debug("measure_in_carrier_sc: %s" % (
                    # measure_in_carrier_sc,))
                measure_in_global = carrier_item.mapToScene(
                    measure_in_carrier_sc)
                # LOG.debug("measure_in_global: %s" % (
                    # measure_in_global,))
                self.show_on_scene(measure_in_global)
            angle += angle_step
        elapsed_time = time.time() - start_time
        # LOG.debug("time for showing on scene: %s" % (
            # elapsed_time,))

    def show_on_scene(self, point):
        # find nearest block in memory:
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

