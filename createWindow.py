from PyQt5.QtCore import (QAbstractTransition, QEasingCurve, QEvent, QParallelAnimationGroup,
        QPropertyAnimation, qrand, QRect, QSequentialAnimationGroup, qsrand, QState, QStateMachine,
        Qt, QTime, QTimer)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, QGraphicsWidget)


class QGraphicsRectWidget(QGraphicsWidget):
    def paint(self, painter, option, widget):
        painter.fillRect(self.rect(), Qt.blue)

def main():
    import sys
    app = QApplication(sys.argv)
    
    button1 = QGraphicsRectWidget()
    button2 = QGraphicsRectWidget()
    button2.setZValue(1)

    scene = QGraphicsScene(50, 50, 1000, 1000)
    scene.setBackgroundBrush(Qt.black)
    scene.addItem(button1)
    scene.addItem(button2)

    window = QGraphicsView(scene)
    window.setFrameStyle(0)
    window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    #machine = QStateMachine()


    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
