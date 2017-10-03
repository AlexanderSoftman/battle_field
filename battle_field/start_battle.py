from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView)
from PyQt5.QtGui import (QPainter)
from PyQt5.QtCore import (qrand, QPointF)

from scene_wrapper import SceneWrapper
from personage import Personage

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    sw = SceneWrapper()
    view = QGraphicsView(sw)
    view.setRenderHint(QPainter.Antialiasing)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Battleground")
    # view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
