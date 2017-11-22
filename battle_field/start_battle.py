import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from battle_field import scene_wrapper
from battle_field import info_scene_wrapper
from PyQt5 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "battle_field.ui"),
            self)
        # information_scene
        isw = info_scene_wrapper.InfoSceneWrapper()
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
        self.info_scene.scale(0.2, 0.2)

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
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
