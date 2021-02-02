from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter
import sys
from clock import Clock

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)

        self.clock = Clock(self)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.clock.draw(qp)

        qp.end()

    def closeEvent(self, e):
        self.clock.bRun = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())