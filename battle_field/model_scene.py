from battle_field.items import obstacle
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import math
import logging
import time

LOG = logging.getLogger(__name__)


# scene show us position of tank at (0, 0) point
class ModelScene(QtWidgets.QGraphicsScene):
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
        scene_rect,
        immovables_pos,
        *xxx,
            **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(scene_rect)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        # for immovable_pos in immovables_pos:
        #     self.addItem(obstacle.Obstacle(
        #         self, immovable_pos, 0))

        self.show_block_freq = 3
        self.block_side = 3
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

    def update(self):
        if self.vehicle:
            self.vehicle.update()
