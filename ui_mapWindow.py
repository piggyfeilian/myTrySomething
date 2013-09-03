# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapWindow.ui'
#
# Created: Tue Sep  3 10:05:43 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapWindow(object):
    def setupUi(self, MapWindow):
        MapWindow.setObjectName(_fromUtf8("MapWindow"))
        MapWindow.resize(800, 600)
        self.symCombo = QtGui.QComboBox(MapWindow)
        self.symCombo.setGeometry(QtCore.QRect(630, 530, 131, 30))
        self.symCombo.setObjectName(_fromUtf8("symCombo"))
        self.symCombo.addItem(_fromUtf8(""))
        self.symCombo.addItem(_fromUtf8(""))
        self.symCombo.addItem(_fromUtf8(""))
        self.symCombo.addItem(_fromUtf8(""))
        self.returnButton = QtGui.QPushButton(MapWindow)
        self.returnButton.setGeometry(QtCore.QRect(630, 570, 131, 30))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))
        self.verticalLayoutWidget = QtGui.QWidget(MapWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 551, 481))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.widget_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.widget_layout.setMargin(0)
        self.widget_layout.setObjectName(_fromUtf8("widget_layout"))
        self.line = QtGui.QFrame(MapWindow)
        self.line.setGeometry(QtCore.QRect(0, 510, 591, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(MapWindow)
        self.line_2.setGeometry(QtCore.QRect(573, 10, 20, 511))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.layoutWidget = QtGui.QWidget(MapWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 540, 471, 29))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newButton = QtGui.QPushButton(self.layoutWidget)
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.horizontalLayout.addWidget(self.newButton)
        self.openButton = QtGui.QPushButton(self.layoutWidget)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout.addWidget(self.openButton)
        self.saveButton = QtGui.QPushButton(self.layoutWidget)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.saveAsButton = QtGui.QPushButton(self.layoutWidget)
        self.saveAsButton.setObjectName(_fromUtf8("saveAsButton"))
        self.horizontalLayout.addWidget(self.saveAsButton)
        self.horizontalLayoutWidget = QtGui.QWidget(MapWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(599, 19, 191, 471))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.listLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.listLayout.setMargin(0)
        self.listLayout.setObjectName(_fromUtf8("listLayout"))
        self.side1 = QtGui.QRadioButton(MapWindow)
        self.side1.setGeometry(QtCore.QRect(590, 500, 90, 20))
        self.side1.setObjectName(_fromUtf8("side1"))
        self.side2 = QtGui.QRadioButton(MapWindow)
        self.side2.setGeometry(QtCore.QRect(690, 500, 90, 20))
        self.side2.setObjectName(_fromUtf8("side2"))
        self.resetButton = QtGui.QPushButton(MapWindow)
        self.resetButton.setGeometry(QtCore.QRect(500, 540, 101, 27))
        self.resetButton.setObjectName(_fromUtf8("resetButton"))

        self.retranslateUi(MapWindow)
        QtCore.QMetaObject.connectSlotsByName(MapWindow)

    def retranslateUi(self, MapWindow):
        MapWindow.setWindowTitle(QtGui.QApplication.translate("MapWindow", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.symCombo.setItemText(0, QtGui.QApplication.translate("MapWindow", "无对称性", None, QtGui.QApplication.UnicodeUTF8))
        self.symCombo.setItemText(1, QtGui.QApplication.translate("MapWindow", "左右对称", None, QtGui.QApplication.UnicodeUTF8))
        self.symCombo.setItemText(2, QtGui.QApplication.translate("MapWindow", "上下对称", None, QtGui.QApplication.UnicodeUTF8))
        self.symCombo.setItemText(3, QtGui.QApplication.translate("MapWindow", "中心对称", None, QtGui.QApplication.UnicodeUTF8))
        self.returnButton.setText(QtGui.QApplication.translate("MapWindow", "返回上级", None, QtGui.QApplication.UnicodeUTF8))
        self.newButton.setText(QtGui.QApplication.translate("MapWindow", "新建", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("MapWindow", "打开", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MapWindow", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsButton.setText(QtGui.QApplication.translate("MapWindow", "另存为", None, QtGui.QApplication.UnicodeUTF8))
        self.side1.setText(QtGui.QApplication.translate("MapWindow", "side1", None, QtGui.QApplication.UnicodeUTF8))
        self.side2.setText(QtGui.QApplication.translate("MapWindow", "side2", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("MapWindow", "重置", None, QtGui.QApplication.UnicodeUTF8))

