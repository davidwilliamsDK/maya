#Importing Modules
import sys, os, platform

#Set Python Paths
if platform.system() == "Windows":
    sys.path.append("//vfx-data-server/dsGlobal/dsCore/maya")
    sys.path.append("//vfx-data-server/dsGlobal/globalMaya/Resources/lib-dynload")
    sys.path.append("//vfx-data-server/dsGlobal/globalMaya/Resources/PyQt_Win64")
    sys.path.append("//vfx-data-server/dsGlobal/globalMaya/Shotgun")
    sys.path.append("//vfx-data-server/dsGlobal/dsCore/shotgun")

elif platform.system() == "Linux":
    sys.path.append("/dsGlobal/dsCore/maya")
    sys.path.append("/dsGlobal/globalMaya/Resources/lib-dynload")
    sys.path.append("/dsGlobal/globalMaya/Resources/PyQt_Win64")
    sys.path.append("/dsGlobal/globalResources/Shotgun")
    sys.path.append("/dsGlobal/dsCore/shotgun")

#IMPORT CUSTOM PYTHON MODULES
import dsCommon.dsOsUtil as dsOsUtil
reload(dsOsUtil)
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)

#Check For GUI
guiName = "modelLibUI02.ui"
if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsModelLib/%s' % guiName
else:
    sys.path.append('/dsCore/maya/dsCommon/')
    uiFile = 'U:/dsCore/maya/dsModelLib/%s' % guiName

#INSIDE MAYA RUN THIS STUFF!
pyVal = dsOsUtil.getPyGUI()
if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

if pyVal == "PySide":
    from PySide import QtCore,QtGui
    from shiboken import wrapInstance
    form_class, base_class = dsOsUtil.loadUiType(uiFile)

if pyVal == "PyQt":
    from PyQt4 import QtGui, QtCore, uic
    import sip
    form_class, base_class = uic.loadUiType(uiFile)

def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    if pyVal == "PySide":
        return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    else:
        return sip.wrapinstance(long(main_window_ptr), QtCore.QObject)

if dsOsUtil.mayaRunning():
    parent = getMayaWindow()
else:
    parent = None

class MyForm(form_class, base_class):
    def __init__(self, parent=parent):
        #Setup Window
        super(MyForm, self).__init__(parent)
        self.setupUi(self)

