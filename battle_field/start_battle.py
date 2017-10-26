import sys
from PyQt5.QtWidgets import (QApplication, QGraphicsView)
from PyQt5.QtGui import (QPainter)
from battle_field.scene_wrapper import SceneWrapper


def main():
    app = QApplication(sys.argv)
    sw = SceneWrapper()
    view = QGraphicsView(sw)
    view.installEventFilter(sw)
    view.setRenderHints(
        QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Battleground")
    view.scale(4, 4)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
