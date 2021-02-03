import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
import pickle


class Dialog(QWidget):

    def __init__(self, opt, type):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.opt = opt
        self.type = type
        self.initUI()
        self.fileName = None


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        if self.opt == 'save':
            self.saveFileDialog()
        elif self.opt == 'load':
            self.openFileNameDialog()
        else:
            sys.exit('Dialog boss option not expected!')
        # self.openFileNamesDialog()


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDialog = QFileDialog(self)
        fileDialog.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.fileName, _ = fileDialog.getOpenFileName(None, "Open File", "",
                                                  self.type + ";;All Files (*)", options=options)
        if self.fileName:
            with open('temp\\load.pkl', 'wb') as f:
                pickle.dump(self.fileName, f)
                f.close()
                return
        else:
            return

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileDialog = QFileDialog(self)
        fileDialog.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.fileName, _ = fileDialog.getSaveFileName(None, "Save File", "",
                                                  self.type + ";;All Files (*)", options=options)
        if self.fileName:
            with open('temp\\save.pkl', 'wb') as f:
                pickle.dump(self.fileName, f)
                f.close()
                return
        else:
            return


def open_dialog(opt, type):

    Dialog(opt, type)



