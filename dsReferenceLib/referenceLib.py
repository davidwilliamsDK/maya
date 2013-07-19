#Import python modules
import sys, os, re, shutil, random, sip
from PyQt4 import QtCore, QtGui

#Import GUI
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Custom import modules
from referenceLibUI import Ui_ReferenceWindow

import dsCommon.dsOsUtil as dsOsUtil
reload(dsOsUtil)

import dsCommon.dsProjectUtil as dsProjectUtil
reload(dsProjectUtil)

import dsCommon.dsReferenceCMD as refCMD
reload(refCMD)

#Check if this is runned inside maya
if dsOsUtil.mayaRunning():
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

#If inside Maya open Maya GUI
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

#ReferenceLib Class
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ReferenceWindow()
        self.ui.setupUi(self)

        #Init definitions to lidt projects
        MyForm.updateProjectComboBox(self)

        #If the button have been clicked, run the def
        QtCore.QObject.connect(self.ui.projectComboBox, QtCore.SIGNAL("activated(int)"), self.updateAssetTypeComboBox);
        QtCore.QObject.connect(self.ui.assetTypeComboBox, QtCore.SIGNAL("activated(int)"), self.updateAssetSubTypeComboBox);
        QtCore.QObject.connect(self.ui.assetSubTypeComboBox, QtCore.SIGNAL("activated(int)"), self.updateAssetsGridLayout);
        QtCore.QObject.connect(self.ui.iconSizeButtonGroup, QtCore.SIGNAL("buttonClicked(int)"), self.updateIconSize);

        QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.updateAssetProxyState);
        QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.createRef);

        QtCore.QObject.connect(self.ui.actionExit, QtCore.SIGNAL("activated(int)"), self.exitWidget)


        QtCore.QObject.connect(self.ui.actionExit, QtCore.SIGNAL("activated(int)"), self.closeEvent);

        #Gui Settings
        self.settings = QtCore.QSettings("Duckling&Sonne", "dsReferenceLib")
        self.iconSizeState = "small"
        self.projectState= ""
        self.assetTypeState = ""
        self.assetSubTypeState = ""

        self.readSettings()

        #Init definitions to update UI
        MyForm.updateIconSize(self)

        #Greetings
        self.ui.statusbar.showMessage('Welcome to the refference library');

        self.ui.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.ui.listWidget.customContextMenuRequested.connect(self.openMenu);

    def openMenu(self, position):
        menu = QMenu()

        #Add Proxy Types to Context menu
        project = self.ui.projectComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()
        asset = self.ui.listWidget.currentItem().text()

        path = dsProjectUtil.listAssetRefPath(project, assetType, assetSubType, asset)

        refs=[]

        for item in sorted(os.listdir(path)):
            refs = item.split(".")
            if len(refs) == 2:
                if refs[1] == "mb" or refs[1] == "ma":
                    entry = menu.addAction(item)
                    self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.createRef(item=item))
                    menu.addAction(entry)

        updataProxyAction = menu.addAction("Update Selected Proxies")
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.ui.listWidget.mapToGlobal(position))
        if action == updataProxyAction:
            self.updateProxies(project, assetType, assetSubType, asset)
        if action == quitAction:
            self.exitWidget()

    def updateProxies(self, project, assetType, assetSubType, asset):
        curProx = refCMD.listCurrentProxy()
        proxyUpdate = False

        #IF REPLACE WITH A NEW ASSET - MEANING NOT ONLY A PROXY UPDATE
        if not str(curProx.split("RN", 1)[0]) == str(asset):
            #Retreving both new and old ref path
            sel = cmds.ls(sl=True, hd=1)
            curRefFile = cmds.referenceQuery(sel ,filename=True )
            curRefPath = curRefFile.rsplit("/",1)[0]+"/"
            newRefPath = dsProjectUtil.listAssetRefPath(project, assetType, assetSubType, asset)

            #Comparing paths to make sure, they are not the same
            if not str(curRefPath) == str(newRefPath):
                refList = os.listdir(newRefPath)
                curProxy = curRefFile.rsplit("_",1)[1]

                #Find the same proxy type for new Asset
                for ref in refList:
                    if curProxy in ref:
                        filetype = "mayaBinary"
                        referenceFilePath = "%s%s" % (newRefPath, ref)
                        loadref = "%s" % curProx

                        #Replace reference.
                        cmds.file(referenceFilePath, loadReference=loadref, type=filetype, options="v=0")
                        proxyUpdate = True

        if str(curProx.split("RN", 1)[0]) == str(asset):
            proxyUpdate = True

        if proxyUpdate:
            refCMD.removeNonActiveProxies(sel)
            refCMD.addProxies(sel)

    def updateProjectComboBox(self):
        '''This Def list all project in the project dir, with a config.xml file in the root'''
        self.ui.projectComboBox.clear()
        projects = dsProjectUtil.listProjects()
        i = 0
        if projects:
            for project in projects:
                self.ui.projectComboBox.addItem("")
                self.ui.projectComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", project, None, QtGui.QApplication.UnicodeUTF8))
                i = i+1
                ##if not project == "Library":
                ##    self.ui.projectComboBox.addItem("")
                ##    self.ui.projectComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", project, None, QtGui.QApplication.UnicodeUTF8))
                ##    i = i+1
		
        MyForm.updateAssetTypeComboBox(self)

    def updateAssetTypeComboBox(self):
        '''Lists all Asset Types for a given project'''
        self.ui.assetTypeComboBox.clear()
        project = self.ui.projectComboBox.currentText()
        path = dsProjectUtil.listAssetTypes(project)

        assetTypes = dsOsUtil.listFolder(str(path))
        i=0
        for assetType in assetTypes:
            self.ui.assetTypeComboBox.addItem("")
            self.ui.assetTypeComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", assetType, None, QtGui.QApplication.UnicodeUTF8))
            i = i+1
        MyForm.updateAssetSubTypeComboBox(self)

    def updateAssetSubTypeComboBox(self):
        '''Lists all Sub Asset Types for a given Asset Type'''
        self.ui.assetSubTypeComboBox.clear()
        project = self.ui.projectComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        path = dsProjectUtil.listSubAssets(project, assetType)

        assetSubTypes = dsOsUtil.listFolder(str(path))
        i=0
        for assetSubType in assetSubTypes:
            self.ui.assetSubTypeComboBox.addItem("")
            self.ui.assetSubTypeComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", assetSubType, None, QtGui.QApplication.UnicodeUTF8))
            i = i+1
        MyForm.updateAssetsGridLayout(self)

    def updateAssetsGridLayout(self):
        ''''''
        self.ui.listWidget.clear()
        project = self.ui.projectComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()

        path = dsProjectUtil.listAssets(project, assetType, assetSubType)
        assets = dsOsUtil.listFolder(str(path))

        i=0
        for asset in assets:
            picPath = dsProjectUtil.listAssetIcon(project, assetType, assetSubType, asset)
            MyForm.addToListWidget(self, picPath, asset, i)
            i=i+1

    def updateAssetProxyState(self):
        self.ui.proxyStateComboBox.clear()

        project = self.ui.projectComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()
        asset = self.ui.listWidget.currentItem().text()

        proxyTypes = []
        subAssets = []

        i=0
        ma = 0
        mb = 0

        path = dsProjectUtil.listAssetRefPath(project, assetType, assetSubType, asset)
        dir = os.listdir(path)

        for item in dir:
            if item.endswith("ma"):
                ma = ma + 1
            if item.endswith("mb"):
                mb = mb + 1

        if ma > mb:
            ext = "ma"
        else:
            ext = "mb"

        for item in dir:
            if item.endswith(ext):
                noExt = item.rsplit(".")[0]

                proxy = noExt.rsplit("_")[-1]
                if not proxy in proxyTypes:
                    proxyTypes.append(proxy)

                subAsset = noExt.rsplit("_", 1)[0]
                if not subAsset in subAssets:
                    subAssets.append(subAsset)

        for proxy in proxyTypes:
            self.ui.proxyStateComboBox.addItem("")
            self.ui.proxyStateComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", proxy, None, QtGui.QApplication.UnicodeUTF8))
            i=i+1

    def addToListWidget(self, picPath, assetName, i):
        ''''''
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(picPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item = QtGui.QListWidgetItem(self.ui.listWidget)
        item.setIcon(icon1)
        self.ui.listWidget.item(i).setText(QtGui.QApplication.translate("MainWindow", assetName, None, QtGui.QApplication.UnicodeUTF8))

    def updateIconSize(self):
        iconSize = [80, 80]
        if self.ui.iconMediumRadioButton.isChecked():
            iconSize = [120, 120]
        if self.ui.iconBigRadioButton.isChecked():
            iconSize = [200, 200]

        self.ui.listWidget.setIconSize(QtCore.QSize(iconSize[0], iconSize[1]))
        self.ui.listWidget.setGridSize(QtCore.QSize(iconSize[0], iconSize[1]))

    def closeEvent(self, event):
        MyForm.writeSettings(self)
        event.accept()

    def writeSettings(self):
        '''Write application settings'''
        settings = self.settings

        #Write icon Size
        settings.setValue("iconSizeState", self.ui.iconSizeButtonGroup.checkedButton().text())

        #Write Asset Menu state
        settings.setValue("projectState", self.ui.projectComboBox.currentText())
        settings.setValue("assetTypeState", self.ui.assetTypeComboBox.currentText())
        settings.setValue("assetSubTypeState", self.ui.assetSubTypeComboBox.currentText())

    def readSettings(self):
        '''Read settings Gui Settings.'''
        settings = self.settings

        #Set Icon Size
        self.iconSizeState = settings.value("iconSizeState").toString()
        buttons = self.ui.iconSizeButtonGroup.buttons()
        for button in buttons:
            if button.text() == self.iconSizeState:
                button.setChecked(True)

        self.projectState = settings.value("projectState").toString()
        if not self.ui.projectComboBox.findText(self.projectState) == -1:
            self.ui.projectComboBox.setCurrentIndex(self.ui.projectComboBox.findText(self.projectState))
            MyForm.updateAssetTypeComboBox(self)

        self.assetTypeState = settings.value("assetTypeState").toString()
        if not self.ui.assetTypeComboBox.findText(self.assetTypeState) == -1:
            self.ui.assetTypeComboBox.setCurrentIndex(self.ui.assetTypeComboBox.findText(self.assetTypeState))

        MyForm.updateAssetSubTypeComboBox(self)

        self.assetSubTypeState = settings.value("assetSubTypeState").toString()
        if not self.ui.assetSubTypeComboBox.findText(self.assetSubTypeState) == -1:
            self.ui.assetSubTypeComboBox.setCurrentIndex(self.ui.assetSubTypeComboBox.findText(self.assetSubTypeState))

        MyForm.updateAssetsGridLayout(self)

    def createRef(self, item=None, sharedEdits=True):
        '''Create Ref'''
        project = self.ui.projectComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()
        asset = self.ui.listWidget.currentItem().text()

        if isinstance(item, str):
            if "_" in item:
                proxyState = item.split("_")[-1].split(".")[0]
        if not isinstance(item, str):
            proxyState=str(self.ui.proxyStateComboBox.currentText())

        #Find extension
        ma = 0
        mb = 0

        path = dsProjectUtil.listAssetRefPath(project, assetType, assetSubType, asset)
        dir = os.listdir(path)

        for item in dir:
            if item.endswith("ma"):
                ma = ma + 1
            if item.endswith("mb"):
                mb = mb + 1

        if ma > mb:
            ext = "ma"
        else:
            ext = "mb"

        #set shared edits on/off
        if sharedEdits:
            if int(cmds.optionVar(q="proxyOptionsSharedEdits")) is 0:
                cmds.optionVar(sv=("proxyOptionsSharedEdits", 0))
                shareEditDefault = False
            else:
                shareEditDefault = True

        #Find Proxies and SubAssets
        proxyTypes = []
        subAssets = []

        for item in dir:
            if item.endswith(ext):
                noExt = item.rsplit(".")[0]

                proxy = noExt.rsplit("_")[-1]
                if not proxy in proxyTypes:
                    proxyTypes.append(proxy)

                subAsset = noExt.rsplit("_", 1)[0]
                if not subAsset in subAssets:
                    subAssets.append(subAsset)

        print proxyTypes
        print subAssets

        for subAsset in subAssets:
            #StoreNodes
            cmds.select(all=True)
            topN = cmds.ls(sl=True, type="transform")

            refFile = "%s_%s.%s" % (subAsset, proxyState, ext)
            if refFile in dir:
                #Create New Ref and find the name of the new Ref
                oldRefs = cmds.ls(references=True)
                cmds.select(all=True)
                oldTopNodes = cmds.ls(sl=True, type="transform")
                cmds.file(str(path + "/" + refFile), r=True, namespace = subAsset, options="v=0;p=17")
                newRef = cmds.ls(references=True)

                currentRef = None
                for ref in newRef:
                    if not ref in oldRefs:
                        currentRef = ref

                #if a new ref is created and the name is found
                if currentRef:
                    for proxy in proxyTypes:
                        if not proxyState in proxy:
                            refProxy = "%s_%s.%s" % (subAsset, proxy, ext)
                            if os.path.exists(path + "/" + refProxy):
                                proxyPath = path.split("\\")
                                proxyPath = proxyPath.join("/")
                                addItem = 'proxyAdd %s "%s" "%s";' % (currentRef, (proxyPath + "/" + refProxy), proxy)
                                mel.eval(addItem)

                cmds.setAttr(currentRef + ".proxyTag", proxyState, type="string")


                #If no asset group, create group and parent asset under group
                try:
                    if not assetType in topN:
                        cmds.group(name=str(assetType), empty=True)
                    if cmds.objExists(str(assetType)):
                        cmds.select(all=True)
                        newN = cmds.ls(sl=True, type="transform")
                        for n in newN:
                            if not n in topN:
                                try:
                                    cmds.parent(n, str(assetType))
                                except:
                                    pass
                except():
                    pass

    def exitWidget(self):
        global referenceLibForm
        self.ui.statusbar.showMessage('Quitting')
        referenceLibForm.close()

#IF not runned inside Maya
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

#If runned unside Maya
def UI():
    global referenceLibForm
    referenceLibForm = MyForm(getMayaWindow())
    referenceLibForm.show()
