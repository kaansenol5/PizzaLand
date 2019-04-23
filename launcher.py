from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget
import sys
import requests
import zipfile
import os
import time
import shutil


try:
    shutil.rmtree("assets")
    os.remove("PizzaLandGame.py")
except Exception:
    pass

dlLink="https://github.com/kaansenol5/PizzaLand/archive/master.zip"
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(751, 552)
        self.val=0
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 70, 361, 121))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 370, 301, 81))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(240, 320, 251, 23))
        self.progressBar.setProperty("value", self.val)
        self.progressBar.setObjectName("progressBar")
        self.pushButton.clicked.connect(self.downLoadGame)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("PizzaLand", "PizzaLand"))
        self.label.setText(_translate("PizzaLand", "<html><head/><body><p><span style=\" font-size:26pt; font-weight:600;\">PizzaLand Launcher</span></p></body></html>"))
        self.pushButton.setText(_translate("PizzaLand", "Play"))

    def downLoadGame(self):
        print("aaaaaaaa")
        self.val=25
        self.progressBar.setProperty("value", self.val)
        r = requests.get(dlLink)
        self.val=30
        self.progressBar.setProperty("value", self.val)
        with open("game.zip","wb") as f:
            f.write(r.content)
            self.val=50
            self.progressBar.setProperty("value", self.val)
        zip_ref= zipfile.ZipFile("game.zip","r")
        zip_ref.extractall("")
        os.remove("game.zip")
        shutil.move("PizzaLand-master/assets","assets")
        shutil.move("PizzaLand-master/PizzaLandGame.py","PizzaLandGame.py")
        self.val=100
        self.progressBar.setProperty("value", self.val)
        time.sleep(1)
        os.system("python3 PizzaLandGame.py")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.processEvents()
    MainWindow= QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
