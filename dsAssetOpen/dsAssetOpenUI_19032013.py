from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AssetWindow(object):
    def setupUi(self, AssetWindow):
        AssetWindow.setObjectName(_fromUtf8("AssetWindow"))
        AssetWindow.setEnabled(True)
        AssetWindow.resize(512, 596)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AssetWindow.sizePolicy().hasHeightForWidth())
        AssetWindow.setSizePolicy(sizePolicy)
        AssetWindow.setWindowTitle(_fromUtf8("Asset Dialog"))
        AssetWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(AssetWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.productionLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productionLabel.sizePolicy().hasHeightForWidth())
        self.productionLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.productionLabel.setFont(font)
        self.productionLabel.setObjectName(_fromUtf8("productionLabel"))
        self.gridLayout.addWidget(self.productionLabel, 0, 0, 1, 2)
        self.productionComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productionComboBox.sizePolicy().hasHeightForWidth())
        self.productionComboBox.setSizePolicy(sizePolicy)
        self.productionComboBox.setMaximumSize(QtCore.QSize(201, 22))
        self.productionComboBox.setEditable(False)
        self.productionComboBox.setObjectName(_fromUtf8("productionComboBox"))
        self.gridLayout.addWidget(self.productionComboBox, 1, 0, 1, 3)
        self.assetTypeLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetTypeLabel.sizePolicy().hasHeightForWidth())
        self.assetTypeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.assetTypeLabel.setFont(font)
        self.assetTypeLabel.setObjectName(_fromUtf8("assetTypeLabel"))
        self.gridLayout.addWidget(self.assetTypeLabel, 2, 0, 1, 2)
        self.assetTypeComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetTypeComboBox.sizePolicy().hasHeightForWidth())
        self.assetTypeComboBox.setSizePolicy(sizePolicy)
        self.assetTypeComboBox.setMaximumSize(QtCore.QSize(201, 22))
        self.assetTypeComboBox.setEditable(True)
        self.assetTypeComboBox.setObjectName(_fromUtf8("assetTypeComboBox"))
        self.gridLayout.addWidget(self.assetTypeComboBox, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.assetSubTypeLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetSubTypeLabel.sizePolicy().hasHeightForWidth())
        self.assetSubTypeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.assetSubTypeLabel.setFont(font)
        self.assetSubTypeLabel.setObjectName(_fromUtf8("assetSubTypeLabel"))
        self.gridLayout.addWidget(self.assetSubTypeLabel, 5, 0, 1, 2)
        self.assetSubTypeComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetSubTypeComboBox.sizePolicy().hasHeightForWidth())
        self.assetSubTypeComboBox.setSizePolicy(sizePolicy)
        self.assetSubTypeComboBox.setMinimumSize(QtCore.QSize(201, 22))
        self.assetSubTypeComboBox.setMaximumSize(QtCore.QSize(201, 22))
        self.assetSubTypeComboBox.setEditable(True)
        self.assetSubTypeComboBox.setObjectName(_fromUtf8("assetSubTypeComboBox"))
        self.gridLayout.addWidget(self.assetSubTypeComboBox, 6, 0, 1, 3)

        spacerItem = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)

        self.shogunTemplateLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shogunTemplateLabel.sizePolicy().hasHeightForWidth())
        self.shogunTemplateLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.shogunTemplateLabel.setFont(font)
        self.shogunTemplateLabel.setObjectName(_fromUtf8("shogunTemplateLabel"))
        self.gridLayout.addWidget(self.shogunTemplateLabel, 8, 0, 1, 2)

        self.shotgunTemplateComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shotgunTemplateComboBox.sizePolicy().hasHeightForWidth())
        self.shotgunTemplateComboBox.setSizePolicy(sizePolicy)
        self.shotgunTemplateComboBox.setMinimumSize(QtCore.QSize(201, 22))
        self.shotgunTemplateComboBox.setMaximumSize(QtCore.QSize(201, 22))
        self.shotgunTemplateComboBox.setEditable(False)
        self.shotgunTemplateComboBox.setObjectName(_fromUtf8("shotgunTemplateComboBox"))
        self.gridLayout.addWidget(self.shotgunTemplateComboBox, 10, 0, 1, 3)

        spacerItem1 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 1, 1, 1)
        self.splitterA = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitterA.sizePolicy().hasHeightForWidth())
        self.splitterA.setSizePolicy(sizePolicy)
        self.splitterA.setMinimumSize(QtCore.QSize(201, 16))
        self.splitterA.setMaximumSize(QtCore.QSize(201, 16))
        self.splitterA.setFrameShape(QtGui.QFrame.HLine)
        self.splitterA.setFrameShadow(QtGui.QFrame.Sunken)
        self.splitterA.setObjectName(_fromUtf8("splitterA"))
        self.gridLayout.addWidget(self.splitterA, 11, 0, 2, 3)
        spacerItem2 = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 12, 1, 1, 1)
        self.assetNameLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetNameLabel.sizePolicy().hasHeightForWidth())
        self.assetNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.assetNameLabel.setFont(font)
        self.assetNameLabel.setObjectName(_fromUtf8("assetNameLabel"))
        self.gridLayout.addWidget(self.assetNameLabel, 13, 0, 1, 2)
        self.assetNameTextEdit = QtGui.QLineEdit(self.centralwidget)
        self.assetNameTextEdit.setMaximumSize(QtCore.QSize(201, 22))
        self.assetNameTextEdit.setObjectName(_fromUtf8("assetNameTextEdit"))
        self.gridLayout.addWidget(self.assetNameTextEdit, 14, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 15, 1, 1, 1)
        self.createPushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createPushButton.sizePolicy().hasHeightForWidth())
        self.createPushButton.setSizePolicy(sizePolicy)
        self.createPushButton.setMinimumSize(QtCore.QSize(201, 31))
        self.createPushButton.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.createPushButton.setFont(font)
        self.createPushButton.setObjectName(_fromUtf8("createPushButton"))
        self.gridLayout.addWidget(self.createPushButton, 16, 0, 1, 3)
        self.createMinifigPushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createMinifigPushButton.sizePolicy().hasHeightForWidth())
        self.createMinifigPushButton.setSizePolicy(sizePolicy)
        self.createMinifigPushButton.setMinimumSize(QtCore.QSize(201, 31))
        self.createMinifigPushButton.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.createMinifigPushButton.setFont(font)
        self.createMinifigPushButton.setObjectName(_fromUtf8("createMinifigPushButton"))
        self.gridLayout.addWidget(self.createMinifigPushButton, 17, 0, 1, 3)
        self.splitterB = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitterB.sizePolicy().hasHeightForWidth())
        self.splitterB.setSizePolicy(sizePolicy)
        self.splitterB.setMinimumSize(QtCore.QSize(201, 16))
        self.splitterB.setMaximumSize(QtCore.QSize(201, 16))
        self.splitterB.setFrameShape(QtGui.QFrame.HLine)
        self.splitterB.setFrameShadow(QtGui.QFrame.Sunken)
        self.splitterB.setObjectName(_fromUtf8("splitterB"))
        self.gridLayout.addWidget(self.splitterB, 18, 0, 2, 3)
        self.createIcon = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createIcon.sizePolicy().hasHeightForWidth())
        self.createIcon.setSizePolicy(sizePolicy)
        self.createIcon.setMinimumSize(QtCore.QSize(201, 31))
        self.createIcon.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.createIcon.setFont(font)
        self.createIcon.setObjectName(_fromUtf8("createIcon"))
        self.gridLayout.addWidget(self.createIcon, 19, 0, 1, 2)

        self.exportPart = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportPart.sizePolicy().hasHeightForWidth())
        self.exportPart.setSizePolicy(sizePolicy)
        self.exportPart.setMinimumSize(QtCore.QSize(201, 31))
        self.exportPart.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.exportPart.setFont(font)
        self.exportPart.setObjectName(_fromUtf8("exportPart"))
        self.gridLayout.addWidget(self.exportPart, 20, 0, 1, 2)

        self.incrPushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incrPushButton.sizePolicy().hasHeightForWidth())
        self.incrPushButton.setSizePolicy(sizePolicy)
        self.incrPushButton.setMinimumSize(QtCore.QSize(201, 31))
        self.incrPushButton.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.incrPushButton.setFont(font)
        self.incrPushButton.setObjectName(_fromUtf8("incrPushButton"))
        self.gridLayout.addWidget(self.incrPushButton, 21, 0, 1, 3)

        self.removePushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removePushButton.sizePolicy().hasHeightForWidth())
        self.removePushButton.setSizePolicy(sizePolicy)
        self.removePushButton.setMinimumSize(QtCore.QSize(201, 31))
        self.removePushButton.setMaximumSize(QtCore.QSize(201, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.removePushButton.setFont(font)
        self.removePushButton.setObjectName(_fromUtf8("removePushButton"))
        self.gridLayout.addWidget(self.removePushButton, 22, 0, 1, 3)
        spacerItem4 = QtGui.QSpacerItem(20, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 23, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.loadAssetgridLayout = QtGui.QGridLayout()
        self.loadAssetgridLayout.setObjectName(_fromUtf8("loadAssetgridLayout"))
        self.loadAssetLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadAssetLabel.sizePolicy().hasHeightForWidth())
        self.loadAssetLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.loadAssetLabel.setFont(font)
        self.loadAssetLabel.setObjectName(_fromUtf8("loadAssetLabel"))
        self.loadAssetgridLayout.addWidget(self.loadAssetLabel, 0, 0, 1, 1)
        self.icongridLayout = QtGui.QGridLayout()
        self.icongridLayout.setObjectName(_fromUtf8("icongridLayout"))
        self.iconSizeLabel = QtGui.QLabel(self.centralwidget)
        self.iconSizeLabel.setMinimumSize(QtCore.QSize(44, 17))
        self.iconSizeLabel.setMaximumSize(QtCore.QSize(44, 17))
        self.iconSizeLabel.setObjectName(_fromUtf8("iconSizeLabel"))
        self.icongridLayout.addWidget(self.iconSizeLabel, 0, 0, 1, 1)
        self.iconCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.iconCheckBox.setMinimumSize(QtCore.QSize(25, 17))
        self.iconCheckBox.setMaximumSize(QtCore.QSize(45, 13))
        self.iconCheckBox.setText(_fromUtf8(""))
        self.iconCheckBox.setCheckable(True)
        self.iconCheckBox.setChecked(True)
        self.iconCheckBox.setObjectName(_fromUtf8("iconCheckBox"))
        self.icongridLayout.addWidget(self.iconCheckBox, 0, 1, 1, 1)
        self.iconMediumRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.iconMediumRadioButton.setMinimumSize(QtCore.QSize(80, 17))
        self.iconMediumRadioButton.setMaximumSize(QtCore.QSize(80, 17))
        self.iconMediumRadioButton.setCheckable(True)
        self.iconMediumRadioButton.setObjectName(_fromUtf8("iconMediumRadioButton"))
        self.iconButtonGroup = QtGui.QButtonGroup(AssetWindow)
        self.iconButtonGroup.setObjectName(_fromUtf8("iconButtonGroup"))
        self.iconButtonGroup.addButton(self.iconMediumRadioButton)
        self.icongridLayout.addWidget(self.iconMediumRadioButton, 0, 4, 1, 1)
        self.iconBigRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.iconBigRadioButton.setMinimumSize(QtCore.QSize(44, 17))
        self.iconBigRadioButton.setObjectName(_fromUtf8("iconBigRadioButton"))
        self.iconButtonGroup.addButton(self.iconBigRadioButton)
        self.icongridLayout.addWidget(self.iconBigRadioButton, 0, 5, 1, 1)
        self.iconSmallRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.iconSmallRadioButton.setMinimumSize(QtCore.QSize(55, 17))
        self.iconSmallRadioButton.setMaximumSize(QtCore.QSize(47, 17))
        self.iconSmallRadioButton.setChecked(True)
        self.iconSmallRadioButton.setObjectName(_fromUtf8("iconSmallRadioButton"))
        self.iconButtonGroup.addButton(self.iconSmallRadioButton)
        self.icongridLayout.addWidget(self.iconSmallRadioButton, 0, 2, 1, 1)
        self.loadAssetgridLayout.addLayout(self.icongridLayout, 1, 0, 1, 1)
        self.assetListWidget = QtGui.QListWidget(self.centralwidget)
        self.assetListWidget.setMinimumSize(QtCore.QSize(211, 400))
        self.assetListWidget.setIconSize(QtCore.QSize(100, 500))
        self.assetListWidget.setObjectName(_fromUtf8("assetListWidget"))
        self.loadAssetgridLayout.addWidget(self.assetListWidget, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.loadAssetgridLayout, 0, 1, 1, 1)
        self.dirgridLayout = QtGui.QGridLayout()
        self.dirgridLayout.setObjectName(_fromUtf8("dirgridLayout"))
        self.dirLabel = QtGui.QLabel(self.centralwidget)
        self.dirLabel.setMaximumSize(QtCore.QSize(21, 16))
        self.dirLabel.setObjectName(_fromUtf8("dirLabel"))
        self.dirgridLayout.addWidget(self.dirLabel, 0, 0, 1, 1)
        self.dirPathLabel = QtGui.QLabel(self.centralwidget)
        self.dirPathLabel.setMinimumSize(QtCore.QSize(450, 0))
        self.dirPathLabel.setText(_fromUtf8(""))
        self.dirPathLabel.setScaledContents(True)
        self.dirPathLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dirPathLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.dirPathLabel.setObjectName(_fromUtf8("dirPathLabel"))
        self.dirgridLayout.addWidget(self.dirPathLabel, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.dirgridLayout, 1, 0, 1, 2)
        AssetWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AssetWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 512, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))

        #Shotgunmenu
        self.menuShotgun = QtGui.QMenu(self.menubar)
        self.menuShotgun.setObjectName(_fromUtf8("menuShotgun"))
        AssetWindow.setMenuBar(self.menubar)
        #Updatemenu
        self.menuUpdate = QtGui.QMenu(self.menubar)
        self.menuUpdate.setObjectName(_fromUtf8("menuUpdate"))
        AssetWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(AssetWindow)
        self.statusbar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.statusbar.setFont(font)
        self.statusbar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.statusbar.setToolTip(_fromUtf8(""))
        self.statusbar.setStatusTip(_fromUtf8(""))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AssetWindow.setStatusBar(self.statusbar)
        self.actionHelp_on_AssetDialog = QtGui.QAction(AssetWindow)
        self.actionHelp_on_AssetDialog.setObjectName(_fromUtf8("actionHelp_on_AssetDialog"))
        self.actionAbout = QtGui.QAction(AssetWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExit = QtGui.QAction(AssetWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionReloadTemplates = QtGui.QAction(AssetWindow)
        self.actionReloadTemplates.setObjectName(_fromUtf8("actionReloadTemplates"))

        self.actionImportMinifig = QtGui.QAction(AssetWindow)
        self.actionImportMinifig.setObjectName(_fromUtf8("actionImportMinifig"))

        self.reloadAssetStatus = QtGui.QAction(AssetWindow)
        self.reloadAssetStatus.setObjectName(_fromUtf8("reloadAssetStatus"))
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp_on_AssetDialog)
        self.menuHelp.addAction(self.actionAbout)
        self.menuShotgun.addAction(self.actionReloadTemplates)
        self.menuShotgun.addAction(self.reloadAssetStatus)
        self.menuUpdate.addAction(self.actionImportMinifig)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuShotgun.menuAction())
        self.menubar.addAction(self.menuUpdate.menuAction())

        self.retranslateUi(AssetWindow)
        QtCore.QMetaObject.connectSlotsByName(AssetWindow)

    def retranslateUi(self, AssetWindow):
        self.productionLabel.setText(QtGui.QApplication.translate("AssetWindow", "Production", None, QtGui.QApplication.UnicodeUTF8))
        self.assetTypeLabel.setText(QtGui.QApplication.translate("AssetWindow", "Asset Type", None, QtGui.QApplication.UnicodeUTF8))
        self.assetSubTypeLabel.setText(QtGui.QApplication.translate("AssetWindow", "Asset SubType", None, QtGui.QApplication.UnicodeUTF8))
        self.shogunTemplateLabel.setText(QtGui.QApplication.translate("AssetWindow", "Set Shogun Template", None, QtGui.QApplication.UnicodeUTF8))
        self.assetNameLabel.setText(QtGui.QApplication.translate("AssetWindow", "Asset Name", None, QtGui.QApplication.UnicodeUTF8))
        self.createPushButton.setText(QtGui.QApplication.translate("AssetWindow", "Create Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.createMinifigPushButton.setText(QtGui.QApplication.translate("AssetWindow", "Create Minifig Char", None, QtGui.QApplication.UnicodeUTF8))
        self.createIcon.setText(QtGui.QApplication.translate("AssetWindow", "Create Icon", None, QtGui.QApplication.UnicodeUTF8))

        self.exportPart.setText(QtGui.QApplication.translate("AssetWindow", "Export Part to Asset", None, QtGui.QApplication.UnicodeUTF8))

        self.incrPushButton.setText(QtGui.QApplication.translate("AssetWindow", "Increment Backup", None, QtGui.QApplication.UnicodeUTF8))
        self.removePushButton.setText(QtGui.QApplication.translate("AssetWindow", "Remove Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.loadAssetLabel.setText(QtGui.QApplication.translate("AssetWindow", "Load Asset", None, QtGui.QApplication.UnicodeUTF8))
        self.iconSizeLabel.setText(QtGui.QApplication.translate("AssetWindow", "Icon: ", None, QtGui.QApplication.UnicodeUTF8))
        self.iconMediumRadioButton.setText(QtGui.QApplication.translate("AssetWindow", "Medium", None, QtGui.QApplication.UnicodeUTF8))
        self.iconBigRadioButton.setText(QtGui.QApplication.translate("AssetWindow", "Big", None, QtGui.QApplication.UnicodeUTF8))
        self.iconSmallRadioButton.setText(QtGui.QApplication.translate("AssetWindow", "Small", None, QtGui.QApplication.UnicodeUTF8))
        self.dirLabel.setText(QtGui.QApplication.translate("AssetWindow", "Dir:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("AssetWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("AssetWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuShotgun.setTitle(QtGui.QApplication.translate("AssetWindow", "Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUpdate.setTitle(QtGui.QApplication.translate("AssetWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp_on_AssetDialog.setText(QtGui.QApplication.translate("AssetWindow", "Help on AssetDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("AssetWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("AssetWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReloadTemplates.setText(QtGui.QApplication.translate("AssetWindow", "Reload Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.reloadAssetStatus.setText(QtGui.QApplication.translate("AssetWindow", "Reload Asset Status", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImportMinifig.setText(QtGui.QApplication.translate("AssetWindow", "Import Minfig to Project", None, QtGui.QApplication.UnicodeUTF8))

