import sys, time, csv,keyboard,qdarkstyle
from Testing.GUI import Keytest3 as VKDesign
from VirtualKeyboard.GUI import testk
from PyQt5.QtWidgets import QMainWindow, QApplication,QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class MyThread(QThread):
    # Create a counter thread
    def __init__(self, two_d_buttons):
        QThread.__init__(self)
        self.twoDButtons = two_d_buttons
        self.row=0
        self.colmn=0

    change_value = pyqtSignal(tuple)
    def run(self):
        while True:
            time.sleep(.5)
            ch=self.twoDButtons[self.row][self.colmn]
            self.colmn+=1
            self.colmn= self.colmn % len(self.twoDButtons[self.row])
            self.change_value.emit((ch,self.twoDButtons[self.row][self.colmn]))

class VK(QMainWindow, VKDesign.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        # Attrbuites
        self.button_to_key_dic = {}
        self.button_to_stylesheet_dic={}
        self.twoDButtons=list()
        self.thread = MyThread(self.twoDButtons)
        self.chosenKey=None
        self.prevKey=None
        self.caps_bool=False
        self.shift_bool=False
        self.ctrl_bool=False
        self.alt_bool=False
        # Methods
        self.initUi()
        self.connectKeys()
        self.startActionOnChosenKey()
        self.TwoD()

    def initUi(self):  # modify the UI here
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setupUi(self)
        self.setFixedWidth(802)
        self.setFixedHeight(388)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def connectKeys(self):  # connect each button to event
        with open('MapKeys.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                self.button_to_key_dic[row[0]] = row[1]
                a = getattr(self, row[0])
                self.button_to_stylesheet_dic[row[0]]=a.styleSheet()
                a.clicked.connect(self.buttonClicked)

    def TwoD(self):
        with open('TwoDButtons.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                temp=list()
                for i in row:
                    if i!="":
                        temp.append(i)
                self.twoDButtons.append(temp)

    def buttonClicked(self):  # all buttons events
        sender = self.sender()
        self.textEdit.setFocus()
        c_key=self.button_to_key_dic[sender.objectName()]
        if c_key in ['shift','ctrl','alt']:
            self.buttonAction(c_key)
        else :
            keyboard.press_and_release(self.button_to_key_dic[sender.objectName()])
            self.boolTrueKey()

        if sender.objectName()=='caps_lock_b':
            self.caps_bool=not self.caps_bool
            if self.caps_bool :sender.setStyleSheet(sender.styleSheet()+"background-color : #A364A0")
            else :sender.setStyleSheet(self.button_to_stylesheet_dic[sender.objectName()])
        if self.chosenKey==sender:
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")

    def boolTrueKey(self):
        #   Shift Button
        if self.shift_bool:
            self.shift_bool = False
            keyboard.release('shift')
            self.l_shift_b.setStyleSheet(self.button_to_stylesheet_dic['l_shift_b'])
            self.r_shift_b.setStyleSheet(self.button_to_stylesheet_dic['r_shift_b'])
        #  Ctrl Button
        if self.ctrl_bool:
            self.ctrl_bool = False
            keyboard.release('ctrl')
            self.l_ctrl.setStyleSheet(self.button_to_stylesheet_dic['l_ctrl'])
            self.r_ctrl.setStyleSheet(self.button_to_stylesheet_dic['r_ctrl'])
        #  Alt Button
        if self.alt_bool:
            self.alt_bool = False
            keyboard.release('alt')
            self.l_alt_b.setStyleSheet(self.button_to_stylesheet_dic['l_alt_b'])
            self.r_alt_b.setStyleSheet(self.button_to_stylesheet_dic['r_alt_b'])

    def buttonAction(self,key):
        if key=='shift':
            self.shift_bool = not self.shift_bool
            if self.shift_bool:
                keyboard.press('shift')
                self.l_shift_b.setStyleSheet(self.l_shift_b.styleSheet() + "background-color : #A364A0")
                self.r_shift_b.setStyleSheet(self.r_shift_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('shift')
                self.l_shift_b.setStyleSheet(self.button_to_stylesheet_dic['l_shift_b'])
                self.r_shift_b.setStyleSheet(self.button_to_stylesheet_dic['r_shift_b'])
        if key=='ctrl':
            self.ctrl_bool = not self.ctrl_bool
            if self.ctrl_bool:
                keyboard.press('ctrl')
                self.l_ctrl.setStyleSheet(self.l_ctrl.styleSheet() + "background-color : #A364A0")
                self.r_ctrl.setStyleSheet(self.r_ctrl.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('ctrl')
                self.l_ctrl.setStyleSheet(self.button_to_stylesheet_dic['l_ctrl_b'])
                self.r_ctrl.setStyleSheet(self.button_to_stylesheet_dic['r_ctrl_b'])
        if key=='alt':
            self.alt_bool = not self.alt_bool
            if self.alt_bool:
                keyboard.press('alt')
                self.l_alt_b.setStyleSheet(self.l_alt_b.styleSheet() + "background-color : #A364A0")
                self.r_alt_b.setStyleSheet(self.r_alt_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('ctrl')
                self.l_alt_b.setStyleSheet(self.button_to_stylesheet_dic['l_alt_b'])
                self.r_alt_b.setStyleSheet(self.button_to_stylesheet_dic['r_alt_b'])

    def startActionOnChosenKey(self):
        self.thread.change_value.connect(self.controlChosenKey)
        self.thread.start()

    def controlChosenKey(self, val):
        self.chosenKey = getattr(self, val[1])
        self.prevKey = getattr(self, val[0])
        self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
        self.fixStyleOfLastChosenKey(self.prevKey)
        self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()]+"background-color : #1464A0")

    def vkController(self, state, command):
        if state and command== "down":
            self.thread.terminate()
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()])
            self.fixStyleOfLastChosenKey(self.chosenKey)
            self.thread.row+=1
            self.thread.row%=6
            self.thread.colmn= len(self.twoDButtons[self.thread.row]) - 1 if self.thread.colmn >= len(self.twoDButtons[self.thread.row])else self.thread.colmn
            self.thread.start()
        elif state and command== 'up':
            self.thread.terminate()
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()])
            self.fixStyleOfLastChosenKey(self.chosenKey)
            self.thread.row -= 1
            self.thread.row = (self.thread.row + 6) % 6
            self.thread.colmn = len(self.twoDButtons[self.thread.row]) - 1 if self.thread.colmn >= len(
                self.twoDButtons[self.thread.row]) else self.thread.colmn
            self.thread.start()
        elif not state and command=="right":
            self.prevKey=self.chosenKey
            self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
            self.fixStyleOfLastChosenKey(self.prevKey)
            self.thread.colmn += 1
            self.thread.colmn = self.thread.colmn % len(self.twoDButtons[self.thread.row])
            self.chosenKey=getattr(self,self.twoDButtons[self.thread.row][self.thread.colmn])
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()]+"background-color : #1464A0")
        elif not state and command=="left":
            self.prevKey = self.chosenKey
            self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
            self.fixStyleOfLastChosenKey(self.prevKey)
            self.thread.colmn -= 1
            self.thread.colmn = (self.thread.colmn+len(self.twoDButtons[self.thread.row])) % len(self.twoDButtons[self.thread.row])
            self.chosenKey = getattr(self, self.twoDButtons[self.thread.row][self.thread.colmn])
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()]+"background-color : #1464A0")
        elif not state and command=="up":
            self.prevKey = self.chosenKey
            self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
            self.fixStyleOfLastChosenKey(self.prevKey)
            self.thread.row-=1
            self.thread.row=(self.thread.row+6)%6
            self.thread.colmn = len(self.twoDButtons[self.thread.row]) - 1 if self.thread.colmn >= len(
                self.twoDButtons[self.thread.row]) else self.thread.colmn
            self.chosenKey = getattr(self, self.twoDButtons[self.thread.row][self.thread.colmn])
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()]+"background-color : #1464A0")
        elif not state and command=="down":
            self.prevKey = self.chosenKey
            self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
            self.fixStyleOfLastChosenKey(self.prevKey)
            self.thread.row += 1
            self.thread.row = self.thread.row % 6
            print(len(self.twoDButtons[self.thread.row]),self.thread.colmn)
            self.thread.colmn = len(self.twoDButtons[self.thread.row]) - 1 if self.thread.colmn >= len(
                self.twoDButtons[self.thread.row]) else self.thread.colmn
            self.chosenKey = getattr(self, self.twoDButtons[self.thread.row][self.thread.colmn])
            self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()]+"background-color : #1464A0")
        elif not state and command=="press":self.chosenKey.click()
        elif state:self.thread.start()
        elif not state:self.thread.terminate()

    def fixStyleOfLastChosenKey(self,sender):
        if self.button_to_key_dic[sender.objectName()]=='caps_lock' and self.caps_bool:
            sender.setStyleSheet(sender.styleSheet()+"background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()]=='shift' and self.shift_bool:
            sender.setStyleSheet(sender.styleSheet()+"background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()]=='ctrl' and self.ctrl_bool:
            sender.setStyleSheet(sender.styleSheet()+"background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()]=='alt' and self.alt_bool:
            sender.setStyleSheet(sender.styleSheet()+"background-color : #A364A0")

class testVK(QWidget, testk.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(0,0,400,200)
        self.vk=VK()
        self.vk.show()
        self.vk.setFocus()
        self.run_b.click()
        self.state=1
        self.run_b.toggled['bool'].connect(self.runToggled)
        self.stop_b_2.toggled['bool'].connect(self.stopToggled)
        self.up_b.clicked.connect(self.upClicked)
        self.down_b.clicked.connect(self.downClicked)
        self.right_b.clicked.connect(self.rightClicked)
        self.left_b.clicked.connect(self.leftClicked)
        self.Press_b.clicked.connect(self.pressClicked)
        self.setWindowFlags(self.windowFlags() | Qt.WindowDoesNotAcceptFocus)
    def runToggled(self):
        self.state=1
        self.vk.vkController(1,"")
    def stopToggled(self):
        self.state=0
        self.vk.vkController(0,"")
    def upClicked(self):
        self.vk.vkController(self.state,"up")
    def downClicked(self):
        self.vk.vkController(self.state, "down")
    def rightClicked(self):
        self.vk.vkController(self.state, "right")
    def leftClicked(self):
        self.vk.vkController(self.state, "left")
    def pressClicked(self):
        self.vk.vkController(self.state, "press")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = testVK()
    win.show()
    sys.exit(app.exec_())