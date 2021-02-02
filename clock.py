from PyQt5.QtCore import QRectF, QPointF, QObject, pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from threading import Thread
import time
import datetime
import math

class Clock(QObject):
    update_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()
        self.parent = w
        self.rect = w.rect()

        self.inrect = QRectF(self.rect)
        gap = 20
        self.inrect.adjust(gap, gap, -gap, -gap)

        # 중심점
        self.cpt = self.inrect.center()
        self.radius = self.inrect.width()/2

        # 시그널
        self.update_signal.connect(self.parent.update)

        # 쓰레드
        self.t = Thread(target=self.threadFunc)
        self.bRun = True
        self.t.start()

    def getPos(self, deg, radius):
        # 각도 -> 라디안
        rad = deg * math.pi / 180

        dx = math.sin(rad) * radius
        dy = math.cos(rad) * radius
        pt = QPointF(dx + self.cpt.x(), self.cpt.y() - dy)
        
        return pt
    
    def draw(self, qp):
        # 안티앨리어싱
        qp.setRenderHint(QPainter.Antialiasing)

        # 펜
        black = QColor(0,0,0)
        pen0 = QPen(black, 1)
        pen1 = QPen(black, 2)
        pen2 = QPen(black, 5)
        pen3 = QPen(black, 10)
        
        qp.setPen(pen3)
        qp.drawEllipse(self.inrect)

        # 시계 배경
        for i in range(1, 61):
            deg = i * 6
            pt1 = self.getPos(deg, self.radius)
            pt2 = self.getPos(deg, self.radius * 0.9)

            if i % 5 == 0:
                qp.setPen(pen2)

                # 시간 숫자
                f = QFont('arial', 30)
                qp.setFont(f)

                pt3 = self.getPos(deg, self.radius * 0.75)
                size = 50
                rect = QRectF(pt3.x()-size/2, pt3.y()-size/2, size, size)
                #qp.drawRect(rect)

                qp.drawText(rect, Qt.AlignCenter, str(i//5))
            else:
                qp.setPen(pen1)

            qp.drawLine(pt1, pt2)

        # 년, 월, 일
        cpt = QPointF(self.cpt.x() - self.radius/3, self.cpt.y())
        w = 100
        h = 30
        rect = QRectF(cpt.x() - w/2, cpt.y() - h/2, w, h)
        qp.drawRect(rect)

        # 초침
        deg = self.sec * 6
        pt = self.getPos(deg, self.radius * 0.8)
        qp.setPen(pen0)
        qp.drawLine(self.cpt, pt)

        # 분침
        deg = self.min * 6 + (self.sec / 60 * 6)
        pt = self.getPos(deg, self.radius * 0.7)
        qp.setPen(pen1)
        qp.drawLine(self.cpt, pt)

        # 시침
        deg = self.hour * 30 + (self.min / 60 * 30)
        pt = self.getPos(deg, self.radius * 0.6)
        qp.setPen(pen2)
        qp.drawLine(self.cpt, pt)


    def threadFunc(self):
        while self.bRun:
            # 현재 시간
            t = datetime.datetime.now()
            self.year = t.year
            self.mon = t.month
            self.day = t.day
            self.hour = t.hour
            self.min = t.minute
            self.sec = t.second

            self.update_signal.emit()
            time.sleep(0.1)