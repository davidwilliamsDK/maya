#Import python modules
print "before anything"
import sys, os, re, shutil, random, sip, platform, webbrowser
import subprocess
import getpass
from PyQt4 import QtCore, QtGui
#import maya.app.general.createImageFormats as createImageFormats

#Import GUI
print "before QT"
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

#Custom import modules
from dsAssetOpenUI import Ui_AssetWindow
import dsCommon.dsOsUtil as dsOsUtil
reload(dsOsUtil)
import dsCommon.dsProjectUtil as dsProjectUtil
reload(dsProjectUtil)

try:
    import dsSgUtil as sgBridge
    reload(sgBridge)
except:
    pass

if dsOsUtil.mayaRunning() == True:
    import maya.app.general.createImageFormats as createImageFormats
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

#If inside Maya open Maya GUI
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AssetWindow()
        self.ui.setupUi(self)

        #For action, run def
        QtCore.QObject.connect(self.ui.productionComboBox, QtCore.SIGNAL("activated(int)"), self.assetTypeUpdate);
        QtCore.QObject.connect(self.ui.productionComboBox, QtCore.SIGNAL("activated(int)"), self.updateFilmComboBox);
        QtCore.QObject.connect(self.ui.productionComboBox, QtCore.SIGNAL("activated(int)"), self.minifigProduction);
        QtCore.QObject.connect(self.ui.assetTypeComboBox, QtCore.SIGNAL("activated(int)"), self.updateAssetSubTypeComboBox);
        QtCore.QObject.connect(self.ui.assetSubTypeComboBox, QtCore.SIGNAL("activated(int)"), self.assetListUpdate);
        QtCore.QObject.connect(self.ui.assetListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.assetListView);
        QtCore.QObject.connect(self.ui.iconButtonGroup, QtCore.SIGNAL("buttonClicked(int)"), self.iconUpdate);
        QtCore.QObject.connect(self.ui.iconCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.iconEnable);
        QtCore.QObject.connect(self.ui.createPushButton, QtCore.SIGNAL("clicked()"), self.createAsset);
        QtCore.QObject.connect(self.ui.createSelectionPushButton, QtCore.SIGNAL("clicked()"), self.createSelectedAsset);
        QtCore.QObject.connect(self.ui.assetNameTextEdit, QtCore.SIGNAL("returnPressed()"), self.createAsset);
        QtCore.QObject.connect(self.ui.createMinifigPushButton, QtCore.SIGNAL("clicked()"), self.createMinifigAsset);
        QtCore.QObject.connect(self.ui.removePushButton, QtCore.SIGNAL("clicked()"), self.removeAsset);
        QtCore.QObject.connect(self.ui.createIcon, QtCore.SIGNAL("clicked()"), self.createAssetIcon);
        QtCore.QObject.connect(self.ui.exportPart, QtCore.SIGNAL("clicked()"), self.exportPart);

        QtCore.QObject.connect(self.ui.incrPushButton, QtCore.SIGNAL("clicked()"), self.incrBackup);
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("activated(int)"), self.aboutMenu);
        self.ui.actionAbout.triggered.connect(self.aboutMenu)

        self.ui.actionExit.triggered.connect(self.closeEvent)
        self.ui.actionExit.triggered.connect(self.exitWidget)

        self.ui.menuHelp.triggered.connect(self.helpWiki)

        #Shotgun
        self.ui.actionReloadTemplates.triggered.connect(self.listTemplates)
        self.ui.reloadAssetStatus.triggered.connect(self.reloadAssetStatus)
        self.ui.actionImportMinifig.triggered.connect(self.importMinifig)

        #Init Widgets
        print "comboBox"
        self.updateProjectComboBox()

        #Set Context Menu for list widget
        self.ui.assetListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        self.ui.assetListWidget.customContextMenuRequested.connect(self.openMenu);

        #Gui Settings
        self.settings = QtCore.QSettings("Duckling&Sonne", "dsAssetOpen")
        self.iconCheckBoxState = True
        self.iconSizeState = "small"
        self.productionState = ""
        self.assetTypeState = ""
        self.assetSubTypeState = ""
        self.asset = ""
        self.setTemplateState = ""

        self.filmState = "No Episodes for this Project"

        self.templateSettings = False
        self.loadedTemplates = []

    	try:
    	  self.readSettings()
    	except Exception as e:
    	  print 'Read Settings fucked up! \nERROR:%s' % (e)

        self.setTemplates()
        self.minifigProduction()

        #disable buttons if not in maya
        if not dsOsUtil.mayaRunning() == True:
            self.ui.createIcon.setEnabled(False)
            self.ui.exportPart.setEnabled(False)
            self.ui.incrPushButton.setEnabled(False)
            self.ui.createSelectionPushButton.setEnabled(False)

    def helpWiki(self):
        url = "http://vfx.duckling.dk/?page_id=935"
        new = 2
        webbrowser.open(url, new=new)

    def importMinifig(self):
        source = dsProjectUtil.minifigGlobalSource()
        project = self.ui.productionComboBox.currentText()
        dest = dsProjectUtil.listMinifigTemplatePath(project)[0] + "/"

        #Copy Minifig
        shutil.copytree(str(source), str(dest))

        #Enable Create Minifig
        self.minifigProduction()

    def reloadAssetStatus(self):
        project = self.ui.productionComboBox.currentText()
        print "loading status for %s" % project
        sgAssetStatusList = sgBridge.sgGetAllAssetStatus(project)

        if sgAssetStatusList:
            for status in sgAssetStatusList:
                color = self.getColor(status['sg_status_list'])
		if not color:
			color = [255,255,255]
                path = str(dsProjectUtil.listAssetIcon(project, str(status['sg_asset_type']), str(status['sg_subtype']), str(status['code']))).rsplit("/",1)[0]

                if path != "None":
                    colorfile = file('%s/color.txt' % path, 'w')
                    colorfile.write(str(color))
                    colorfile.close()
            self.assetListUpdate()

    def getColor(self, status):
	if str(status) == "fin": return [0,200,0]
        if str(status) == "apr": return [0,190,0]

        if str(status) == "ip": return [0,100,0]
        if str(status) == "rev": return [255,255,0]

        if str(status) == "omt": return [200,0,0]
        if str(status) == "hld": return [200,0,0]

        if str(status) == "rdy": return [50,150,200]
        if str(status) == "wtg": return [50,150,200]

        if str(status) == "cmptc": return [200,150,200]
        if str(status) == "inc": return [200,150,200]
        if str(status) == "wtgc": return [200,150,200]

    def setTemplates(self):
        if self.loadedTemplates:
            self.updateTemplateCombobox(self.loadedTemplates)

    def setShotgunStatus(self, assetName, status):
        project = self.ui.productionComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()

        assetID = sgBridge.sgGetAssetID(project, assetName, assetType, assetSubType)
        sgBridge.sgSetAssetStatus(assetID, status)
        self.reloadAssetStatus()

    def listTemplates(self):
        if not self.templateSettings:
            print "Loading templates"
            sgEntity = "TaskTemplate"
            templates = sgBridge.sgGetTemplate(sgEntity)
            self.loadedTemplates = templates

            self.updateTemplateCombobox(templates)
            self.templateSettings = True
        else:
            print "Templates allready loaded"

    def updateTemplateCombobox(self, templates):
        self.ui.shotgunTemplateComboBox.clear()
        i=0
        for plate in templates:
            if not "Shot" in plate["code"]:
                    if not "Sequence" in plate["code"]:
                            if not "Comp" in plate["code"]:
                                self.ui.shotgunTemplateComboBox.addItem("")
                                text = "%s ID:%s" % (plate["code"], plate["id"])
                                self.ui.shotgunTemplateComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", text, None, QtGui.QApplication.UnicodeUTF8))
                                i = i+1
        self.setTemplateIndex()

    def setTemplateIndex(self):
        settings = QtCore.QSettings("Duckling&Sonne", "dsAssetOpen")
        self.setTemplateState = settings.value("currentTemplate").toString()
        if not self.ui.shotgunTemplateComboBox.findText(self.setTemplateState) == -1:
            self.ui.shotgunTemplateComboBox.setCurrentIndex(self.ui.shotgunTemplateComboBox.findText(self.setTemplateState))

    def exportPart(self, assetSettings=None):
        cmds.delete(ch=True)
        if assetSettings:
            project = assetSettings["projName"]
            assetType = assetSettings["assetType"]
            assetSubType = assetSettings["assetSubType"]
            assetName = assetSettings["assetName"]
        else:
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            assetName = self.ui.assetListWidget.currentItem().text()

        fileName = "%s%s_Model" % (dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, assetName), assetName)
        print fileName

        cmds.file(fileName, f=True, options="V=0", type="mayaAscii", es=True)

        self.createAssetIcon(True, assetSettings)

    def createAssetIcon(self, isolateView=False, assetSettings=None):
        if assetSettings:
            project = assetSettings["projName"]
            assetType = assetSettings["assetType"]
            assetSubType = assetSettings["assetSubType"]
            assetName = assetSettings["assetName"]
        else:
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            assetName = self.ui.assetListWidget.currentItem().text()

        filename = dsProjectUtil.listAssetIcon(project, assetType, assetSubType, assetName)
        try:
            self.renderIcon(isolateView)
            self.saveIcon(filename)
            self.saveIconToShotgun(project, assetName, assetType, assetSubType, filename)
        except:
            pass

        self.assetListUpdate()

    def renderIcon(self,isolateView=False):
        render = mel.eval("currentRenderer")
        if not render == "vray":
             cmds.setAttr("defaultRenderGlobals.currentRenderer", "vray", type="string")
        if not cmds.objExists('vraySettings'):
            cmds.createNode("VRaySettingsNode", n="vraySettings")

        selectedOption = mel.eval("optionVar -exists renderViewRenderSelectedObj")
        if isolateView:
            if selectedOption == 1:
                selectedValue = mel.eval("optionVar -q renderViewRenderSelectedObj")
                mel.eval("optionVar -intValue renderViewRenderSelectedObj 1;")

        cmds.setAttr("defaultRenderGlobals.animation", 1)
        cmds.setAttr("vraySettings.animBatchOnly", 1)
        width = cmds.getAttr("vraySettings.width")
        height = cmds.getAttr("vraySettings.height")
        vfb = cmds.getAttr("vraySettings.vfbOn")
        cmds.setAttr("vraySettings.width", 1280)
        cmds.setAttr("vraySettings.height", 720)
        cmds.setAttr("vraySettings.vfbOn", 0)
        mel.eval("renderWindowRender redoPreviousRender renderView;")

        cmds.setAttr("vraySettings.vfbOn", vfb)
        cmds.setAttr("vraySettings.width", width)
        cmds.setAttr("vraySettings.height", height)

        if isolateView:
            if selectedOption == 1:
                print selectedValue
                mel.eval("optionVar -intValue renderViewRenderSelectedObj %s;" % selectedValue)

    def saveIcon(self, filename):
        renderPanels = cmds.getPanel(scriptType="renderWindowPanel")
        formatManager = createImageFormats.ImageFormats()
        formatManager.pushRenderGlobalsForDesc("PNG")
        cmds.renderWindowEditor(renderPanels[0], e=True, writeImage=str(filename))
        formatManager.popRenderGlobals()

    def saveIconToShotgun(self, project, assetName, assetType, assetSubType, filename):
        sgBridge.sgCreateIcon(project, assetName, assetType, assetSubType, filename)


    def minifigProduction(self):
        project = self.ui.productionComboBox.currentText()
        path = dsProjectUtil.listMinifigTemplatePath(project)[0]

        if os.path.exists(path) == True:
            self.ui.createMinifigPushButton.setEnabled(True)
        else:
            self.ui.createMinifigPushButton.setEnabled(False)

    def updateProjectComboBox(self):
        '''This Def list all project in the project dir, with a config.xml file in the root'''
        self.ui.productionComboBox.clear()
        projects = dsProjectUtil.listProjects()
        print projects
        i = 0
        if projects:
            for project in projects:
                self.ui.productionComboBox.addItem("")
                self.ui.productionComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", project, None, QtGui.QApplication.UnicodeUTF8))
                i = i+1
        #self.assetTypeUpdate()
        #self.updateFilmComboBox()

    def assetTypeUpdate(self):
        self.ui.assetTypeComboBox.clear()
        path = dsProjectUtil.listAssetTypes(str(self.ui.productionComboBox.currentText()))
        i=0
        for folder in dsOsUtil.listFolder(path):
            self.ui.assetTypeComboBox.addItem("")
            self.ui.assetTypeComboBox.setItemText(i, QtGui.QApplication.translate("AssetWindow", folder, None, QtGui.QApplication.UnicodeUTF8))
            i=i+1
        self.updateAssetSubTypeComboBox()

    def updateAssetSubTypeComboBox(self):
        '''Lists all Sub Asset Types for a given Asset Type'''
        self.ui.assetSubTypeComboBox.clear()
        project = self.ui.productionComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        path = dsProjectUtil.listSubAssets(project, assetType)

        assetSubTypes = dsOsUtil.listFolder(str(path))
        i=0
        for assetSubType in assetSubTypes:
            self.ui.assetSubTypeComboBox.addItem("")
            self.ui.assetSubTypeComboBox.setItemText(i, QtGui.QApplication.translate("MainWindow", assetSubType, None, QtGui.QApplication.UnicodeUTF8))
            i = i+1
        self.assetListUpdate()

    def updateFilmComboBox(self):
        '''List all active films for selected project'''
        print "------------------------------------------------------------------------***************"
        try:
            self.ui.filmList.clear()
            project = self.ui.productionComboBox.currentText()
            episodes = dsProjectUtil.listEpisodes(project)
            print episodes

            i=0
            for episode in episodes:
                self.ui.filmList.addItem("")
                self.ui.filmList.setItemText(i, QtGui.QApplication.translate("MainWindow", episode, None, QtGui.QApplication.UnicodeUTF8))
                i = i+1
        except:
            self.ui.filmList.addItem("")
            self.ui.filmList.setItemText(0, QtGui.QApplication.translate("MainWindow", self.filmState, None, QtGui.QApplication.UnicodeUTF8))
            print "No Episodes"

    def assetListUpdate(self):
        self.iconUpdate()
        font = QtGui.QFont()
        font.setPixelSize(15)
        font.PreferAntialias
        font.setWeight(63)

        #Listing Assets
        project = self.ui.productionComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()

        path = str(dsProjectUtil.listAssets(project, assetType, assetSubType))
        self.ui.assetListWidget.clear()
        i = 0
        for asset in dsOsUtil.listFolder(path):
            picPath = dsProjectUtil.listAssetIcon(project, assetType, assetSubType, asset)
            if picPath:
                if os.path.exists(picPath) == True:
                    item = QtGui.QListWidgetItem(self.ui.assetListWidget)
                    if self.ui.iconCheckBox.isChecked() == True:
                    #Add Icon
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap(picPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:
                        #Icon dosen't exist add new row
                        #self.ui.assetListWidget.addItem("")
                        pass
                        #print "Icon Doesen't exists"

                    path = str(picPath).rsplit("/", 1)[0]
                    dirs = []
                    if os.path.exists("%s/color.txt" % path):
                        f = open("%s/color.txt" % path, "r")
                        color = f.readline()
                        dirs = eval(color)

                    if dirs != []:
                        self.ui.assetListWidget.item(i).setBackgroundColor(QtGui.QColor(dirs[0], dirs[1], dirs[2]))
                        self.ui.assetListWidget.item(i).setTextColor(QtGui.QColor(0, 0, 0))

                else:
                    self.ui.assetListWidget.item(i).setSizeHint(QSize(20 ,20))

                self.ui.assetListWidget.item(i).setFont(font)
                self.ui.assetListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", asset, None, QtGui.QApplication.UnicodeUTF8))
                i=i+1

    def assetListView(self, item):
        if ".." in item.text():
            MyForm.assetListUpdate(self)
            self.ui.dirPathLabel.clear()
        elif ".ma" in item.text():
            MyForm.openMaFiles(self, item.text())
        else:
            self.asset = item.text()
            MyForm.listMaFiles(self, item)


    def listMaFiles(self, item="", fullPath=False):
        if fullPath == False:
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            asset = item.text()

            maFolder = dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, asset)
        if fullPath == True:
            maFolder = item

        if dsOsUtil.listMa(maFolder) != "ERROR":
            self.ui.dirPathLabel.setText(QtGui.QApplication.translate("AssetWindow", maFolder, None, QtGui.QApplication.UnicodeUTF8))

            i=0

            self.ui.assetListWidget.clear()
            self.ui.assetListWidget.addItem("")
            self.ui.assetListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", "..", None, QtGui.QApplication.UnicodeUTF8))

            for asset in dsOsUtil.listMa(maFolder):
                i=i+1
                self.ui.assetListWidget.addItem("")
                self.ui.assetListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", asset, None, QtGui.QApplication.UnicodeUTF8))
            self.ui.dirPathLabel.setText(maFolder)

        else:
            self.ui.statusbar.showMessage("Path dosen't exist: " + maFolder)

    def iconUpdate(self):
        #Icon Size
        iconSize = [100,500]
        if self.ui.iconMediumRadioButton.isChecked() == 1:
            iconSize[0] = 150
        elif self.ui.iconBigRadioButton.isChecked() == 1:
            iconSize[0] = 200

        self.ui.assetListWidget.setIconSize(QtCore.QSize(iconSize[0], iconSize[1]))

    def iconEnable(self):
        if self.ui.iconCheckBox.isChecked() == True:
            #Enable Buttons
            self.ui.iconSmallRadioButton.setEnabled(True)
            self.ui.iconMediumRadioButton.setEnabled(True)
            self.ui.iconBigRadioButton.setEnabled(True)

            self.iconUpdate()
            self.assetListUpdate()
        else:
            #Disable Buttons
            self.ui.iconSmallRadioButton.setEnabled(False)
            self.ui.iconMediumRadioButton.setEnabled(False)
            self.ui.iconBigRadioButton.setEnabled(False)
            self.ui.assetListWidget.setIconSize(QtCore.QSize(0, 0))

    def createMinifigAsset(self):
        if self.ui.assetNameTextEdit.text() == "":
            print "No name Typed"
        else:
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            shotgunTemplate = str(self.ui.shotgunTemplateComboBox.currentText()).rsplit(" ", 1)[0]

            path = dsProjectUtil.listAssets(project, assetType, assetSubType)
            assetName = self.ui.assetNameTextEdit.text()
            templateVal = dsProjectUtil.listMinifigTemplatePath(project)
            print templateVal
            assetMinifigTemplate = templateVal[0]
            assetMinifigTemplateName = templateVal[1]

            newSubAsset = path + "/" + assetName
            i=0

            if os.path.exists(newSubAsset) == True:
                self.ui.statusbar.showMessage("Asset Already Exists")
            else:
                shutil.copytree(str(assetMinifigTemplate), str(newSubAsset))
                for root, dirs, files in os.walk(str(newSubAsset)):
                    for item in files:
                        if assetMinifigTemplateName in item:
                            nameSplit = item.split("_")

                            oldPath = os.path.join(root, item)
                            newPath = os.path.join(root, item.replace(assetMinifigTemplateName, assetName))

                            if item.endswith(".ma"):
                                oldArray = [("$AssetFilePath/%s" % (assetMinifigTemplateName)), ("%s_%s" % (assetMinifigTemplateName, nameSplit[1])), "{assetName}", "{assetType}", "{assetSubType}", "{assetProject}"]
                                newArray = [("$AssetFilePath/%s" % (assetName)), ("%s_%s" % (assetName, nameSplit[1])), assetName, assetType, assetSubType, project]
                                dsOsUtil.readReplaceMa(oldPath, oldArray, newArray)
                            shutil.move(oldPath, newPath)
                            i=i+1

        MyForm.assetListUpdate(self)
        self.ui.statusbar.showMessage("Asset created:  " + assetName)

        list = [["Asset", "sg_asset_type", assetType],["Asset", "sg_subtype", assetSubType]]
        sgBridge.addTypesToList(list)

        assetID = sgBridge.sgCreateAsset(project, assetName, assetType, assetSubType)
        sgBridge.setTemplate(assetID, shotgunTemplate)

        self.ui.assetNameTextEdit.clear()

    def createSelectedAsset(self):
        #Make sure something is selected
        sel = cmds.ls(sl=True, long=True)
        if not sel == []:
            #Prepare
            asset = cmds.duplicate(sel)
            selNew= cmds.ls(sl=True, long=True)
            try:
                cmds.parent(selNew, w=True)
            except:
                print "Already parented to World"

            #Create The Asset
            print "creating Asset"
            assetSettings = self.createAsset()

            #Export Selected to the model File
            print "Exporting part to model"
            self.exportPart(assetSettings)

            project = str(assetSettings["projName"])
            assetType = str(assetSettings["assetType"])
            assetSubType = str(assetSettings["assetSubType"])
            assetName = str(assetSettings["assetName"])

            #Finish The Setup and Publish
            melCmd = ('source assetExportSetup; cleanAssetExport "%s";' % str(assetSettings))
            fileName = "%s%s_Rig.ma" % (dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, assetName), assetName)
            print fileName

            logPath = "C:\\assetExport_log.txt"
            os.system("maya -batch -log '%s' -command '%s' -file '%s'" % (logPath, str(melCmd), fileName))

            #Cleanup
            cmds.delete(cmds.ls(sl=True, long=True))
            cmds.select(sel)
        else:
            print "Please Select Something to Export"

    def createAsset(self):
        if self.ui.assetNameTextEdit.text() == "":
            print "No name Typed"
        else:
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            film = self.ui.filmList.currentText()
            shotgunTemplate = str(self.ui.shotgunTemplateComboBox.currentText()).rsplit(" ", 1)[0]

            path = dsProjectUtil.listAssets(project, assetType, assetSubType)
            assetName = self.ui.assetNameTextEdit.text()
            templateVal = dsProjectUtil.listTemplatePath(project)
            assetTemplate = templateVal[0]
            assetTemplateName = templateVal[1]

            newSubAsset = path + "/" + assetName
            i=0

            if os.path.exists(newSubAsset) == True:
                self.ui.statusbar.showMessage("Asset Already Exists")
            else:
                shutil.copytree(str(assetTemplate), str(newSubAsset))
                for root, dirs, files in os.walk(str(newSubAsset)):
                    for item in files:
                        if assetTemplateName in item:
                            nameSplit = item.split("_")

                            oldPath = os.path.join(root, item)
                            newPath = os.path.join(root, item.replace(assetTemplateName, assetName))

                            if item.endswith(".ma"):
                                oldArray = [("{$assetFilePath}/%s" % (assetTemplateName)), ("%s_%s" % (assetTemplateName, nameSplit[1])), "{assetName}", "{assetType}", "{assetSubType}", "{assetProject}"]
                                newArray = [("{$assetFilePath}/%s" % (assetName)), ("%s_%s" % (assetName, nameSplit[1])), assetName, assetType, assetSubType, project]
                                dsOsUtil.readReplaceMa(oldPath, oldArray, newArray)
                            shutil.move(oldPath, newPath)
                            i=i+1

        MyForm.assetListUpdate(self)
        self.ui.statusbar.showMessage("Asset created:  " + assetName)

        print film
        list = [["Asset", "sg_asset_type", assetType],["Asset", "sg_subtype", assetSubType]]
        sgBridge.addTypesToList(list)
        assetID = sgBridge.sgCreateAsset(project, assetName, assetType, assetSubType)
        sgBridge.setTemplate(assetID, shotgunTemplate)
        sgBridge.setEpisode(assetID, film)


        self.ui.assetNameTextEdit.clear()
        return {'projName':project, 'assetType':assetType, 'assetSubType':assetSubType, 'assetName':assetName}

    def removeAsset(self):
        currentSelection = self.ui.assetListWidget.currentItem()

        if currentSelection == None:
            self.ui.statusbar.showMessage("No Asset Selected")
            mel.eval('print "Please select asset"')
        else:
            #Listing Assets
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()

            path = str(dsProjectUtil.listAssets(project, assetType, assetSubType) + "/" + currentSelection.text())
            MyForm.deleteConfirmDialog(self, path)

        #Remove from shotgun too....
        sgBridge.sgRemoveAsset(project, currentSelection.text(), assetType, assetSubType)

    def openMaFiles(self, item):
        path = self.ui.dirPathLabel.text()
        if path == "":
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            assetName = self.ui.assetListWidget.currentItem().text()

            dir = dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, assetName)
            if os.path.exists(dir):
                path=dir

        if not path == "":
            asset = item
            devFile = "%s/%s" % (path, asset)

            if dsOsUtil.mayaRunning() == True:
                if cmds.file(q=True, anyModified=True) == True:
                    MyForm.saveConfirmDialog(self, devFile)
                else:
                    cmds.file( devFile, o=True )
                    mel.eval('print "Scene opened: %s"' % devFile)
            else:
                if platform.system() == "Windows":
                    subprocess.call(["C:\\Program Files\\Autodesk\\Maya2011\\bin\\maya.exe", devFile])
                elif platform.system() == "Linux":
                    subprocess.call(["maya", devFile])

    def deleteConfirmDialog(self, itemPath):
        posetiveStatus = "Asset Removed"
        negativeStatus = "Abort"

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Want to delete this Asset?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if os.path.isdir(itemPath) == True:
                shutil.rmtree(str(itemPath))
                self.ui.assetListWidget.takeItem(self.ui.assetListWidget.currentRow())
                self.ui.statusbar.showMessage(posetiveStatus)
            else:
                path = self.ui.dirPathLabel.text()
                os.remove(str(itemPath))
                MyForm.listMaFiles(self, str(path), True)
        else:
            self.ui.statusbar.showMessage(negativeStatus)

    def importAsset(self, item):
        path = self.ui.dirPathLabel.text()
        if path == "":
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            assetName = self.ui.assetListWidget.currentItem().text()

            dir = dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, assetName)
            if os.path.exists(dir):
                path=dir

        if not path == "":
            asset = item
            devFile = "%s/%s" % (path, asset)

            if dsOsUtil.mayaRunning() == True:
                cmds.file(devFile, i=True )
                mel.eval('print "File Imported: %s"' % (devFile))
            else:
                os.system("maya.exe -file %s" % (devFile))

    def refAsset(self, item):
        path = self.ui.dirPathLabel.text()
        if path == "":
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            assetName = self.ui.assetListWidget.currentItem().text()

            dir = dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, assetName)
            if os.path.exists(dir):
                path=dir

        if not path == "":
            asset = item
            devFile = "%s/%s" % (path, asset)
            if "_" in asset:
                name = asset.split("_", 1)[0]
            else:
                name = asset

            if dsOsUtil.mayaRunning() == True:
                cmds.file(devFile, r=True, namespace=str(name), options="v=0", shd="shadingNetworks")
                mel.eval('print "File Referenced: %s"' % (devFile))
            else:
                os.system("maya.exe -file %s" % (devFile))

    def incrBackup(self):
        posetiveStatus = "Backup created"
        negativeStatus = "No file selected - please select .ma file"

        assetPath = self.ui.dirPathLabel.text()
        asset = self.ui.assetListWidget.currentItem().text()

        filePath = (assetPath + asset)
        incrementFolder = assetPath + "/Increment"
        user = getpass.getuser()

        if str(user) == "administrator":
            user = "adm"

        files=[]
        if asset != None:
            if asset.split(".")[-1] == "ma":
                if not os.path.exists(incrementFolder):
                    os.mkdir(incrementFolder)
                for item in dsOsUtil.listMa(incrementFolder):
                    if str(asset[1:-3]) in str(item):
                        files.append(item.split("_")[-2])

                if len(files) == 0:
                    incrValue = 1
                else:
                    incrValue = int(sorted(files)[-1])+1

                newPath = incrementFolder + "/" + asset.split(".")[0] + "_" + "%.3d" % incrValue + "_" + user + ".ma"

                shutil.copy(filePath, newPath)

                self.ui.statusbar.showMessage(posetiveStatus)
            else:
                self.ui.statusbar.showMessage(negativeStatus)
        else:
            self.ui.statusbar.showMessage(negativeStatus)

    def saveConfirmDialog(self, item):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Want to to Save, before closing?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            cmds.file( save=True, type='mayaAscii' )
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File saved - File opened")
            mel.eval('print "File Saved - File Opened"')
        elif reply == QtGui.QMessageBox.No:
            print item
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File opened")
            mel.eval('print "File Opened: %s"' % item)
        else:
            self.ui.statusbar.showMessage("Open Scene Cancled")
            mel.eval('print "Cancled"')

    def openAssetExplore(self):
        path = self.ui.dirPathLabel.text()
        if path == "":
            project = self.ui.productionComboBox.currentText()
            assetType = self.ui.assetTypeComboBox.currentText()
            assetSubType = self.ui.assetSubTypeComboBox.currentText()
            path = dsProjectUtil.listSubAssets(project, assetType) + "/" + assetSubType + "/"
        dsOsUtil.openInBrowser(path)

    def aboutMenu(self):
        aboutDialog = QDialog()
        aboutDialog.setObjectName("About")
        aboutDialog.resize(450, 220)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutDialog.sizePolicy().hasHeightForWidth())
        aboutDialog.setSizePolicy(sizePolicy)
        aboutDialog.textBrowser = QtGui.QTextBrowser(aboutDialog)
        aboutDialog.textBrowser.setEnabled(True)
        aboutDialog.textBrowser.setGeometry(QtCore.QRect(10, 10, 430, 200))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutDialog.textBrowser.sizePolicy().hasHeightForWidth())
        aboutDialog.textBrowser.setSizePolicy(sizePolicy)
        aboutDialog.textBrowser.setObjectName("textBrowser")

        aboutDialog.setWindowTitle(QtGui.QApplication.translate("About", "About", None, QtGui.QApplication.UnicodeUTF8))
        aboutDialog.textBrowser.setHtml(QtGui.QApplication.translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Asset Open Dialog</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Updated: Sunday, 10th July 2011</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">By Karsten Friis Nielsen</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">karsten_friis_nielsen@hotmail.com</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Duckling&Sonne (c)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        aboutDialog.exec_()
        aboutDialog.setVisible()

    def openMenu(self, position):
        menu = QMenu()
        openMenu = QMenu("Open")
        importMenu = QMenu("Import")
        refMenu = QMenu("Ref")

        selectedItem = self.ui.assetListWidget.currentItem()
        incrAction=""
        removeAction=""
        openAction = ""
        importAction = ""
        refAction = ""
        revAction = ""
        progressAction = ""

        project = self.ui.productionComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()
        asset = selectedItem.text()


        if selectedItem != None:
            #If Ma file selected
            if ".ma" in selectedItem.text():
                openAction = menu.addAction("Open")
                if dsOsUtil.mayaRunning() == True:
                    refAction = menu.addAction("Ref")
                    importAction = menu.addAction("Import")
                    removeAction = menu.addAction("Remove")
                incrAction = menu.addAction("Increment Backup")

            #If Folder Selected
            else:
                maFolder = dsProjectUtil.listAssetDevPath(project, assetType, assetSubType, asset)
                menu.addMenu(openMenu)
                menu.addMenu(importMenu)
                menu.addMenu(refMenu)
                for item in dsOsUtil.listMa(maFolder):
                    openA = openMenu.addAction(item)
                    importA = importMenu.addAction(item)
                    refA = refMenu.addAction(item)
                    self.connect(openA,QtCore.SIGNAL('triggered()'), lambda item=item: self.openMaFiles(item=item))
                    self.connect(importA,QtCore.SIGNAL('triggered()'), lambda item=item: self.importAsset(item=item))
                    self.connect(refA,QtCore.SIGNAL('triggered()'), lambda item=item: self.refAsset(item=item))
                openMenu.addAction(openA)
                importMenu.addAction(importA)
                refMenu.addAction(refA)


                menu.addSeparator()
                removeAction = menu.addAction("Remove Folder")


        menu.addSeparator()
        timelog = menu.addAction("Time Log")
        quitAction = menu.addAction("Quit")
        exploreAction = menu.addAction("Open in Explore")
        menu.addSeparator()

        path = str(dsProjectUtil.listAssetIcon(project, assetType, assetSubType, asset)).rsplit("/",1)[0]
        currentStatus = []
        if os.path.exists("%s/color.txt" % path):
            f = open("%s/color.txt" % path, "r")
            color = f.readline()
            currentStatus = eval(color)

        if currentStatus !=[]:
            if currentStatus != [0,200,0]:
                if currentStatus != [255,255,0]:
                    if currentStatus != [0,100,0]:
                        progressAction = menu.addAction("Set Status In Progress")
                    revAction = menu.addAction("Set Status In Review")


        action = menu.exec_(self.ui.assetListWidget.mapToGlobal(position))


        #Check Action
        if action == quitAction:
            self.exitWidget()
        if action == timelog:
            self.timelog()
        if action == exploreAction:
            self.openAssetExplore()
        if action == incrAction:
            MyForm.incrBackup(self)
        if action == removeAction:
            MyForm.removeAsset(self)
        if action == openAction:
            MyForm.assetListView(self, selectedItem)
        if action == importAction:
            MyForm.importAsset(self, selectedItem.text())
        if action == refAction:
            MyForm.refAsset(self, selectedItem.text())
        if action == revAction:
            status = "rev"
            MyForm.setShotgunStatus(self, selectedItem.text(), status)
        if action == progressAction:
            status = "ip"
            MyForm.setShotgunStatus(self, selectedItem.text(), status)

    def timelog(self):
        print "print open timelog window"
        pass

    def closeEvent(self, event):
        self.writeSettings()

    def exitWidget(self):
        if dsOsUtil.mayaRunning() == True:
            global assetOpenForm
            self.ui.statusbar.showMessage('Quitting')
            mel.eval('print "Asset Open Dialog closed"')
            assetOpenForm.close()
        else:
            self.close()

    def readSettings(self):
        '''Read application settings from the QT Settings object.'''
        settings = QtCore.QSettings("Duckling&Sonne", "dsAssetOpen")

        self.iconCheckBoxState = settings.value("iconCheckBoxState").toBool()
        self.ui.iconCheckBox.setChecked(self.iconCheckBoxState)

        self.productionState = settings.value("productionState").toString()
        if not self.ui.productionComboBox.findText(self.productionState) == -1:
            self.ui.productionComboBox.setCurrentIndex(self.ui.productionComboBox.findText(self.productionState))
            MyForm.assetTypeUpdate(self)
            MyForm.updateFilmComboBox(self)

        self.assetTypeState = settings.value("assetTypeState").toString()
        if not self.ui.assetTypeComboBox.findText(self.assetTypeState) == -1:
            self.ui.assetTypeComboBox.setCurrentIndex(self.ui.assetTypeComboBox.findText(self.assetTypeState))
            MyForm.updateAssetSubTypeComboBox(self)

        self.assetSubTypeState = settings.value("assetSubTypeState").toString()
        assetSubValue = self.ui.assetSubTypeComboBox.findText(self.assetSubTypeState)
        if not assetSubValue == -1:
            self.ui.assetSubTypeComboBox.setCurrentIndex(assetSubValue)

        self.iconSizeState = settings.value("iconSizeState").toString()
        buttons = self.ui.iconButtonGroup.buttons()
        for button in buttons:
            if button.text() == self.iconSizeState:
                button.setChecked(True)

        tempTempPlates = settings.value("loadedTemplates").toString()
        loadedTemplates = eval(str(tempTempPlates))
        for t in loadedTemplates:
            self.loadedTemplates.append(t)

        MyForm.assetListUpdate(self)

    def writeSettings(self):
        '''Write settings'''
        settings = QtCore.QSettings("Duckling&Sonne", "dsAssetOpen")

        settings.setValue("iconCheckBoxState", self.ui.iconCheckBox.isChecked())

        settings.setValue("productionState", self.ui.productionComboBox.currentText())
        settings.setValue("assetTypeState", self.ui.assetTypeComboBox.currentText())
        settings.setValue("assetSubTypeState", self.ui.assetSubTypeComboBox.currentText())

        settings.setValue("iconSizeState", self.ui.iconButtonGroup.checkedButton().text())
        settings.setValue("loadedTemplates", str(self.loadedTemplates))
        settings.setValue("currentTemplate", self.ui.shotgunTemplateComboBox.currentText())

#IF not runned inside Maya
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

#If runned unside Maya
def UI():
    global assetOpenForm
    assetOpenForm = MyForm(getMayaWindow())
    assetOpenForm.show()
