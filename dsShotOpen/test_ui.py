# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\dsCore\maya\dsShotOpen\test.ui'
#
# Created: Fri Oct 11 10:39:16 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(676, 544)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(60, 80, 470, 130))
        self.widget.setMinimumSize(QtCore.QSize(470, 130))
        self.widget.setMaximumSize(QtCore.QSize(470, 130))
        self.widget.setObjectName("widget")
        self.icon_L = QtGui.QLabel(self.widget)
        self.icon_L.setGeometry(QtCore.QRect(0, 0, 131, 131))
        self.icon_L.setMinimumSize(QtCore.QSize(131, 131))
        self.icon_L.setMaximumSize(QtCore.QSize(131, 131))
        self.icon_L.setAutoFillBackground(True)
        self.icon_L.setText("")
        self.icon_L.setPixmap(QtGui.QPixmap("../../../globalMaya/Icons/mayaico_2014.png"))
        self.icon_L.setScaledContents(False)
        self.icon_L.setObjectName("icon_L")
        self.splitter = QtGui.QSplitter(self.widget)
        self.splitter.setGeometry(QtCore.QRect(150, 50, 341, 26))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.scene_L = QtGui.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.scene_L.setFont(font)
        self.scene_L.setFrameShape(QtGui.QFrame.NoFrame)
        self.scene_L.setFrameShadow(QtGui.QFrame.Plain)
        self.scene_L.setObjectName("scene_L")
        self.date_L = QtGui.QLabel(self.splitter)
        self.date_L.setObjectName("date_L")
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(60, 210, 470, 75))
        self.widget_2.setMinimumSize(QtCore.QSize(470, 75))
        self.widget_2.setMaximumSize(QtCore.QSize(470, 75))
        self.widget_2.setObjectName("widget_2")
        self.icon_L_2 = QtGui.QLabel(self.widget_2)
        self.icon_L_2.setGeometry(QtCore.QRect(0, 0, 75, 75))
        self.icon_L_2.setMinimumSize(QtCore.QSize(75, 75))
        self.icon_L_2.setMaximumSize(QtCore.QSize(75, 75))
        self.icon_L_2.setAutoFillBackground(True)
        self.icon_L_2.setText("")
        self.icon_L_2.setPixmap(QtGui.QPixmap("../../../globalMaya/Icons/mayaico_2014.png"))
        self.icon_L_2.setScaledContents(True)
        self.icon_L_2.setObjectName("icon_L_2")
        self.splitter_2 = QtGui.QSplitter(self.widget_2)
        self.splitter_2.setGeometry(QtCore.QRect(90, 30, 341, 26))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.scene_L_2 = QtGui.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.scene_L_2.setFont(font)
        self.scene_L_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.scene_L_2.setFrameShadow(QtGui.QFrame.Plain)
        self.scene_L_2.setObjectName("scene_L_2")
        self.date_L_2 = QtGui.QLabel(self.splitter_2)
        self.date_L_2.setObjectName("date_L_2")
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setGeometry(QtCore.QRect(60, 290, 470, 50))
        self.widget_3.setMinimumSize(QtCore.QSize(470, 50))
        self.widget_3.setMaximumSize(QtCore.QSize(470, 50))
        self.widget_3.setObjectName("widget_3")
        self.icon_L_3 = QtGui.QLabel(self.widget_3)
        self.icon_L_3.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.icon_L_3.setMaximumSize(QtCore.QSize(50, 50))
        self.icon_L_3.setAutoFillBackground(True)
        self.icon_L_3.setText("")
        self.icon_L_3.setPixmap(QtGui.QPixmap("../../../globalMaya/Icons/mayaico_2014.png"))
        self.icon_L_3.setScaledContents(True)
        self.icon_L_3.setObjectName("icon_L_3")
        self.date_L_3 = QtGui.QLabel(self.widget_3)
        self.date_L_3.setGeometry(QtCore.QRect(60, 25, 341, 16))
        self.date_L_3.setObjectName("date_L_3")
        self.scene_L_3 = QtGui.QLabel(self.widget_3)
        self.scene_L_3.setGeometry(QtCore.QRect(60, 10, 341, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.scene_L_3.setFont(font)
        self.scene_L_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.scene_L_3.setFrameShadow(QtGui.QFrame.Plain)
        self.scene_L_3.setObjectName("scene_L_3")
        self.tw_mayaScene = QtGui.QTableWidget(Form)
        self.tw_mayaScene.setGeometry(QtCore.QRect(60, 350, 475, 610))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.tw_mayaScene.setFont(font)
        self.tw_mayaScene.setAlternatingRowColors(False)
        self.tw_mayaScene.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tw_mayaScene.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tw_mayaScene.setIconSize(QtCore.QSize(50, 50))
        self.tw_mayaScene.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tw_mayaScene.setShowGrid(False)
        self.tw_mayaScene.setGridStyle(QtCore.Qt.NoPen)
        self.tw_mayaScene.setWordWrap(False)
        self.tw_mayaScene.setCornerButtonEnabled(True)
        self.tw_mayaScene.setObjectName("tw_mayaScene")
        self.tw_mayaScene.setColumnCount(1)
        self.tw_mayaScene.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tw_mayaScene.setHorizontalHeaderItem(0, item)
        self.tw_mayaScene.horizontalHeader().setVisible(False)
        self.tw_mayaScene.horizontalHeader().setCascadingSectionResizes(True)
        self.tw_mayaScene.horizontalHeader().setMinimumSectionSize(100)
        self.tw_mayaScene.horizontalHeader().setStretchLastSection(True)
        self.tw_mayaScene.verticalHeader().setVisible(False)
        self.tw_mayaScene.verticalHeader().setCascadingSectionResizes(True)
        self.tw_mayaScene.verticalHeader().setDefaultSectionSize(100)
        self.tw_mayaScene.verticalHeader().setMinimumSectionSize(40)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_L.setText(QtGui.QApplication.translate("Form", "MAYA SCENE.ma", None, QtGui.QApplication.UnicodeUTF8))
        self.date_L.setText(QtGui.QApplication.translate("Form", "last modified: 101013", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_L_2.setText(QtGui.QApplication.translate("Form", "MAYA SCENE.ma", None, QtGui.QApplication.UnicodeUTF8))
        self.date_L_2.setText(QtGui.QApplication.translate("Form", "last modified: 101013", None, QtGui.QApplication.UnicodeUTF8))
        self.date_L_3.setText(QtGui.QApplication.translate("Form", "last modified: 101013", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_L_3.setText(QtGui.QApplication.translate("Form", "MAYA SCENE.ma", None, QtGui.QApplication.UnicodeUTF8))
        self.tw_mayaScene.setSortingEnabled(True)
        self.tw_mayaScene.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "scene", None, QtGui.QApplication.UnicodeUTF8))

