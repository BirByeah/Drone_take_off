# Form implementation generated from reading ui file 'd:\MyWorks\Programs\Python\Drone_rasp\UI\initialization.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Initialization_MainWindow(object):
    def setupUi(self, Initialization_MainWindow):
        Initialization_MainWindow.setObjectName("Initialization_MainWindow")
        Initialization_MainWindow.resize(360, 380)
        Initialization_MainWindow.setAutoFillBackground(False)
        Initialization_MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(Initialization_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.waiting_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.waiting_graphicsView.setGeometry(QtCore.QRect(160, 230, 41, 41))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.waiting_graphicsView.setBackgroundBrush(brush)
        self.waiting_graphicsView.setObjectName("waiting_graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 361, 381))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("d:\\MyWorks\\Programs\\Python\\Drone_rasp\\UI\\assets/pictures/初始化背景.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.loading_label_4 = QtWidgets.QLabel(self.centralwidget)
        self.loading_label_4.setGeometry(QtCore.QRect(130, 290, 111, 20))
        self.loading_label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loading_label_4.setObjectName("loading_label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(160, 60, 51, 41))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("d:\\MyWorks\\Programs\\Python\\Drone_rasp\\UI\\assets/pictures/起飞.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 100, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));")
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 170, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        Initialization_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(Initialization_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Initialization_MainWindow)

    def retranslateUi(self, Initialization_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Initialization_MainWindow.setWindowTitle(_translate("Initialization_MainWindow", "MainWindow"))
        self.loading_label_4.setText(_translate("Initialization_MainWindow", "正在配置串口连接..."))
        self.label_2.setText(_translate("Initialization_MainWindow", "起飞！"))
        self.label_3.setText(_translate("Initialization_MainWindow", "专业调试工具"))
