from PyQt5 import QtWidgets, QtGui, QtCore
from battle_field.items.devices_models import lidar_model

import os
import battle_field
import logging

LOG = logging.getLogger(__name__)


class Lidar(QtWidgets.QGraphicsPixmapItem):

    lidar_pict = os.path.join(
        os.path.split(
            battle_field.__file__)[0],
        'images/lidar.png')

    def __init__(
        self,
        parent,
        timer_update_freq,
        sensor_update_freq,
        scan_sector,
        points_in_sector,
        lidar_maximum_distance,
            error_model):
        super(Lidar, self).__init__(parent)
        self.setPixmap(
            QtGui.QPixmap(self.lidar_pict))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.1)
        # convert distance fron scene value to carrier dist
        map_dist_point = QtCore.QPointF(
            lidar_maximum_distance,
            0)
        parent_dist_point = parent.mapFromScene(
            map_dist_point)
        self.lidar_model = lidar_model.LidarModel(
            timer_update_freq,
            sensor_update_freq,
            scan_sector,
            points_in_sector,
            parent_dist_point.x(),
            parent,
            None)
        self.parent = parent

    def update(self):
        # LOG.debug("carrier_pos = %s" % (self.parent.pos(),))
        # LOG.debug("carrier_heading = %s" % (-self.parent.rotation(),))
        self.lidar_model.update()
