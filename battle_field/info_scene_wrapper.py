from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import math
import logging

LOG = logging.getLogger(__name__)


# scene show us position of tank at (0, 0) point
class InfoSceneWrapper(QtWidgets.QGraphicsScene):
    lidar_ellipses = []
    sc_start = None

    def __init__(self, *xxx, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        tank_bound = QtWidgets.QGraphicsRectItem(-10, -10, 20, 20)
        self.addItem(tank_bound)
        x_bound = QtWidgets.QGraphicsRectItem(10, 0, 5, 5)
        y_bound = QtWidgets.QGraphicsRectItem(0, 20, 5, 5)
        self.addItem(x_bound)
        self.addItem(y_bound)
        # add tank rect

    # expect input value - list of tuples
    # [(range, measure_of_trust 0..1), (), ()]
    def show_lidar_info(
            self,
            carrier_item,
            wrapped_measures_list,
            start_angle,
            angle_step):
        # clean previous dots
        # for measure in self.lidar_ellipses:
            # self.removeItem(measure)
        # self.lidar_ellipses[:] = []
        # position of carrier item in scene sc
        LOG.debug("===================")
        # LOG.debug("len(wrapped_measures_list): %s" % (
            # len(wrapped_measures_list),))
        # LOG.debug("start_angle: %s, angle_step: %s" % (
            # start_angle, angle_step))
        angle = start_angle
        for wrapped_measure in wrapped_measures_list:
            if wrapped_measure[0] is not None:
                LOG.debug("angle: %s, measure: %s" % (
                    angle, wrapped_measure[0]))
                diameter = 2 * wrapped_measure[1]
                # convert measure to point
                measure_in_carrier_sc = QtCore.QPointF(
                    wrapped_measure[0] * math.cos(
                        angle * math.pi / 180),
                    wrapped_measure[0] * math.sin(
                        angle * math.pi / 180))
                LOG.debug("measure_in_carrier_sc: %s" % (
                    measure_in_carrier_sc,))
                measure_in_global = carrier_item.mapToScene(
                    measure_in_carrier_sc)
                # LOG.debug("measure_in_global: %s" % (
                    # measure_in_global,))
                new_ellipse = QtWidgets.QGraphicsEllipseItem(
                    measure_in_global.x() - diameter,
                    measure_in_global.y() - diameter,
                    diameter,
                    diameter)
                new_ellipse.setPen(
                    QtGui.QPen(QtGui.QColor(255, 0, 0, 255)))
                self.lidar_ellipses.append(
                    new_ellipse)
                self.addItem(new_ellipse)
            angle += angle_step
