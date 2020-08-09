import sys, time, csv, keyboard, qdarkstyle,pyttsx3
from VirtualKeyboard.GUI import VKDesign, testk
# from GazDetection.GazDetection import GazControl
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtGui

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


class EyeTrackerThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    change_value = pyqtSignal(str)

    def run(self):
        self.change_value.emit(self.test.comand)

class VK(QMainWindow, VKDesign.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        # Attrbuites
        self.button_to_key_dic = {}
        self.button_to_stylesheet_dic = {}
        self.twoDButtons = list()
        self.curserThread = CurserThread(self.twoDButtons)
        self.eyeTrackerThread = EyeTrackerThread()
        self.chosenKey = None
        self.prevKey = None
        self.caps_bool = False
        self.shift_bool = False
        self.ctrl_bool = False
        self.alt_bool = False
        self.state=True
        self.speaker = pyttsx3.init()
        # Methods
        self.initUi()
        self.connectKeys()
        self.startCurserThread()
        self.makeButtons2D()
        # self.startEyeTrackerThread()

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
                self.button_to_stylesheet_dic[row[0]] = a.styleSheet()
                a.clicked.connect(self.buttonClicked)

    def makeButtons2D(self):
        with open('TwoDButtons.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                temp = list()
                for i in row:
                    if i != "":
                        temp.append(i)
                self.twoDButtons.append(temp)

    def buttonClicked(self):  # all buttons events
        sender = self.sender()
        self.textEdit.setFocus()
        c_key = self.button_to_key_dic[sender.objectName()]
        if c_key in ['shift', 'ctrl', 'alt']:
            self.buttonAction(c_key)
        elif self.button_to_key_dic[sender.objectName()]=='suggest':
            keyboard.write(sender.text()+' ')
        elif sender.objectName()=='text_to_speech_b':
            self.textToSpeech()
        elif sender.objectName()=='mouse_b':
            self.mouseController()
        else:
            keyboard.press_and_release(self.button_to_key_dic[sender.objectName()])
            self.boolTrueKey(sender)

        if sender.objectName() == 'caps_lock_b':
            self.caps_bool = not self.caps_bool
            if self.caps_bool:
                sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
            else:
                sender.setStyleSheet(self.button_to_stylesheet_dic[sender.objectName()])
        if self.chosenKey == sender:
            self.chosenKey.setStyleSheet(
                self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")

    def boolTrueKey(self,sender):
        #   Shift Button
        if self.shift_bool and (sender.objectName() not in ['up_b','right_b','down_b','left_b']):
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

    def buttonAction(self, key):
        if key == 'shift':
            self.shift_bool = not self.shift_bool
            if self.shift_bool:
                keyboard.press('shift')
                self.l_shift_b.setStyleSheet(self.l_shift_b.styleSheet() + "background-color : #A364A0")
                self.r_shift_b.setStyleSheet(self.r_shift_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('shift')
                self.l_shift_b.setStyleSheet(self.button_to_stylesheet_dic['l_shift_b'])
                self.r_shift_b.setStyleSheet(self.button_to_stylesheet_dic['r_shift_b'])
        if key == 'ctrl':
            self.ctrl_bool = not self.ctrl_bool
            if self.ctrl_bool:
                keyboard.press('ctrl')
                self.l_ctrl.setStyleSheet(self.l_ctrl.styleSheet() + "background-color : #A364A0")
                self.r_ctrl.setStyleSheet(self.r_ctrl.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('ctrl')
                self.l_ctrl.setStyleSheet(self.button_to_stylesheet_dic['l_ctrl'])
                self.r_ctrl.setStyleSheet(self.button_to_stylesheet_dic['r_ctrl'])
        if key == 'alt':
            self.alt_bool = not self.alt_bool
            if self.alt_bool:
                keyboard.press('alt')
                self.l_alt_b.setStyleSheet(self.l_alt_b.styleSheet() + "background-color : #A364A0")
                self.r_alt_b.setStyleSheet(self.r_alt_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('alt')
                self.l_alt_b.setStyleSheet(self.button_to_stylesheet_dic['l_alt_b'])
                self.r_alt_b.setStyleSheet(self.button_to_stylesheet_dic['r_alt_b'])

    def startCurserThread(self):
        self.curserThread.change_value.connect(self.controlCurserThread)
        self.curserThread.start()

    def controlCurserThread(self, val):
        self.chosenKey = getattr(self, val[1])
        self.prevKey = getattr(self, val[0])
        self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
        self.fixStyleOfLastChosenKey(self.prevKey)
        self.chosenKey.setStyleSheet(
            self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")

    def vkController(self, comand):
        if self.state:
            if comand=='right_blank':               #Go down
                self.curserThread.terminate()
                self.chosenKey.setStyleSheet(self.button_to_stylesheet_dic[self.chosenKey.objectName()])
                self.fixStyleOfLastChosenKey(self.chosenKey)
                self.curserThread.row += 1
                self.curserThread.row %= 7
                self.curserThread.colmn = len(
                    self.twoDButtons[self.curserThread.row]) - 1 if self.curserThread.colmn >= len(
                    self.twoDButtons[self.curserThread.row]) else self.curserThread.colmn
                self.curserThread.start()
            elif comand=='left_blank':  #Stop Curser
                self.state=False
                self.curserThread.terminate()
            elif comand=='blank':   #press ChosenKey
                self.chosenKey.click()
            elif comand=='right':pass
            elif comand=='left':pass
            else :print(f'in vkController this comand unvalid {comand} and state is True')
        else:
            if comand=='right_blank':   #GO Down Step
                self.prevKey = self.chosenKey
                self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
                self.fixStyleOfLastChosenKey(self.prevKey)
                self.curserThread.row += 1
                self.curserThread.row = self.curserThread.row % 7
                # print(len(self.twoDButtons[self.curserThread.row]), self.curserThread.colmn)
                self.curserThread.colmn = len(
                    self.twoDButtons[self.curserThread.row]) - 1 if self.curserThread.colmn >= len(
                    self.twoDButtons[self.curserThread.row]) else self.curserThread.colmn
                self.chosenKey = getattr(self, self.twoDButtons[self.curserThread.row][self.curserThread.colmn])
                self.chosenKey.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")
            elif comand=='left_blank': #continue
                self.state=True
                self.curserThread.start()
            elif comand=='blank':self.chosenKey.click()
            elif comand=='right':   #Go right Step
                self.prevKey = self.chosenKey
                self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
                self.fixStyleOfLastChosenKey(self.prevKey)
                self.curserThread.colmn += 1
                self.curserThread.colmn = self.curserThread.colmn % len(self.twoDButtons[self.curserThread.row])
                self.chosenKey = getattr(self, self.twoDButtons[self.curserThread.row][self.curserThread.colmn])
                self.chosenKey.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")
            elif comand=='left':    # Go Left Step
                self.prevKey = self.chosenKey
                self.prevKey.setStyleSheet(self.button_to_stylesheet_dic[self.prevKey.objectName()])
                self.fixStyleOfLastChosenKey(self.prevKey)
                self.curserThread.colmn -= 1
                self.curserThread.colmn = (self.curserThread.colmn + len(
                    self.twoDButtons[self.curserThread.row])) % len(
                    self.twoDButtons[self.curserThread.row])
                self.chosenKey = getattr(self, self.twoDButtons[self.curserThread.row][self.curserThread.colmn])
                self.chosenKey.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosenKey.objectName()] + "background-color : #1464A0")
            else :print(f'in vkController this comand unvalid {comand} and state is False')

    def fixStyleOfLastChosenKey(self, sender):
        if self.button_to_key_dic[sender.objectName()] == 'caps_lock' and self.caps_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'shift' and self.shift_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'ctrl' and self.ctrl_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'alt' and self.alt_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")

    def startEyeTrackerThread(self):
        self.eyeTrackerThread.change_value.connect(self.controlEyeTrackerThread)
        self.eyeTrackerThread.start()

    def controlEyeTrackerThread(self, val):self.vkController(val)

    def textToSpeech(self):
        selected_text=self.textEdit.textCursor().selection().toPlainText()
        self.speaker.say(selected_text if len(selected_text)>0 else self.textEdit.toPlainText())
        self.speaker.runAndWait()

    def mouseController(self):
        pass


class TestVK(QWidget, testk.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(0, 0, 400, 200)
        self.vk = VK()
        self.vk.show()
        self.setWindowFlags(self.windowFlags() | Qt.WindowDoesNotAcceptFocus)
        self.vk.setFocus()
        self.blank_b.clicked.connect(self.blankClicked)
        self.right_blank_b.clicked.connect(self.rightBlanckstopClicked)
        self.left_blank_b.clicked.connect(self.leftBlanckClicked)
        self.right_b.clicked.connect(self.rightClicked)
        self.left_b.clicked.connect(self.leftClicked)

    def blankClicked(self):
        self.vk.setFocus()
        self.vk.vkController('blank')

    def rightBlanckstopClicked(self):
        self.vk.vkController('right_blank')

    def leftBlanckClicked(self):
        self.vk.vkController('left_blank')

    def rightClicked(self):
        self.vk.vkController('right')

    def leftClicked(self):
        self.vk.vkController('left')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestVK()
    win.show()
    sys.exit(app.exec_())