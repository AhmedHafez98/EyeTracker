from Controller import Controller
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys



if __name__=='__main__':
    app = QApplication(sys.argv)
    win = Controller()
    win.show()
    sys.exit(app.exec_())