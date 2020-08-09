from PyQt5.QtCore import QThread,pyqtSignal
from win32api import GetSystemMetrics
from pynput.mouse import Controller
from EyeTracker import Detection
import time


class CurserThread(QThread):
    def __init__(self, two_d_buttons):
        QThread.__init__(self)
        self.twoDButtons = two_d_buttons
        self.row = 0
        self.colmn = 0

    change_value = pyqtSignal(tuple)

    def run(self):
        while True:
            time.sleep(.5)
            ch = self.twoDButtons[self.row][self.colmn]
            self.colmn += 1
            self.colmn = self.colmn % len(self.twoDButtons[self.row])
            self.change_value.emit((ch, self.twoDButtons[self.row][self.colmn]))




class MouseThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.controller = Controller()
        self.moving_x = 0
        self.moving_y = 25
        self.mxHeight=GetSystemMetrics(1)
        self.mxWidth=GetSystemMetrics(0)

    change_value = pyqtSignal(str)

    def run(self):
        while True:
            time.sleep(.2)
            self.controller.move(self.moving_x,self.moving_y)
            pos=self.controller.position

            if self.moving_y:
                if self.moving_y>0:
                    if pos[1]>=self.mxHeight-1:
                        self.moving_y=-self.moving_y
                else:
                    if pos[1]<=0:
                        self.moving_y=-self.moving_y
            else :
                if self.moving_x > 0:
                    if pos[0] >= self.mxWidth-1:
                        self.moving_x = -self.moving_x
                else:
                    if pos[0] <= 0:
                        self.moving_x = -self.moving_x

            self.change_value.emit("")


class EyeTrackerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.d = Detection()

    change_value = pyqtSignal(str)

    def run(self):
        while True:
            key=self.d.run()
            print(self.d.comand)
            self.change_value.emit(self.d.comand)
            if key==27:
                break