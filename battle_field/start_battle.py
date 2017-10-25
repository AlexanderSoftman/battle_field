from PyQt5.QtWidgets import (QApplication, QGraphicsView)
from PyQt5.QtGui import (QPainter)
import sys

# sys.path.append('./src/')

from battle_field.scene_wrapper import SceneWrapper

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sw = SceneWrapper()
    view = QGraphicsView(sw)
    view.installEventFilter(sw)
    view.setRenderHint(QPainter.Antialiasing)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Battleground")
    # view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
