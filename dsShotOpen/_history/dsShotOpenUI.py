# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'U:\dsCore\maya\dsShotOpen\dsShotOpenUI.ui'
#
# Created: Fri Jun 28 09:53:08 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(452, 681)
        MainWindow.setMinimumSize(QtCore.QSize(452, 681))
        MainWindow.setMaximumSize(QtCore.QSize(452, 681))
        #MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.user_L = QtGui.QLabel(self.centralwidget)
        self.user_L.setMaximumSize(QtCore.QSize(201, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.user_L.setFont(font)
        self.user_L.setObjectName(_fromUtf8("user_L"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.user_L)
        self.user_CB = QtGui.QComboBox(self.centralwidget)
        self.user_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.user_CB.setObjectName(_fromUtf8("user_CB"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.user_CB)
        self.project_L = QtGui.QLabel(self.centralwidget)
        self.project_L.setMaximumSize(QtCore.QSize(201, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.project_L.setFont(font)
        self.project_L.setObjectName(_fromUtf8("project_L"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.project_L)
        self.projects_CB = QtGui.QComboBox(self.centralwidget)
        self.projects_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.projects_CB.setObjectName(_fromUtf8("projects_CB"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.projects_CB)
        self.episode_L = QtGui.QLabel(self.centralwidget)
        self.episode_L.setMaximumSize(QtCore.QSize(201, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.episode_L.setFont(font)
        self.episode_L.setObjectName(_fromUtf8("episode_L"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.episode_L)
        self.episodes_CB = QtGui.QComboBox(self.centralwidget)
        self.episodes_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.episodes_CB.setObjectName(_fromUtf8("episodes_CB"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.episodes_CB)
        self.seq_L = QtGui.QLabel(self.centralwidget)
        self.seq_L.setMaximumSize(QtCore.QSize(201, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.seq_L.setFont(font)
        self.seq_L.setObjectName(_fromUtf8("seq_L"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.seq_L)
        self.sequence_CB = QtGui.QComboBox(self.centralwidget)
        self.sequence_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.sequence_CB.setObjectName(_fromUtf8("sequence_CB"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.sequence_CB)
        self.seq_L_2 = QtGui.QLabel(self.centralwidget)
        self.seq_L_2.setEnabled(False)
        self.seq_L_2.setMaximumSize(QtCore.QSize(201, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.seq_L_2.setFont(font)
        self.seq_L_2.setObjectName(_fromUtf8("seq_L_2"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.seq_L_2)
        self.shot_CB = QtGui.QComboBox(self.centralwidget)
        self.shot_CB.setEnabled(False)
        self.shot_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.shot_CB.setObjectName(_fromUtf8("shot_CB"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.SpanningRole, self.shot_CB)
        self.task_L = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.task_L.setFont(font)
        self.task_L.setObjectName(_fromUtf8("task_L"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.task_L)
        self.task_CB = QtGui.QComboBox(self.centralwidget)
        self.task_CB.setMinimumSize(QtCore.QSize(150, 0))
        self.task_CB.setObjectName(_fromUtf8("task_CB"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.SpanningRole, self.task_CB)
        spacerItem = QtGui.QSpacerItem(20, 250, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(12, QtGui.QFormLayout.LabelRole, spacerItem)
        self.createPushButton = QtGui.QPushButton(self.centralwidget)
        self.createPushButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createPushButton.sizePolicy().hasHeightForWidth())
        self.createPushButton.setSizePolicy(sizePolicy)
        self.createPushButton.setMinimumSize(QtCore.QSize(201, 31))
        self.createPushButton.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.createPushButton.setFont(font)
        self.createPushButton.setObjectName(_fromUtf8("createPushButton"))
        self.formLayout.setWidget(13, QtGui.QFormLayout.LabelRole, self.createPushButton)
        self.createPushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.createPushButton_2.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createPushButton_2.sizePolicy().hasHeightForWidth())
        self.createPushButton_2.setSizePolicy(sizePolicy)
        self.createPushButton_2.setMinimumSize(QtCore.QSize(201, 31))
        self.createPushButton_2.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.createPushButton_2.setFont(font)
        self.createPushButton_2.setObjectName(_fromUtf8("createPushButton_2"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.LabelRole, self.createPushButton_2)
        self.createPushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.createPushButton_3.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createPushButton_3.sizePolicy().hasHeightForWidth())
        self.createPushButton_3.setSizePolicy(sizePolicy)
        self.createPushButton_3.setMinimumSize(QtCore.QSize(201, 31))
        self.createPushButton_3.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.createPushButton_3.setFont(font)
        self.createPushButton_3.setObjectName(_fromUtf8("createPushButton_3"))
        self.formLayout.setWidget(15, QtGui.QFormLayout.LabelRole, self.createPushButton_3)
        self.createPushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.createPushButton_4.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createPushButton_4.sizePolicy().hasHeightForWidth())
        self.createPushButton_4.setSizePolicy(sizePolicy)
        self.createPushButton_4.setMinimumSize(QtCore.QSize(201, 31))
        self.createPushButton_4.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.createPushButton_4.setFont(font)
        self.createPushButton_4.setObjectName(_fromUtf8("createPushButton_4"))
        self.formLayout.setWidget(16, QtGui.QFormLayout.LabelRole, self.createPushButton_4)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scene_L = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_L.sizePolicy().hasHeightForWidth())
        self.scene_L.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.scene_L.setFont(font)
        self.scene_L.setObjectName(_fromUtf8("scene_L"))
        self.gridLayout_2.addWidget(self.scene_L, 0, 0, 1, 1)
        self.hero_RB = QtGui.QRadioButton(self.centralwidget)
        self.hero_RB.setEnabled(True)
        self.hero_RB.setMinimumSize(QtCore.QSize(55, 17))
        self.hero_RB.setMaximumSize(QtCore.QSize(47, 17))
        self.hero_RB.setChecked(True)
        self.hero_RB.setObjectName(_fromUtf8("hero_RB"))
        self.gridLayout_2.addWidget(self.hero_RB, 0, 1, 1, 1)
        self.version_RB = QtGui.QRadioButton(self.centralwidget)
        self.version_RB.setEnabled(True)
        self.version_RB.setMinimumSize(QtCore.QSize(55, 17))
        self.version_RB.setMaximumSize(QtCore.QSize(47, 17))
        self.version_RB.setChecked(False)
        self.version_RB.setObjectName(_fromUtf8("version_RB"))
        self.gridLayout_2.addWidget(self.version_RB, 0, 2, 1, 1)
        self.scene_LW = QtGui.QListWidget(self.centralwidget)
        self.scene_LW.setMinimumSize(QtCore.QSize(211, 400))
        self.scene_LW.setIconSize(QtCore.QSize(100, 500))
        self.scene_LW.setObjectName(_fromUtf8("scene_LW"))
        self.gridLayout_2.addWidget(self.scene_LW, 1, 0, 1, 4)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.user_L.setText(QtGui.QApplication.translate("MainWindow", "User:", None, QtGui.QApplication.UnicodeUTF8))
        self.project_L.setText(QtGui.QApplication.translate("MainWindow", "Project:", None, QtGui.QApplication.UnicodeUTF8))
        self.episode_L.setText(QtGui.QApplication.translate("MainWindow", "Episode:", None, QtGui.QApplication.UnicodeUTF8))
        self.seq_L.setText(QtGui.QApplication.translate("MainWindow", "Sequence:", None, QtGui.QApplication.UnicodeUTF8))
        self.seq_L_2.setText(QtGui.QApplication.translate("MainWindow", "Shot:", None, QtGui.QApplication.UnicodeUTF8))
        self.task_L.setText(QtGui.QApplication.translate("MainWindow", "Task:", None, QtGui.QApplication.UnicodeUTF8))
        self.createPushButton.setText(QtGui.QApplication.translate("MainWindow", "Create Scene ", None, QtGui.QApplication.UnicodeUTF8))
        self.createPushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Version to Hero", None, QtGui.QApplication.UnicodeUTF8))
        self.createPushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Version Up", None, QtGui.QApplication.UnicodeUTF8))
        self.createPushButton_4.setText(QtGui.QApplication.translate("MainWindow", "Export to New Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_L.setText(QtGui.QApplication.translate("MainWindow", "Scene:", None, QtGui.QApplication.UnicodeUTF8))
        self.hero_RB.setText(QtGui.QApplication.translate("MainWindow", "Hero", None, QtGui.QApplication.UnicodeUTF8))
        self.version_RB.setText(QtGui.QApplication.translate("MainWindow", "Version", None, QtGui.QApplication.UnicodeUTF8))

