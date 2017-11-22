from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import math


# scene show us position of tank at (0, 0) point
class InfoSceneWrapper(QtWidgets.QGraphicsScene):
    lidar_ellipses = []

    def __init__(self, *xxx, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        tank_bound = QtWidgets.QGraphicsRectItem(-10, -10, 20, 20)
        self.addItem(tank_bound)
        x_bound = QtWidgets.QGraphicsRectItem(100, 0, 20, 20)
        y_bound = QtWidgets.QGraphicsRectItem(0, 200, 20, 20)
        self.addItem(x_bound)
        self.addItem(y_bound)
        # add tank rect

    # expect input value - list of tuples
    # [(QPointF, measure_of_trust 0..1), (), ()]
    def show_lidar_info(
            self,
            wrapped_measures_list,
            start_angle,
            angle_step):
        # clean previous dots
        for measure in self.lidar_ellipses:
            self.removeItem(measure)
        self.lidar_ellipses[:] = []
        angle = start_angle
        for wrapped_measure in wrapped_measures_list:
            if wrapped_measure[0] is not None:
                diameter = 50 * wrapped_measure[1]
                new_ellipse = QtWidgets.QGraphicsEllipseItem(
                    wrapped_measure[0] * math.cos(
                        angle * math.pi / 180.0) - diameter,
                    wrapped_measure[0] * math.sin(
                        angle * math.pi / 180.0) - diameter,
                    diameter,
                    diameter)
                new_ellipse.setPen(
                    QtGui.QPen(QtGui.QColor(255, 0, 0, 255)))
                self.lidar_ellipses.append(
                    new_ellipse)
                self.addItem(new_ellipse)
            angle += angle_step
