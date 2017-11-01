import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from battle_field import scene_wrapper


def main():
    app = QtWidgets.QApplication(sys.argv)
    sw = scene_wrapper.SceneWrapper()
    view = QtWidgets.QGraphicsView(sw)
    view.installEventFilter(sw)
    view.setRenderHints(
        QtGui.QPainter.HighQualityAntialiasing |
        QtGui.QPainter.SmoothPixmapTransform)
    view.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(
        QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Battleground")
    # view.scale(4, 4)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
