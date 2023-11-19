import sys
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Qt, QRect, QCoreApplication, QSize, QMetaObject
from Screens.Home import Ui_Home
from modules.mica.styleSheet import ApplyMenuBlur
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWinExtras import QtWin
from modules.mica.styleSheet import setMicaWindow
from modules.mica.styleSheet import ApplyMenuBlur, setStyleSheet
import matplotlib
from icons import icon_rc

matplotlib.use("Qt5Agg")


class TheWindow(QMainWindow):
    min_size = QSize(980, 650)
    font_family = "Segoe UI Variable Small"
    font_size = 11
    font_weight = 50

    def setupUI(self):
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.ico"))
        self.setObjectName("MainWindow")
        self.setEnabled(True)

        self.resize(self.min_size)
        self.setMinimumSize(self.min_size)

        font = QtGui.QFont()
        font.setFamily(self.font_family)
        font.setPointSize(self.font_size)
        font.setWeight(self.font_weight)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)

        self.setFont(font)

        setStyleSheet(self)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QRect(0, 0, self.min_size.width(), 63))
        self.menuBar.setStyleSheet("")
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setEnabled(True)
        self.menuFile.setObjectName("menuFile")

        self.actionNew = QtWidgets.QMenu(self.menuFile)
        self.actionNew.setEnabled(True)
        self.actionNew.setStyleSheet("")
        self.actionNew.setObjectName("actionNew")

        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")

        self.setMenuBar(self.menuBar)

        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setEnabled(True)
        self.actionSave.setObjectName("actionSave")

        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")

        self.actionPlain_Text_Document = QtWidgets.QAction(self)
        self.actionPlain_Text_Document.setObjectName("actionPlain_Text_Document")
        self.actionRich_Text_Document = QtWidgets.QAction(self)
        self.actionRich_Text_Document.setObjectName("actionRich_Text_Document")

        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")

        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setEnabled(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew.addAction(self.actionPlain_Text_Document)
        self.actionNew.addAction(self.actionRich_Text_Document)

        self.menuFile.addAction(self.actionNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)

        self.menuHelp.addAction(self.actionAbout)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        # ---

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(self.min_size)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setFont(font)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setStyleSheet(
            """
            QTabWidget::pane {
                    border: none;
            }"""
        )

        self.tabHome = QtWidgets.QWidget(self.tabWidget)
        self.tabHome.setStyleSheet("")
        self.tabHome.setObjectName("home")

        self.homeUi = Ui_Home()
        self.homeUi.setupUi(self, self.tabHome)

        self.tabWidget.addTab(self.tabHome, "Home")

        self.setCentralWidget(self.tabWidget)

        self.valuesUI()
        self.actionUI()

    def valuesUI(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "PIF"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setTitle(_translate("MainWindow", "New"))

        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPlain_Text_Document.setText(_translate("MainWindow", "Project"))
        self.actionRich_Text_Document.setText(_translate("MainWindow", "Project File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+I"))

        ApplyMenuBlur(self.menuFile.winId().__int__())
        ApplyMenuBlur(self.actionNew.winId().__int__())
        ApplyMenuBlur(self.menuHelp.winId().__int__())

        QMetaObject.connectSlotsByName(self)

    def actionUI(self):
        self.actionExit.triggered.connect(self.close)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUI()

        setMicaWindow(self)

        self.setAttribute(Qt.WA_TranslucentBackground)
        if QtWin.isCompositionEnabled():
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    centralwidget = TheWindow()
    sys.exit(app.exec_())