##        QtCore.QObject.connect(self.buttonGroup, QtCore.SIGNAL("buttonClicked(int)"), self.listAssets);
        QtCore.QObject.connect(self.D2, QtCore.SIGNAL("clicked(int)"), self.addType);
        QtCore.QObject.connect(self.D2, QtCore.SIGNAL("clicked(int)"), self.addSubType);
        QtCore.QObject.connect(self.D3, QtCore.SIGNAL("clicked(int)"), self.addType);
        QtCore.QObject.connect(self.D3, QtCore.SIGNAL("clicked(int)"), self.addSubType);
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(int)"), self.addSubType);
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(int)"), self.list);
        QtCore.QObject.connect(self.subType, QtCore.SIGNAL("activated(int)"), self.list);
        QtCore.QObject.connect(self.search, QtCore.SIGNAL("returnPressed()"), self.list);
        QtCore.QObject.connect(self.iconSlider, QtCore.SIGNAL("valueChanged(int)"), self.iconUpdate);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.listAssets);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.list);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.enableDisableGUI);
        QtCore.QObject.connect(self.project, QtCore.SIGNAL("activated(int)"), self.listMajors);


        self.libraryPath = projectUtil.libraryPath() + "/asset/"

        self.asset3D = []
        self.asset3Dtype = []
        self.asset3DsubType = []
        self.listed3D = 0

        self.asset2D = []
        self.asset2Dtype = []
        self.asset2DsubType = []
        self.listed2D = 0

        self.mBrick = []
        self.listedmBrick = 0

        self.projects = projectUtil.listProjects()

        self.listProjects()
        self.listAssets()
        self.addType()
        self.addSubType()
        self.list()
        self.iconUpdate()
        self.autoSetting()

    def autoSetting(self):
        if dsOsUtil.mayaRunning() == True:
            path = cmds.file(q=True, location=True)
            if "dsPipe" in path:
                print path

    def listProjects(self):
        if not self.listProjects == []:
            i = 1
            for prj in self.projects:
                self.project.addItem("")
                self.project.setItemText(i, QtGui.QApplication.translate("MainWindow", prj, None, QtGui.QApplication.UnicodeUTF8))
                i = i + 1

    def listMajors(self):
        path = projectUtil.listAssetTypes(str(self.project.currentText()))
        i = 0
        self.major.clear()
        self.major.addItem("")
        self.major.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Major", None, QtGui.QApplication.UnicodeUTF8))
        for asset in dsOsUtil.listFolder(path):
            i = i + 1
            self.major.addItem("")
            self.major.setItemText(i, QtGui.QApplication.translate("MainWindow", asset, None, QtGui.QApplication.UnicodeUTF8))

    def listAssets(self):
        if not self.mbrick.isChecked():
            if self.D3.isChecked():
                base = "3D"
                listed= self.listed3D
                self.listed3D = 1
            else:
                base = "2D"
                listed= self.listed2D
                self.listed2D = 1
        else:
            base = "3D"
            listed= self.listedmBrick
            self.listedmBrick = 1

        assetSubType = []
        assetList = []
        i = 0
        assetType = dsOsUtil.listFolder("%s/%s" % (self.libraryPath, base))

        if not listed == 1:
            for type in assetType:
                subtype = dsOsUtil.listFolder("%s/%s/%s" % (self.libraryPath, base, type))
                if not subtype == []:
                    for sub in subtype:
                        if not self.mbrick.isChecked():
                            if not "mBrick" in sub:
                                #Append sub Type to list of subtypes if it's not allready there.
                                subDict = {"type":type, "sub":sub}
                                assetSubType.append(subDict)

                                path = "%s/%s/%s/%s" % (self.libraryPath, base, type, sub)
                                assets = dsOsUtil.listFolder(path)
                                if not assets == []:
                                    for asset in assets:
                                        #def listAssetIcon(project, assetType, assetSubType, asset):
                                        iconPath = projectUtil.listAssetIcon("Library", type, sub, asset)
                                        dict = {"id":i, "name":asset, "2D/3D":base, "type":type, "subType":sub, "path":path, "iconPath":iconPath}
                                        assetList.append(dict)
                                        i = i + 1
                        else:
                            if "mBrick" in sub:
                                subDict = {"type":type, "sub":sub}
                                assetSubType.append(subDict)

                                path = "%s/%s/%s/%s" % (self.libraryPath, base, type, sub)
                                assets = dsOsUtil.listFolder(path)
                                if not assets == []:
                                    for asset in assets:
                                        #def listAssetIcon(project, assetType, assetSubType, asset):
                                        iconPath = projectUtil.listAssetIcon("Library", type, sub, asset)
                                        dict = {"id":i, "name":asset, "2D/3D":base, "type":type, "subType":sub, "path":path, "iconPath":iconPath}
                                        assetList.append(dict)
                                        i = i + 1

            #Save Settings
            if not self.mbrick.isChecked():
                if base == "3D":
                    self.asset3D = assetList
                    self.asset3Dtype = assetType
                    self.asset3DsubType = assetSubType
                else:
                    self.asset2D = assetList
                    self.asset2Dtype = assetType
                    self.asset2DsubType = assetSubType
            else:
                self.mBrick = assetList

    def addType(self):
        if self.D3.isChecked(): assetTypes = self.asset3Dtype
        else: assetTypes = self.asset2Dtype

        self.type.clear()
        self.type.addItem("")
        i= 0
        self.type.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Type", None, QtGui.QApplication.UnicodeUTF8))

        if not assetTypes == []:
            for assetType in assetTypes:
                i = i+1
                self.type.addItem("")
                self.type.setItemText(i, QtGui.QApplication.translate("MainWindow", assetType, None, QtGui.QApplication.UnicodeUTF8))

    def addSubType(self):
        if self.D3.isChecked(): assetSubTypes = self.asset3DsubType
        else: assetSubTypes = self.asset2DsubType
        typeCombo = self.type.currentText()
        used = []

        self.subType.clear()
        self.subType.addItem("")
        i = 0
        self.subType.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Sub Type", None, QtGui.QApplication.UnicodeUTF8))

        if not assetSubTypes == []:
            for assetSubType in assetSubTypes:
                if typeCombo == "Select Type":
                    if not assetSubType['sub'] in used:
                        i = i+1
                        self.subType.addItem("")
                        self.subType.setItemText(i, QtGui.QApplication.translate("MainWindow", assetSubType['sub'], None, QtGui.QApplication.UnicodeUTF8))
                        used.append(assetSubType['sub'])
                else:
                    if typeCombo == assetSubType['type']:
                        if not assetSubType['sub'] in used:
                            i = i+1
                            self.subType.addItem("")
                            self.subType.setItemText(i, QtGui.QApplication.translate("MainWindow", assetSubType['sub'], None, QtGui.QApplication.UnicodeUTF8))
                            used.append(assetSubType['sub'])

    def list(self):
        if not self.mbrick.isChecked():
            if self.D3.isChecked(): assets = self.asset3D
            else: assets = self.asset2D
        else:
            assets = self.mBrick

        mbrick = self.mbrick.isChecked()
        print mbrick

        #FILTERS
        type = self.type.currentText()
        subType = self.subType.currentText()
        search = self.search.text()
        self.modelList.clear()
        i = 0

        if not assets == []:
            for asset in assets:
                if not self.mbrick.isChecked():
                    if type == "Select Type":
                        if subType == "Select Sub Type":
                            if search == "":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                        elif subType == asset["subType"]:
                            if search == "":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                    elif type == asset["type"]:
                        if subType == "Select Sub Type":
                            if search == "":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                        elif subType == asset["subType"]:
                            if search == "":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                else:
                    if search == "":
                        self.addToList(asset, i)
                        i = i + 1
                    elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                        self.addToList(asset, i)
                        i = i + 1

    def enableDisableGUI(self):
        if self.mbrick.isChecked(): value = False
        else: value = True

        self.type.setEnabled(value)
        self.subType.setEnabled(value)
        self.D2.setEnabled(value)
        self.D3.setEnabled(value)

    def addToList(self, asset, i):
        self.modelList.setResizeMode(QtGui.QListView.Adjust)
        self.modelList.setViewMode(QtGui.QListView.IconMode)
        font = QtGui.QFont()
        font.setPixelSize(15)
        font.PreferAntialias
        font.setWeight(63)

        if os.path.exists(asset["iconPath"]) == True:
            item = QtGui.QListWidgetItem(self.modelList)
            #Add Icon
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(asset["iconPath"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            self.modelList.item(i).setFont(font)
            self.modelList.item(i).setText(QtGui.QApplication.translate("modelLibUI", asset["name"], None, QtGui.QApplication.UnicodeUTF8))

    def iconUpdate(self):
        percentage = float(self.iconSlider.value())
        #Icon Size
        iconSize = [1280,720]
        self.modelList.setIconSize(QtCore.QSize(iconSize[0]*(percentage/100), iconSize[1]*(percentage/100)))

#IF not runned inside Maya
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

#If runned unside Maya
##def UI():
##    global myWindow
##    myWindow = MyForm(getMayaWindow())
##    myWindow.show()

def UI():
    global dsModelLibWindow
    try:
        dsModelLibWindow.close()
    except:
        pass
    dsModelLibWindow = MyForm()
    dsModelLibWindow.show()