from PyQt5 import QtWidgets
from PyQt5 import QtGui
from battle_field.items import lidar_model

import os
import battle_field


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
        self.setScale(0.6)
        self.lidar_model = lidar_model.LidarModel(
            timer_update_freq,
            sensor_update_freq,
            scan_sector,
            points_in_sector,
            lidar_maximum_distance,
            parent,
            None)

    def update(self):
        self.lidar_model.update()
