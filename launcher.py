import os
import shutil
import sys
import time
import zipfile
import subprocess
import requests
import configparser
config = configparser.ConfigParser()
config.read("launcherconfig.config")
default=config.get("launcher","default-style")
branch=config.get("launcher","default-branch")

def install(pkg):
    subprocess.call(["python3","-m","pip","install",pkg,"--user"])


class colors():
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"


cmdhelp = f""""{colors.RED}
launch                     Launches the game
launch-offline             Launches the game but doesnt download
set-default-style-cmd      sets the default launcher to command line
set-default-style-gui      sets the default launcher to gui
set-default-branch-release sets the default git branch to release
set-default-branch-master  sets the default git branch to master
help                       displays this message {colors.RESET}
"""


def downLoadGame(offline=True):
    if not offline:
        try:
            shutil.rmtree("assets")
            os.remove("PizzaLandGame.py")
        except Exception:
            pass
        dlLink = f"https://github.com/kaansenol5/PizzaLand/archive/{branch}.zip"
        r = requests.get(dlLink)
        with open("game.zip", "wb") as f:
            f.write(r.content)
        zip_ref = zipfile.ZipFile("game.zip", "r")
        zip_ref.extractall("")
        os.remove("game.zip")
        shutil.move(f"PizzaLand-{branch}/assets", "assets")
        shutil.move(f"PizzaLand-{branch}/PizzaLandGame.py", "PizzaLandGame.py")
        os.remove("launcher.py")
        shutil.move(f"PizzaLand-{branch}/launcher.py", "launcher.py")
        time.sleep(1)
    try:
        import pygame
    except ImportError:
        install("pygame")
    os.system("python3 PizzaLandGame.py")

def setdefault(default,thing):
    config.set("launcher", thing, default)
    with open("launcherconfig.config", "w") as f:
        config.write(f)
        
def cmdLauncher():
    print(f"{colors.CYAN}Welcome to the command-line pizzaland launcher!")
    print('If you want to save this option, type "save" to the command line')
    print("To display a list of comments, type help")
    print(f"You are on your own{colors.RESET}")
    cmdline=True
    while cmdline:
        cmd=input()
        if cmd == "launch":
            downLoadGame(False)
        if cmd == "launch-offline":
            downLoadGame(True)
        elif cmd == "set-default-style-gui":
            setdefault("gui","default-style")
        elif cmd == "set-default-style-cmd":
            setdefault("cmd","default-style")
        elif cmd == "set-default-branch-release":
            setdefault("release","default-branch")
        elif cmd == "set-default-branch-master":
            setdefault("master","default-branch")
        elif cmd == "help":
            print(cmdhelp)
        else:
            print(cmdhelp)


def guiLauncher():
    class Ui_Dialog(object):
        def setupUi(self, Dialog):
            Dialog.setObjectName("Dialog")
            Dialog.resize(751, 552)
            self.val = 0
            self.label = QtWidgets.QLabel(Dialog)
            self.label.setGeometry(QtCore.QRect(200, 70, 361, 121))
            self.label.setObjectName("label")
            self.pushButton = QtWidgets.QPushButton(Dialog)
            self.pushButton.setGeometry(QtCore.QRect(220, 370, 301, 81))
            self.pushButton.setObjectName("pushButton")
            self.pushButton.clicked.connect(downLoadGame)
            self.retranslateUi(Dialog)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("PizzaLand", "PizzaLand"))
            self.label.setText(_translate("PizzaLand",
                                          "<html><head/><body><p><span style=\" font-size:26pt; font-weight:600;\">PizzaLand Launcher</span></p></body></html>"))
            self.pushButton.setText(_translate("PizzaLand", "Play"))

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        app.processEvents()
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_Dialog()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


if default == "gui":
    try:
        from PyQt5 import QtCore, QtWidgets
        from PyQt5.QtWidgets import QApplication
        guiLauncher()
    except ImportError:
        print("Failed to import PyQt5")
        print("This can be fix by installing PyQt5.")
        print("Do you want to install PyQt5 y/n")
        print("If you choose no, you can use command line launcher")
        mode=input()
        if mode == "y":
            install("PyQt5")
        else:
            cmdLauncher()

else:
    cmdLauncher()

