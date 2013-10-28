#Importing Modules
import sys, os, platform, shutil, webbrowser, subprocess
#from thread import start_new_thread as snt

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
guiName = "dsAssetOpenV2_UI.ui"
if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsAssetOpenV2/%s' % guiName
else:
    sys.path.append('/dsCore/maya/dsCommon/')
    uiFile = 'U:/dsCore/maya/dsAssetOpenV2/%s' % guiName

#INSIDE MAYA RUN THIS STUFF!
pyVal = dsOsUtil.getPyGUI()
if dsOsUtil.mayaRunning() == True:
    import maya.app.general.createImageFormats as createImageFormats
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
        #-------------------------------------------------------------GUI SETUP STARTS--------------------------------------------------------------------------
        #Setup Window
        super(MyForm, self).__init__(parent)
        self.setupUi(self)

        '''READ GUI SETTINGS!!!'''
        self.prjState = None
        self.mjrState= None
        self.minState = None
        self.sgFilmLink = None
        self.sgTemp = None
        self.sgTempLoad = None

        try:
    	  self.readSettings()
    	except:
            pass

        '''CONNECT BUTTONS, SLIDERS ETC...'''
        QtCore.QObject.connect(self.D2, QtCore.SIGNAL("clicked(int)"), self.addType);
        QtCore.QObject.connect(self.D2, QtCore.SIGNAL("clicked(int)"), self.addSubType);
        QtCore.QObject.connect(self.D3, QtCore.SIGNAL("clicked(int)"), self.addType);
        QtCore.QObject.connect(self.D3, QtCore.SIGNAL("clicked(int)"), self.addSubType);
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(int)"), self.addSubType);
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(int)"), self.list);
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(int)"), self.bgColor);
        QtCore.QObject.connect(self.subType, QtCore.SIGNAL("activated(int)"), self.list);
        QtCore.QObject.connect(self.subType, QtCore.SIGNAL("activated(int)"), self.bgColor);
        QtCore.QObject.connect(self.search, QtCore.SIGNAL("returnPressed()"), self.list);
        QtCore.QObject.connect(self.search, QtCore.SIGNAL("returnPressed()"), self.bgColor);
        QtCore.QObject.connect(self.iconSlider, QtCore.SIGNAL("valueChanged(int)"), self.iconUpdate);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.listAssets);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.list);
        QtCore.QObject.connect(self.mbrick, QtCore.SIGNAL("stateChanged(int)"), self.enableDisableGUI);
        QtCore.QObject.connect(self.project, QtCore.SIGNAL("activated(int)"), self.listMajors);
        QtCore.QObject.connect(self.major, QtCore.SIGNAL("activated(int)"), self.bgColor);
        QtCore.QObject.connect(self.major, QtCore.SIGNAL("activated(int)"), self.listMinor);
        QtCore.QObject.connect(self.minor, QtCore.SIGNAL("activated(int)"), self.assetView);
        QtCore.QObject.connect(self.major, QtCore.SIGNAL("activated(int)"), self.assetView);
        QtCore.QObject.connect(self.project, QtCore.SIGNAL("activated(int)"), self.updateFilmComboBox);

        QtCore.QObject.connect(self.modelList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.assetHandler);
        QtCore.QObject.connect(self.modelList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.bgColor);
        QtCore.QObject.connect(self.modelList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.assetView);

        QtCore.QObject.connect(self.libraryShow, QtCore.SIGNAL("stateChanged(int)"), self.libMenuShow);
        QtCore.QObject.connect(self.libraryShow, QtCore.SIGNAL("stateChanged(int)"), self.listAssets);
        QtCore.QObject.connect(self.libraryShow, QtCore.SIGNAL("stateChanged(int)"), self.list);
        QtCore.QObject.connect(self.libraryShow, QtCore.SIGNAL("stateChanged(int)"), self.addType);
        QtCore.QObject.connect(self.libraryShow, QtCore.SIGNAL("stateChanged(int)"), self.addSubType);
        QtCore.QObject.connect(self.libraryFilters, QtCore.SIGNAL("stateChanged(int)"), self.libFiltersMenuShow);
        QtCore.QObject.connect(self.assetIconSlider, QtCore.SIGNAL("valueChanged(int)"), self.iconUpdate);
        QtCore.QObject.connect(self.wrapIconsCheckbox, QtCore.SIGNAL("stateChanged(int)"), self.wrapIcons);
        QtCore.QObject.connect(self.assetSearch, QtCore.SIGNAL("returnPressed()"), self.assetView);

        QtCore.QObject.connect(self.assetName, QtCore.SIGNAL("returnPressed()"), self.createAsset);
        QtCore.QObject.connect(self.assetCreate, QtCore.SIGNAL("clicked()"), self.createAsset);
        QtCore.QObject.connect(self.assetRemove, QtCore.SIGNAL("clicked()"), self.rmAsset);
        QtCore.QObject.connect(self.iconCreate, QtCore.SIGNAL("clicked()"), self.createAssetIcon);
        QtCore.QObject.connect(self.partExport, QtCore.SIGNAL("clicked()"), self.exportPart);
        QtCore.QObject.connect(self.assetExport, QtCore.SIGNAL("clicked()"), self.createSelectedAsset);
        QtCore.QObject.connect(self.project, QtCore.SIGNAL("activated(int)"), self.setFilm)
        QtCore.QObject.connect(self.major, QtCore.SIGNAL("activated(int)"), self.setFilm)

        """DRAG AND DROP"""
        #QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("dropped"), self.assetDropped)
        #self.listWidget.dropped.connect(self.assetDropped)

        self.actionExit.triggered.connect(self.closeEvent)
        self.actionExit.triggered.connect(self.exitWidget)

        #Action Menu
        #Shotgun
        self.actionReload_Templates.triggered.connect(self.listTemplates)
        self.actionReload_Asset_Status.triggered.connect(self.reloadAssetStatus)
        self.actionWiki.triggered.connect(self.helpWiki)
        self.actionShow_Project_Settings.triggered.connect(self.showProjectMenu)
        self.actionShow_Library.triggered.connect(self.libMenuAction)
        self.actionShow_Library_Filters.triggered.connect(self.libFiltersMenuAction)
        #self.actionShow_Menu.triggered.connect(self.showMenu)

        #Set Context Menu for list widget
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.openMenu)

        self.libraryPath = projectUtil.libraryPath() + "/asset/"

        #Model Lib Database
        self.asset3D = []
        self.asset3Dtype = []
        self.asset3DsubType = []
        self.listed3D = 0

        self.asset2D = []
        self.asset2Dtype = []
        self.asset2DsubType = []
        self.listed2D = 0

        #Asset List
        self.assets = []
        self.assetsInDst = []
        self.prj = ""
        self.eps = ""

        self.mBrick = []
        self.listedmBrick = 0

        self.currentAssetList = []

        self.projects = projectUtil.listProjects()
        self.filmState = "No Episodes for this Project"

        self.listProjects()
        self.listAssets()
        self.addType()
        self.addSubType()
        self.list()
        self.iconUpdate("iconSlider")
        self.iconUpdate("assetIconSlider")
        self.autoSetting()
        self.updateFilmComboBox()
        self.assetView()
        self.enableDisableGUI()
        self.setFilm()
        self.libMenuShow()
        if self.sgTempLoad: self.updateTemplateCombobox(self.sgTempLoad)

        self.sgLoaded = False
        self.bgColor()
        self.libSize = 0

        self.sgLoaded == 0
        self.templateSettings = None

        self.loadedTemplates = self.sgTempLoad
        self.copyP()
    #-------------------------------------------------------------GUI SETUP ENDS--------------------------------------------------------------------------

    #-----------------------------------------------------------ASSET DEFS STARTS-------------------------------------------------------------------------
    def guiSize(self):
        height = self.height()
        width = self.width()
        self.libSize = self.modelLibDock.width()

        if not self.libraryShow.isChecked():
            self.resize(width - self.libSize, height)

    def copyP(self):
        """START COPY"""
        self.copyLabel.setVisible(True)
        self.copyProgress.setVisible(True)

        """END COPY"""
        self.copyLabel.setVisible(False)
        self.copyProgress.setVisible(False)


    def createAsset(self):
        self.loadSgBridge()
        global sgBridge
        if self.assetName.text() == "":
            print "No name Typed"
        else:
            project = self.project.currentText()
            assetType = self.major.currentText()
            assetSubType = self.minor.currentText()
            film = self.sgLink.currentText()
            shotgunTemplate = str(self.sgTemplate.currentText()).rsplit(" ", 1)[0]

            path = projectUtil.listAssets(project, assetType, assetSubType)
            assetName = self.assetName.text()
            templateVal = projectUtil.listTemplatePath(project)
            assetTemplate = templateVal[0]
            assetTemplateName = templateVal[1]

            newSubAsset = path + "/" + assetName
            i=0

            if os.path.exists(newSubAsset) == True:
                self.statusbar.showMessage("Asset Already Exists")
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

        self.assetView()
        self.statusbar.showMessage("Asset created:  " + assetName)

        list = [["Asset", "sg_asset_type", assetType],["Asset", "sg_subtype", assetSubType]]
        sgBridge.addTypesToList(list)
        assetID = sgBridge.sgCreateAsset(project, assetName, assetType, assetSubType)
        sgBridge.setTemplate(assetID, shotgunTemplate)
        print assetID
        print film
        print "------------------------------------"
        if not film == "No Episodes for this Project":
            sgBridge.setEpisode(assetID, film)


        self.assetName.clear()
        return {'projName':project, 'assetType':assetType, 'assetSubType':assetSubType, 'assetName':assetName}

    def exportPart(self, assetSettings=None):
        cmds.delete(ch=True)
        if assetSettings:
            project = assetSettings["projName"]
            assetType = assetSettings["assetType"]
            assetSubType = assetSettings["assetSubType"]
            assetName = assetSettings["assetName"]
        else:
            project = self.project.currentText()
            assetType = self.major.currentText()
            assetSubType = self.minor.currentText()
            assetName = self.listWidget.currentItem().text()

        fileName = "%s%s_Model" % (projectUtil.listAssetDevPath(project, assetType, assetSubType, assetName), assetName)
        cmds.file(fileName, f=True, options="V=0", type="mayaAscii", es=True)
        self.createAssetIcon(True, assetSettings)

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
            assetSettings = self.createAsset()

            #Export Selected to the model File
            self.exportPart(assetSettings)

            project = str(assetSettings["projName"])
            assetType = str(assetSettings["assetType"])
            assetSubType = str(assetSettings["assetSubType"])
            assetName = str(assetSettings["assetName"])

            #Finish The Setup and Publish
            melCmd = ('source assetExportSetup; cleanAssetExport "%s";' % str(assetSettings))
            fileName = "%s%s_Rig.ma" % (projectUtil.listAssetDevPath(project, assetType, assetSubType, assetName), assetName)

            logPath = "C:\\assetExport_log.txt"
            os.system("maya -batch -log '%s' -command '%s' -file '%s'" % (logPath, str(melCmd), fileName))

            #Cleanup
            cmds.delete(cmds.ls(sl=True, long=True))
            cmds.select(sel)
        else:
            print "Please Select Something to Export"

    def rmAsset(self):
        currentSelection = self.listWidget.currentItem()

        if currentSelection == None:
            self.statusbar.showMessage("No Asset Selected")
        else:
            project = self.project.currentText()
            assetType = self.major.currentText()
            assetSubType = self.minor.currentText()

            path = str(projectUtil.listAssets(project, assetType, assetSubType) + "/" + currentSelection.text())
            self.deleteConfirmDialog(path)

    def deleteConfirmDialog(self, itemPath):
        posetiveStatus = "Asset Removed"
        negativeStatus = "Abort"

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Want to delete this Asset?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if os.path.isdir(itemPath) == True:
                self.loadSgBridge()
                global sgBridge
                sgBridge.sgRemoveAsset(self.project.currentText(), self.listWidget.currentItem().text(), self.major.currentText(), self.minor.currentText())
                shutil.rmtree(str(itemPath))
                self.listWidget.takeItem(self.listWidget.currentRow())
                self.statusbar.showMessage(posetiveStatus)
        else:
            self.statusbar.showMessage(negativeStatus)

    def createAssetIcon(self, isolateView=False, assetSettings=None):
        if dsOsUtil.mayaRunning():
            if assetSettings:
                project = assetSettings["projName"]
                assetType = assetSettings["assetType"]
                assetSubType = assetSettings["assetSubType"]
                assetName = assetSettings["assetName"]
            else:
                project = self.project.currentText()
                assetType = self.major.currentText()
                assetSubType = self.minor.currentText()
                assetName = self.listWidget.currentItem().text()

            print "GOT THIS FAR"
            filename = projectUtil.listAssetIcon(project, assetType, assetSubType, assetName)
            try:
                self.renderIcon(isolateView)
                print "1"
                print filename
                self.saveIcon(filename)
                print "2"
                self.saveIconToShotgun(project, assetName, assetType, assetSubType, filename)
            except:
                pass
            self.assetView()
        else:
            self.statusbar.showMessage("CAN ONLY CREATE ICONS IN MAYA")

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
        print "RUNNING SAVE ICON"
        renderPanels = cmds.getPanel(scriptType="renderWindowPanel")
        print "2"
        formatManager = createImageFormats.ImageFormats()
        formatManager.pushRenderGlobalsForDesc("PNG")
        print filename
        cmds.renderWindowEditor(renderPanels[0], e=True, writeImage=str(filename))
        formatManager.popRenderGlobals()

    def saveIconToShotgun(self, project, assetName, assetType, assetSubType, filename):
        self.loadSgBridge()
        global sgBridge
        sgBridge.sgCreateIcon(project, assetName, assetType, assetSubType, filename)

    def updateFilmComboBox(self):
        '''List all active films for selected project'''
        self.sgLink.clear()
        try:
            project = self.project.currentText()
            episodes = projectUtil.listEpisodes(project)
            i=0
            if episodes:
                for episode in episodes:
                    self.sgLink.addItem("")
                    self.sgLink.setItemText(i, QtGui.QApplication.translate("MainWindow", str(episode), None, QtGui.QApplication.UnicodeUTF8))
                    i = i+1
            if not episodes:
                self.sgLink.addItem("")
                self.sgLink.setItemText(0, QtGui.QApplication.translate("MainWindow", self.filmState, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.sgLink.addItem("")
            self.sgLink.setItemText(0, QtGui.QApplication.translate("MainWindow", self.filmState, None, QtGui.QApplication.UnicodeUTF8))

    def setFilm(self):
        project = self.project.currentText()
        episodes = projectUtil.listEpisodes(project)
        major = self.major.currentText()

        if episodes:
            if self.sgFilmLink in episodes:
                        index = episodes.index(self.sgFilmLink)
                        self.sgLink.setCurrentIndex(index)
            for s in episodes:
                if str(major) in s:
                    index = episodes.index(s)
                    self.sgLink.setCurrentIndex(index)

    def wrapIcons(self):
        if self.wrapIconsCheckbox.isChecked():
            self.listWidget.setResizeMode(QtGui.QListView.Adjust)
            self.listWidget.setViewMode(QtGui.QListView.IconMode)
        else:
            self.listWidget.setResizeMode(QtGui.QListView.Fixed)
            self.listWidget.setViewMode(QtGui.QListView.ListMode)

    def assetView(self):
        #Set Font
        font = QtGui.QFont()
        font.setPixelSize(15)
        font.PreferAntialias
        font.setWeight(63)

        path = projectUtil.listAssets(self.project.currentText(), self.major.currentText(), self.minor.currentText())
        self.assets = []
        assets = dsOsUtil.listFolder(str(path))
        i=0
        self.listWidget.clear()
        for asset in assets:
            if str(self.assetSearch.text()) in str(asset) or str(self.assetSearch.text()) == "":
                picPath = projectUtil.listAssetIcon(self.project.currentText(), self.major.currentText(), self.minor.currentText(), asset)

                if os.path.exists(picPath) == True:
                    item = QtGui.QListWidgetItem(self.listWidget)
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(picPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item.setIcon(icon)

                self.listWidget.item(i).setFont(font)
                self.listWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", asset, None, QtGui.QApplication.UnicodeUTF8))
                i=i+1
            dict = {"name":asset, "prj":str(self.project.currentText()), "major":str(self.major.currentText()), "minor":str(self.minor.currentText())}
            self.assets.append(dict)

    def bgColor(self):
        if not self.prj == str(self.project.currentText()):
            if not self.eps == str(self.major.currentText()):
                subAssetInDst = dsOsUtil.listFolder(projectUtil.listSubAssets(str(self.project.currentText()), str(self.major.currentText())))
                for subAsset in subAssetInDst:
                    for asset in dsOsUtil.listFolder(projectUtil.listAssets(str(self.project.currentText()), str(self.major.currentText()), subAsset)):
                        self.assetsInDst.append("%s/%s" % (projectUtil.listAssets(str(self.project.currentText()), str(self.major.currentText()), subAsset), asset))
                        self.prj = str(self.project.currentText())
                        self.eps = str(self.major.currentText())

        i = 0
        if pyVal == "PyQt":
            for asset in self.currentAssetList:
                src = "%s/%s" % (projectUtil.listAssets(str(self.project.currentText()) , str(self.major.currentText()), asset["subType"]), asset["name"])
                if src in self.assetsInDst:
                    self.modelList.item(i).setBackgroundColor(QtGui.QColor(0, 160, 0))
                    self.modelList.item(i).setTextColor(QtGui.QColor(0, 0, 0))
                    i = i + 1
                else:
                    self.modelList.item(i).setBackgroundColor(QtGui.QColor(0, 0, 0, 0))
                    self.modelList.item(i).setTextColor(QtGui.QColor(0, 0, 0))
                    i = i + 1

    def libMenuAction(self):
        if self.sender().text() == "Show Library": self.libraryShow.setChecked(self.actionShow_Library.isChecked())

    def libMenuShow(self):
        self.modelLibDock.setVisible(self.libraryShow.isChecked())
        self.modelLibFiltersDock.setVisible(self.libraryShow.isChecked())
        self.libraryFilters.setEnabled(self.libraryShow.isChecked())
        self.actionShow_Library.setChecked(self.libraryShow.isChecked())

        self.libFiltersMenuShow()

    def libFiltersMenuAction(self):
        if self.sender().text() == "Show Library Filters": self.libraryFilters.setChecked(self.actionShow_Library_Filters.isChecked())

    def libFiltersMenuShow(self):
        if self.libraryFilters.isEnabled():
            self.modelLibFiltersDock.setVisible(self.libraryFilters.isChecked())
            self.actionShow_Library_Filters.setChecked(self.libraryFilters.isChecked())
        else:
            self.modelLibFiltersDock.setVisible(False)
            self.actionShow_Library_Filters.setChecked(False)
        self.guiSize()

    def showProjectMenu(self):
        print self.actionShow_Project_Settings.isChecked()
        self.projectDock.setVisible(self.actionShow_Project_Settings.isChecked())

    def assetHandler(self):
        """GET ASSET INFO"""
        asset =  self.currentAssetList[self.modelList.currentRow()]

        """IF IT'S NOT A SHADER"""
        if not str(asset["type"]) == "shader":
            """CHECK THAT ALL SETTINGS ARE SET"""
            if "Select Project" in str(self.project.currentText()) or "Select Major" in str(self.major.currentText()) or "Select Minor" in str(self.major.currentText()):
                self.statusbar.showMessage("Please Set Project and Major")
            else:
                src = "%s/%s" % (asset["path"], asset["name"])
                dst = "%s/%s/" % (projectUtil.listAssets(self.project.currentText(), self.major.currentText(), self.minor.currentText()), asset["name"])
                #"""IF THE ASSET DOES NOT ALREADY EXIST, COPY IT"""
                if not os.path.exists("%s" % (dst)):
                    path = "%s" % (dst)
                    shutil.copytree(str(src), str(dst))
                    if str(dst).endswith("/"): dst = str(dst)[0:-1]
                    self.assetsInDst.append(str(dst))

                    """ADD TO SHOTGUN"""
                    try:
                        self.loadSG()
                        list = [["Asset", "sg_asset_type", str(asset["type"])],["Asset", "sg_subtype", str(asset["subType"])]]
                        sgBridge.addTypesToList(list)
                        assetID = sgBridge.sgCreateAsset(self.project.currentText(), str(asset["name"]), str(self.major.currentText()), str(self.minor.currentText()))
                        if os.path.exists(asset["iconPath"]):
                            sgBridge.sgCreateIcon(self.project.currentText(), str(asset["name"]), str(self.major.currentText()), str(self.minor.currentText()), asset["iconPath"])
                    except: pass
                else:
                    self.statusbar.showMessage("There's already an asset with that name present")
        else:
            self.statusbar.showMessage("This is a shader assign to selected instead?")

    def autoSetting(self):
        prj = None
        major = None
        D2D3 = 0
        if dsOsUtil.mayaRunning() == True:
            path = cmds.file(q=True, location=True)
            if "/dsPipe/" in path or "P:/" in path:
                if "/film/" in path:
                    if "dsPipe" in path: prj = path.split("/dsPipe/", 1)[-1].rsplit("/film/", 1)[0]
                    elif "P:/" in path: prj = path.split("P:/", 1)[-1].rsplit("/film/", 1)[0]
                    major = path.split("/film/", 1)[-1].split("/", 1)[0].rsplit("_", 1)[0]
                    D2D3 = 1
                elif "/asset/" in path:
                    if "dsPipe" in path: prj = path.split("/dsPipe/", 1)[-1].rsplit("/asset/", 1)[0]
                    elif "P:/" in path: prj = path.split("P:/", 1)[-1].rsplit("/asset/", 1)[0]

                    if "/asset/3D/" in path:
                        major = path.split("/asset/3D/", 1)[-1].split("/", 1)[0]
                        D2D3 = 1
                    if "/asset/2D/" in path:
                        major = path.split("/asset/2D/", 1)[-1].split("/", 1)[0]
                        D2D3 = 0

        if prj:
            self.project.setCurrentIndex(self.project.findText(prj))
        self.listMajors()
        if major:
            self.major.setCurrentIndex(self.major.findText(major))

    def listProjects(self):
        self.project.addItem("")
        self.project.setItemText(0, QtGui.QApplication.translate("MainWindow", "Select Project", None, QtGui.QApplication.UnicodeUTF8))

        if not self.listProjects == []:
            i = 1
            for prj in self.projects:
                self.project.addItem("")
                self.project.setItemText(i, QtGui.QApplication.translate("MainWindow", prj, None, QtGui.QApplication.UnicodeUTF8))
                i = i + 1

            if self.prjState:
                if self.prjState in self.projects:
                    index = self.projects.index(self.prjState) + 1
                    self.project.setCurrentIndex(index)


    def listMajors(self):
        path = projectUtil.listAssetTypes(str(self.project.currentText()))
        i = 0
        self.major.clear()
        majors = dsOsUtil.listFolder(path)
        if not majors:
            self.major.addItem("")
            self.major.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Major", None, QtGui.QApplication.UnicodeUTF8))
        else:
            for asset in majors:
                self.major.addItem("")
                self.major.setItemText(i, QtGui.QApplication.translate("MainWindow", asset, None, QtGui.QApplication.UnicodeUTF8))
                i = i + 1

        if self.mjrState:
                if self.mjrState in majors:
                    index = majors.index(self.mjrState)
                    self.major.setCurrentIndex(index)
        self.listMinor()

    def listMinor(self):
        path = projectUtil.listSubAssets(str(self.project.currentText()), self.major.currentText())
        assets = dsOsUtil.listFolder(str(path))
        if assets:
            i = 0
            self.minor.clear()
            for asset in assets:
                self.minor.addItem("")
                self.minor.setItemText(i, QtGui.QApplication.translate("MainWindow", asset, None, QtGui.QApplication.UnicodeUTF8))
                i = i + 1

        if self.minState:
                if self.minState in assets:
                    index = assets.index(self.minState)
                    self.minor.setCurrentIndex(index)

    def listAssets(self):
        """Check If View Is Enabled"""
        if self.libraryShow.isChecked():
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
        self.currentAssetList = []

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
                            if search == "Search":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                        elif subType == asset["subType"]:
                            if search == "Search":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                    elif type == asset["type"]:
                        if subType == "Select Sub Type":
                            if search == "Search":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                        elif subType == asset["subType"]:
                            if search == "Search":
                                self.addToList(asset, i)
                                i = i + 1
                            elif str(search) in str(asset["type"]) or str(search) in str(asset["subType"]) or str(search) in str(asset["name"]):
                                self.addToList(asset, i)
                                i = i + 1
                else:
                    if search == "Search":
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

        if not dsOsUtil.mayaRunning():
            self.assetExport.setEnabled(False)
            self.partExport.setEnabled(False)
            self.iconCreate.setEnabled(False)

    def addToList(self, asset, i):
        self.modelList.setResizeMode(QtGui.QListView.Adjust)
        self.modelList.setViewMode(QtGui.QListView.IconMode)
        font = QtGui.QFont()
        font.setPixelSize(15)
        font.PreferAntialias
        font.setWeight(63)

        self.currentAssetList.append(asset)

        if os.path.exists(asset["iconPath"]) == True:
            item = QtGui.QListWidgetItem(self.modelList)
            #Add Icon
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(asset["iconPath"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            self.modelList.item(i).setFont(font)
            self.modelList.item(i).setText(QtGui.QApplication.translate("modelLibUI", asset["name"], None, QtGui.QApplication.UnicodeUTF8))

    def iconUpdate(self, sliderName=None):
        if not sliderName == "assetIconSlider" and not sliderName == "iconSlider":
            if self.sender() == self.assetIconSlider:
                slider = self.assetIconSlider
                list =  self.listWidget
            else:
                slider = self.iconSlider
                list =  self.modelList
        else:
            if sliderName == "assetIconSlider":
                slider = self.assetIconSlider
                list =  self.listWidget
            elif sliderName == "iconSlider":
                slider = self.iconSlider
                list =  self.modelList

        percentage = float(slider.value())
        iconSize = [1280,720]
        list.setIconSize(QtCore.QSize(iconSize[0]*(percentage/100), iconSize[1]*(percentage/100)))

    def helpWiki(self):
        url = "http://vfx.duckling.dk/?page_id=935"
        new = 2
        webbrowser.open(url, new=new)

    def openAssetExplore(self):
        path =  "%s/%s/" % (projectUtil.listAssets(self.project.currentText(), self.major.currentText(), self.minor.currentText()), self.listWidget.currentItem().text())
        dsOsUtil.openInBrowser(path)

    def contexMenuHandler(self, menu, method, action, item):
        """GET FILE PATH"""
        if method == "dev":
            path = projectUtil.listAssetDevPath(self.project.currentText(), self.major.currentText(), self.minor.currentText(), self.listWidget.currentItem().text())
        if method == "publish":
            path = projectUtil.listAssetRefPath(self.project.currentText(), self.major.currentText(), self.minor.currentText(), self.listWidget.currentItem().text())

        """FILE THAT SHOULD BE OPENED"""
        mayaFile = "%s%s" % (path, item)
        print mayaFile

        """CHECK IF MAYA IS RUNNING"""
        if dsOsUtil.mayaRunning() == True:
            if action == "open":
                """IF ANY MODIFICATIONS MADE TO OPEN SCENE SAVE OR NOT?"""
                if cmds.file(q=True, anyModified=True) == True:
                    MyForm.saveConfirmDialog(self, mayaFile)
                else:
                    """IF NO MODS, JUST OPEN SCENE"""
                    cmds.file( mayaFile, o=True )
            if action == "ref":
                name = item.split("_")[0]
                cmds.file(mayaFile, r=True, namespace=str(name), options="v=0", shd="shadingNetworks")
            if action == "import":
                cmds.file(mayaFile, i=True )
        else:
            """IF NOT MAYA RUNNING, OPEN MAYA AND SCENE FILE"""
            os.system("maya.exe -file %s" % (mayaFile))

    def saveConfirmDialog(self, item):
        """SAVE SCENE YES, NO or CANCEL"""
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Want to to Save, before closing?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            cmds.file( save=True, type='mayaAscii' )
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File saved - File opened")
            mel.eval('print "File Saved - File Opened"')
        elif reply == QtGui.QMessageBox.No:
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File opened")
            mel.eval('print "File Opened: %s"' % item)
        else:
            self.ui.statusbar.showMessage("Open Scene Cancled")
            mel.eval('print "Cancled"')

    #----------------------------------------------------------CONTEX MENU START-----------------------------------------------------------------------
    def openMenu(self, position):
        selectedItem = self.listWidget.currentItem()
        if selectedItem:
            """GET DATA"""
            refPath = projectUtil.listAssetRefPath(self.project.currentText(), self.major.currentText(), self.minor.currentText(), selectedItem.text())
            devPath = projectUtil.listAssetDevPath(self.project.currentText(), self.major.currentText(), self.minor.currentText(), selectedItem.text())
            refs = dsOsUtil.listMb(refPath)
            devs = dsOsUtil.listMa(devPath)

            """Set Menu"""
            menu = QtGui.QMenu()
            openMenu = QtGui.QMenu("Open")

            """Task Menu's"""
            openMenu = QtGui.QMenu("Open")
            refMenu = QtGui.QMenu("Ref")
            importMenu = QtGui.QMenu("Import")
            publishFilesRef = QtGui.QMenu("Ref Publish")
            publishFilesImport = QtGui.QMenu("Import Publish")

            """Add Menu's"""
            if devs:
                for item in devs:
                    menu.addMenu(openMenu)
                    if dsOsUtil.mayaRunning():
                        menu.addMenu(refMenu)
                        menu.addMenu(importMenu)
                    menu.addSeparator()

                    self.connect(openMenu.addAction(item) ,QtCore.SIGNAL('triggered()'), lambda item=item: self.contexMenuHandler(openMenu, "dev", "open", item))
                    if dsOsUtil.mayaRunning():
                        self.connect(refMenu.addAction(item) ,QtCore.SIGNAL('triggered()'), lambda item=item: self.contexMenuHandler(openMenu, "dev", "ref", item))
                        self.connect(importMenu.addAction(item) ,QtCore.SIGNAL('triggered()'), lambda item=item: self.contexMenuHandler(openMenu, "dev", "import", item))
            if dsOsUtil.mayaRunning():
                if refs:
                    for item in refs:
                        menu.addMenu(publishFilesRef)
                        menu.addMenu(publishFilesImport)
                        menu.addSeparator()

                        self.connect(publishFilesRef.addAction(item) ,QtCore.SIGNAL('triggered()'), lambda item=item: self.contexMenuHandler(openMenu, "publish", "ref",item))
                        self.connect(publishFilesImport.addAction(item) ,QtCore.SIGNAL('triggered()'), lambda item=item: self.contexMenuHandler(openMenu, "publish", "import",item))

            """Add Actions"""
            exploreAction = menu.addAction("Open in Explore")
            self.connect(exploreAction,QtCore.SIGNAL('triggered()'),lambda item=[]: self.openAssetExplore())

            quitAction = menu.addAction("Quit")
            self.connect(quitAction,QtCore.SIGNAL('triggered()'),lambda item=[]: self.exitWidget())

            """Open Contex Menu"""
            menu.exec_(QtGui.QCursor.pos())
    #----------------------------------------------------------CONTEX MENU END-----------------------------------------------------------------------

    #----------------------------------------------------------SHOTGUN DEFS START-----------------------------------------------------------------------
    def loadSG(self):
        if not self.sgLoaded:
            import dsSgUtil as sgBridge
            global sgBridge
            self.sgLoaded = True

    def loadSgBridge(self):
        if self.sgLoaded == 0:
            try:
                print "LOADING BRIDGE"
                self.sgLoaded = 1
                import dsSgUtil as sgBridge
                global sgBridge
            except:
                print "NOT LOADING LOADING BRIDGE"
                self.sgLoaded = 1

    def reloadAssetStatus(self):
        self.loadSgBridge()
        global sgBridge
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

    def setShotgunStatus(self, assetName, status):
        self.loadSgBridge()
        global sgBridge
        project = self.ui.productionComboBox.currentText()
        assetType = self.ui.assetTypeComboBox.currentText()
        assetSubType = self.ui.assetSubTypeComboBox.currentText()

        assetID = sgBridge.sgGetAssetID(project, assetName, assetType, assetSubType)
        sgBridge.sgSetAssetStatus(assetID, status)
        self.reloadAssetStatus()

    def listTemplates(self):
        self.loadSgBridge()
        global sgBridge
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
        self.sgTemplate.clear()
        added = []
        i=0
        if templates:
            for plate in templates:
                if not "Shot" in plate["code"]:
                        if not "Sequence" in plate["code"]:
                                if not "Comp" in plate["code"]:
                                    self.sgTemplate.addItem("")
                                    text = "%s ID:%s" % (plate["code"], plate["id"])
                                    self.sgTemplate.setItemText(i, QtGui.QApplication.translate("MainWindow", text, None, QtGui.QApplication.UnicodeUTF8))
                                    added.append(text)
                                    i = i+1
            if self.sgTemp:
                if self.sgTemp in added:
                    index = added.index(self.sgTemp)
                self.sgTemplate.setCurrentIndex(index)
    #-------------------------------------------------------------SHOTGUN DEFS ENDS--------------------------------------------------------------------------

    #----------------------------------------------------------GUI SETTING DEFS STARTS-----------------------------------------------------------------------
    def closeEvent(self, event):
        self.writeSettings()

    def exitWidget(self):
        if dsOsUtil.mayaRunning() == True:
            global dsModelLibWindow
            dsModelLibWindow.close()
        else:
            self.close()

    def writeSettings(self):
        '''Write settings'''
        settings = QtCore.QSettings("Duckling&Sonne", "Asset Tool UI v2.0")

        #Asset Settings
        settings.setValue("prjState", self.project.currentText())
        settings.setValue("majorState", self.major.currentText())
        settings.setValue("minorState", self.minor.currentText())
        settings.setValue("link", self.sgLink.currentText())
        settings.setValue("sgTemplateLoad", str(self.loadedTemplates))
        settings.setValue("sgTemplate", self.sgTemplate.currentText())

        #GUI Settings
        settings.setValue("showLib", self.libraryShow.isChecked())
        settings.setValue("showLibFilters", self.libraryShow.isChecked())
        settings.setValue("icons", self.iconCheck.isChecked())
        settings.setValue("wrap", self.wrapIconsCheckbox.isChecked())

        settings.setValue("assetIconSlider", self.assetIconSlider.value())
        settings.setValue("iconSlider", self.iconSlider.value())

    def readSettings(self):
        '''Read application settings from the QT Settings object.'''
        settings = QtCore.QSettings("Duckling&Sonne", "Asset Tool UI v2.0")
        #Asset Settings
        self.prjState = settings.value("prjState").toString()
        self.mjrState = settings.value("majorState").toString()
        self.minState = settings.value("minorState").toString()
        self.sgFilmLink = settings.value("link").toString()
        self.sgTemp = settings.value("sgTemplate").toString()

        temp = eval(str(settings.value("sgTemplateLoad").toString()))
        self.sgTempLoad = []
        for t in temp: self.sgTempLoad.append(t)

        #GUI Settings READ
        self.libraryShow.setChecked(settings.value("showLib").toBool())
        self.actionShow_Library.setChecked(settings.value("showLib").toBool())
        self.libraryFilters.setChecked(settings.value("showLibFilters").toBool())
        self.actionShow_Library_Filters.setChecked(settings.value("showLibFilters").toBool())

        self.iconCheck.setChecked(settings.value("icons").toBool())
        self.wrapIconsCheckbox.setChecked(settings.value("wrap").toBool())

        self.assetIconSlider.setValue(int(settings.value("assetIconSlider").toString()))
        self.iconSlider.setValue(int(settings.value("iconSlider").toString()))

    #----------------------------------------------------------GUI SETTING DEFS ENDS-----------------------------------------------------------------------

#IF not runned inside Maya
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

def UI():
    global dsModelLibWindow
    try:
        dsModelLibWindow.close()
    except:
        pass
    dsModelLibWindow = MyForm()
    dsModelLibWindow.show()