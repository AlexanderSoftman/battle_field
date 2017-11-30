import sys
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from battle_field import scene_wrapper
from battle_field import info_scene_wrapper
from PyQt5 import uic


LOG = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "battle_field.ui"),
            self)
        # information_scene
        isw = info_scene_wrapper.InfoSceneWrapper(
            block_side=3,
            show_block_freq=3,
            scene_rect=QtCore.QRectF(
                -1000,
                -1000,
                2000,
                2000))
        self.info_scene.setScene(isw)
        self.info_scene.installEventFilter(isw)
        self.info_scene.setRenderHints(
            QtGui.QPainter.HighQualityAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.info_scene.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.info_scene.setViewportUpdateMode(
            QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.info_scene.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.info_scene.setWindowTitle("Information")
        self.info_scene.scale(4, 4)

        sw = scene_wrapper.SceneWrapper(isw)
        self.main_scene.setScene(sw)
        self.main_scene.installEventFilter(sw)
        self.main_scene.setRenderHints(
            QtGui.QPainter.HighQualityAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.main_scene.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.main_scene.setViewportUpdateMode(
            QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.main_scene.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.main_scene.setWindowTitle("Battleground")
        # self.main_scene.scale(4, 4)


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
