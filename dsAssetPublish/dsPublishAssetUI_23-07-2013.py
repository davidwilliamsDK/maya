# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exportAssetUI.ui'
#
# Created: Wed Jan 19 12:23:15 2011
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

#Exporter UI
class Ui_exportAsset(object):
    '''
    '''
    def setupUi(self, exportAssetWindow):
        exportAssetWindow.setObjectName("exportAssetWindow")
        exportAssetWindow.resize(274, 374)
        self.centralwidget = QtGui.QWidget(exportAssetWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.subAssetLabel = QtGui.QLabel(self.centralwidget)
        self.subAssetLabel.setObjectName("subAssetLabel")
        self.gridLayout.addWidget(self.subAssetLabel, 0, 0, 1, 1)
        self.proxyAssetLabel = QtGui.QLabel(self.centralwidget)
        self.proxyAssetLabel.setObjectName("proxyAssetLabel")
        self.gridLayout.addWidget(self.proxyAssetLabel, 0, 1, 1, 1)
        self.subAssetListWidget = QtGui.QListWidget(self.centralwidget)
        self.subAssetListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.subAssetListWidget.setObjectName("subAssetListWidget")
        QtGui.QListWidgetItem(self.subAssetListWidget)
        self.gridLayout.addWidget(self.subAssetListWidget, 1, 0, 1, 1)
        self.proxyListWidget = QtGui.QListWidget(self.centralwidget)
        self.proxyListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.proxyListWidget.setObjectName("proxyListWidget")
        QtGui.QListWidgetItem(self.proxyListWidget)
        self.gridLayout.addWidget(self.proxyListWidget, 1, 1, 1, 1)
        self.updateListsPushButton = QtGui.QPushButton(self.centralwidget)
        self.updateListsPushButton.setObjectName("updateListsPushButton")
        self.gridLayout.addWidget(self.updateListsPushButton, 2, 0, 1, 2)
        self.assetExportPushButton = QtGui.QPushButton(self.centralwidget)
        self.assetExportPushButton.setMinimumSize(QtCore.QSize(251, 31))
        self.assetExportPushButton.setObjectName("assetExportPushButton")
        self.gridLayout.addWidget(self.assetExportPushButton, 3, 0, 1, 2)
        exportAssetWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(exportAssetWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 274, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        exportAssetWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(exportAssetWindow)
        self.statusbar.setObjectName("statusbar")
        exportAssetWindow.setStatusBar(self.statusbar)
        self.actionHelp_on_AssetExport = QtGui.QAction(exportAssetWindow)
        self.actionHelp_on_AssetExport.setObjectName("actionHelp_on_AssetExport")
        self.actionAbout = QtGui.QAction(exportAssetWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtGui.QAction(exportAssetWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp_on_AssetExport)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(exportAssetWindow)
        QtCore.QMetaObject.connectSlotsByName(exportAssetWindow)

    def retranslateUi(self, exportAssetWindow):
        exportAssetWindow.setWindowTitle(QtGui.QApplication.translate("exportAssetWindow", "AssetExportUI", None, QtGui.QApplication.UnicodeUTF8))
        self.subAssetLabel.setText(QtGui.QApplication.translate("exportAssetWindow", "SubAsset List:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyAssetLabel.setText(QtGui.QApplication.translate("exportAssetWindow", "Proxy List:", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.subAssetListWidget.isSortingEnabled()
        self.subAssetListWidget.setSortingEnabled(False)
        __sortingEnabled = self.proxyListWidget.isSortingEnabled()
        self.proxyListWidget.setSortingEnabled(False)
        self.updateListsPushButton.setText(QtGui.QApplication.translate("exportAssetWindow", "Update Lists", None, QtGui.QApplication.UnicodeUTF8))
        self.assetExportPushButton.setText(QtGui.QApplication.translate("exportAssetWindow", "Export Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("exportAssetWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("exportAssetWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("exportAssetWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp_on_AssetExport.setText(QtGui.QApplication.translate("exportAssetWindow", "Help on AssetExport", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("exportAssetWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("exportAssetWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

