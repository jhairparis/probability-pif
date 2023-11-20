from PySide2 import QtCore, QtGui, QtWidgets
from pandas import DataFrame, read_excel
from Screens.components.Select import Select
from lib.PIFSolve import Solve
from modules.MathToQPixmap import MathToQPixmap
from modules.MplCanvas import MplCanvas

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class Ui_Home(object):
    init_table = DataFrame(
        {
            "Wait...": [1, 2, 3, 5, 8, 13, 21],
        }
    )
    data = None

    def setupUi(self, MainWindow, MainWidget):
        from modules.TableModel import TableModel

        self.width = MainWindow.min_size.width()
        self.height = MainWindow.min_size.height() - 63

        font = QtGui.QFont()
        font.setFamily(MainWindow.font_family)
        font.setPointSize(MainWindow.font_size)
        font.setWeight(MainWindow.font_weight)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)

        self.scrollCentral = QtWidgets.QScrollArea(MainWidget)
        self.scrollCentral.setFixedSize(QtCore.QSize(self.width, self.height))

        self.interpolation = QtWidgets.QWidget()
        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))

        self.window = QtWidgets.QFrame(self.interpolation)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        self.initWidget = QtWidgets.QWidget(self.window)

        centerHeight = ((self.height - 63) - 40) / 2

        self.instructions = QtWidgets.QLabel(self.initWidget)
        self.instructions.setEnabled(True)
        self.instructions.setMinimumSize(QtCore.QSize(200, 40))
        self.instructions.setGeometry(
            QtCore.QRect((self.width - 138) / 2, (self.height - 63 - 120) / 2, 200, 10)
        )
        self.instructions.setStyleSheet("")
        self.instructions.setObjectName("instructions")

        self.getFile = QtWidgets.QPushButton(self.initWidget)
        self.getFile.setEnabled(True)
        self.getFile.setMaximumSize(QtCore.QSize(150, 40))
        self.getFile.setGeometry(
            QtCore.QRect((self.width - 150) / 2, centerHeight, 150, 40)
        )
        self.getFile.setFont(font)
        self.getFile.setStyleSheet("")
        self.getFile.setObjectName("getClipboardButton")

        # ---

        self.readyWidget = QtWidgets.QWidget(self.window)
        self.readyWidget.setVisible(False)

        self.labelCity = QtWidgets.QLabel(self.readyWidget)
        self.labelCity.setEnabled(True)
        self.labelCity.setMinimumSize(QtCore.QSize(150, 40))
        self.labelCity.setGeometry(QtCore.QRect(20, 20, 150, 40))
        self.labelCity.setStyleSheet("")
        self.labelCity.setObjectName("labelMethod")

        self.city_box = Select(self.readyWidget)
        self.city_box.setGeometry(QtCore.QRect(20, 60, 250, 40))
        self.city_box.setEnabled(True)
        self.city_box.setToolTip("")
        self.city_box.setStatusTip("")
        self.city_box.setWhatsThis("")
        self.city_box.setAccessibleName("")
        self.city_box.setAccessibleDescription("")
        self.city_box.setStyleSheet("")
        self.city_box.setCurrentText("")
        self.city_box.setMinimumContentsLength(0)
        self.city_box.setObjectName("method_box")

        self.clearButton = QtWidgets.QPushButton(self.readyWidget)
        self.clearButton.setEnabled(True)
        self.clearButton.setMaximumSize(QtCore.QSize(150, 40))
        self.clearButton.setGeometry(QtCore.QRect(self.width - 180, 20, 150, 40))
        self.clearButton.setFont(font)
        self.clearButton.setStyleSheet("")
        self.clearButton.setObjectName("clearButton")

        self.tableWidget = QtWidgets.QTableView(self.readyWidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(20, 120, self.width - 50, 470))
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setStyleSheet("background:red;")

        model = TableModel(self.init_table)
        self.tableWidget.setModel(model)

        self.graph = QtWidgets.QWidget(self.readyWidget)
        self.graph.setGeometry(QtCore.QRect(20, 610, 622, 2000))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_1 = MplCanvas()
        self.graph_2 = MplCanvas()
        self.graph_3 = MplCanvas()
        self.graph_4 = MplCanvas()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_1)
        self.graph_layout.addWidget(self.graph_2)
        self.graph_layout.addWidget(self.graph_3)
        self.graph_layout.addWidget(self.graph_4)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph.setLayout(self.graph_layout)

        self.one = QtWidgets.QWidget(self.readyWidget)
        self.one.setGeometry(QtCore.QRect(650, 620, 300, 400))
        self.oneLayout = QtWidgets.QVBoxLayout()

        self.titleLabel = QtWidgets.QLabel(self.one)
        self.titleLabel.setStyleSheet("")
        self.titleLabel.setObjectName("label")

        self.scrollMath = QtWidgets.QScrollArea(self.one)

        self.Math = QtWidgets.QWidget(self.scrollMath)
        self.Math.setFixedSize(QtCore.QSize(300, 800))

        self.explainWithMath = QtWidgets.QLabel(self.Math)
        self.explainWithMath.setGeometry(QtCore.QRect(0, 0, 300, 800))
        self.explainWithMath.setObjectName("label")

        self.scrollMath.setWidget(self.Math)

        self.oneLayout.addWidget(self.titleLabel)
        self.oneLayout.addWidget(self.scrollMath)
        self.one.setLayout(self.oneLayout)

        self.scrollCentral.setWidget(self.interpolation)

        self.valuesUI()
        self.actionsUI(MainWindow)

    def valuesUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.instructions.setText(_translate("MainWindow", "Seleciona un excel"))

        self.getFile.setText(_translate("MainWindow", "Archivo de excel"))

        self.labelCity.setText(_translate("MainWindow", "Escoge una ciudad:"))

        self.city_box.setCurrentIndex(-1)

        self.clearButton.setText(_translate("MainWindow", "Clear"))

        self.titleLabel.setText(_translate("MainWindow", "Datos"))
        self.explainWithMath.setText("...?")

    prev = ""

    def explain(self, text, text2=""):
        self.prev += str(text) + str(text2) + "\n"
        img = MathToQPixmap(self.prev, fs=12)
        self.Math.setGeometry(QtCore.QRect(0, 0, 300, 800))
        self.explainWithMath.setGeometry(QtCore.QRect(0, 0, 300, 800))
        self.explainWithMath.setPixmap(img)

        return

    def actionsUI(self, MainWindow):
        self.getFile.clicked.connect(lambda: self.openSelectFile(MainWindow))
        self.city_box.currentIndexChanged.connect(self.changeCity)
        self.clearButton.clicked.connect(self.returnInitWidget)

    def changeCity(self, i):
        if i <= 0:
            return

        city = self.city_box.itemText(i)

        self.graph_1.axes.cla()
        self.graph_2.axes.cla()
        self.graph_3.axes.cla()
        self.graph_4.axes.cla()

        Solve(
            self.data,
            int(city),
            [
                self.graph_1.axes,
                self.graph_2.axes,
                self.graph_3.axes,
                self.graph_4.axes,
            ],
            self.explain,
        )

        self.graph_1.draw()
        self.graph_2.draw()
        self.graph_3.draw()
        self.graph_4.draw()
        return

    def openSelectFile(self, MainWindow):
        fname = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Open file")

        self.data = read_excel(fname[0])

        self.showReadyWidget()
        self.initReadyWidget()

    def showReadyWidget(self):
        self.initWidget.setVisible(False)
        self.readyWidget.setVisible(True)

        expand = self.height * 4.6
        self.interpolation.setFixedSize(QtCore.QSize(self.width - 16, expand))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, expand))

    def initReadyWidget(self):
        from modules.TableModel import TableModel

        self.graph_1.axes.cla()

        model = TableModel(self.data)
        self.tableWidget.setModel(model)

        if self.data is not None:
            self.city_box.addItem("Select a city")
            for val in self.data["Cod_Div"].unique():
                self.city_box.addItem(str(val))

        self.titleLabel.setText("Datos")
        self.explainWithMath.setText("...?")

    def returnInitWidget(self):
        from modules.TableModel import TableModel

        self.graph_1.axes.cla()
        self.graph_1.draw()
        self.data = None

        self.readyWidget.setVisible(False)
        self.initWidget.setVisible(True)

        self.city_box.clear()
        self.city_box.setCurrentIndex(-1)

        self.tableWidget.setGeometry(QtCore.QRect(20, 120, self.width - 50, 470))
        self.graph.setGeometry(QtCore.QRect(20, 610, 622, 520))

        self.one.setGeometry(QtCore.QRect(650, 620, 300, 140))

        self.interpolation.setFixedSize(QtCore.QSize(self.width, self.height))
        self.window.setGeometry(QtCore.QRect(0, 0, self.width, self.height))

        model = TableModel(DataFrame(self.init_table))
        self.tableWidget.setModel(model)
