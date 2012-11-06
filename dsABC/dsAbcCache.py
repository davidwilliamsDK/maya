#Importing Modules
import sys, os, sip
from PyQt4 import QtGui, QtCore, uic
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)
import dsCommon.dsReferenceCMD as refUtil
import dsABC.dsAbcConnect as abcConnect
reload(abcConnect)
import dsCommon.dsOsUtil as dsOsUtil
import maya.mel as mel

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsABC/abc.ui'
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsABC/abc.ui'
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsABC/abc.ui'

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

#Importing maya UI
try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
except:
    pass

abcCachePath = projectUtil.abcCachePath()

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    ptr = long(ptr)
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class dsAbcCache(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
##        base_class.__init__(self, parent=getMayaWindow())

        self.setupUi(self)

        self.cachePushButton.clicked.connect(self.handler)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionExit.triggered.connect(self.exitWidget)

        self.listCams()
        self.listAsset()

        self.newRef = ""
        self.swoprefState = True
        self.shotlevelState = False

        try:
            self.readSettings()
        except:
            print "Read setting fucked up"

    def listShots(self):
        camSeq = None
        try:
            camSeq = cmds.ls(type="sequencer")[0]
        except:
            print "No Camera Sequencer Present"
        if camSeq:
            return cmds.listConnections(camSeq + ".shots")
        else: return None

    def startEndFrame(self, shot, start=True):
        if start:
            return cmds.getAttr(shot + ".startFrame")
        else:
            return cmds.getAttr(shot + ".endFrame")

    def listCams(self):
        shots = self.listShots()
        if shots:
            for shot in shots:
                start = self.startEndFrame(shot)
                end = self.startEndFrame(shot, False)

                add = ("%s_%s_%s") % (shot, start, end)
                item = QtGui.QListWidgetItem(add)
                self.camListWidget.addItem(item)

    def fullSeqLengt(self):
        shots = self.listShots()
        start = int(self.startEndFrame(shots[0]))
        end = int(self.startEndFrame(shots[0], False))
        for shot in shots:
            x = int(self.startEndFrame(shot))
            y = int(self.startEndFrame(shot, False))
            if x < start:
                start=x
            if y > end:
                end = y
        return start, end

    def getAssets(self):
        fullname = cmds.ls("*:Rig_Grp")
        nicename = []
        for name in fullname:
            nicename.append(name.split(":",1)[0])
        return nicename

    def abcFileExists(self, asset, returnPath=False):
        assetType = cmds.getAttr(str(asset + ":Rig_Grp.assetType"))
        assetSubType = cmds.getAttr(str(asset + ":Rig_Grp.assetSubType"))
        assetName = cmds.getAttr(str(asset + ":Rig_Grp.assetName"))
        project = cmds.getAttr(str(asset + ":Rig_Grp.project"))

        refPath = projectUtil.listAssetRefPath(project, assetType, assetSubType, assetName)
        abcfile = ("%s/%s_ABC.mb") % (refPath, assetName)

        print os.path.exists(abcfile)
        if os.path.exists(abcfile):
            if returnPath:
                return abcfile
            else:
                return True
        else:
            print "path doesn't exist: %s" % abcfile
            return False

    def listAsset(self):
        self.assetListWidget.clear()
        assets = self.getAssets()
        for asset in assets:
            ref = self.abcFileExists(asset)
            cached = self.abcCached(asset)
            item = QtGui.QListWidgetItem(asset)
            item.setTextColor(QtGui.QColor(0, 0, 0))
            if ref:
                if cached:
                    item.setBackgroundColor(QtGui.QColor(255, 0, 0))
                    item.setWhatsThis("False")
                else:
                    item.setBackgroundColor(QtGui.QColor(0, 255, 0))
                    item.setWhatsThis("True")
            else:
                item.setBackgroundColor(QtGui.QColor(255, 0, 0))
                item.setWhatsThis("False")
            self.assetListWidget.addItem(item)

    def abcCached(self, asset):
        meshes = cmds.ls(asset + ":mesh_*")
        if meshes:
            for mesh in meshes:
                shapes = cmds.listRelatives(mesh, c=True, fullPath=True)
                if shapes:
                    for shape in shapes:
                        connect = cmds.listConnections(shape, d=True, s=True)
                        alembic = cmds.ls(connect, type="AlembicNode")
                        if alembic:
                            return True

    def cache(self, startframe, endframe, asset, output):
        cmds.select(str(asset.text() + ":mesh_*"))
        geo = cmds.ls(sl=True, type="transform", l=True)

        meshData = ""
        for g in geo:
            try:
                if cmds.listRelatives(g, c=True, type="mesh")[0]:
                    meshData = '%s -root %s' % (meshData, g)
            except:
                pass
                #print g
        if not os.path.exists(output.rsplit("/",1)[0]):
            os.mkdir(output.rsplit("/",1)[0])
        mel.eval('AbcExport -j "-fr %s %s -uvWrite -worldSpace -writeVisibility%s -file %s"' % (startframe, endframe, meshData, output))

    def refABC(self, asset, nameSpace):
        #get path to ABC ref file
        abc = self.abcFileExists(asset, True)

        #unload ref
        refNode = refUtil.listCurrentProxy("%s:Rig_Grp" % asset)
        cmds.file(unloadReference=refNode)

        #Create ref
        if cmds.objExists("%s:Rig_Grp" % nameSpace):
            print "Ref Exists"
        oldNode = cmds.ls(type="transform", rn=True, assemblies=True)
        cmds.file(abc, r=True, type="mayaBinary", gl=True, loadReferenceDepth="all", namespace=nameSpace, options="v=0")
        newNode = cmds.ls(type="transform", rn=True, assemblies=True)
        baseRefName = list(set(newNode)-set(oldNode))[0].split(":",1)[0]
        newRef = baseRefName + ":Rig_Grp"
        if not cmds.objExists("ABC"):
            cmds.group(em=True, name="ABC")
        cmds.parent(newRef, "ABC")

        return refUtil.listCurrentProxy(newRef), baseRefName

    def importABC(self, asset, refNode, input):
        #import ABC Cache
        newRef=refNode[1]
        oldAbcNodes = cmds.ls(type="AlembicNode")
        oldGeo = cmds.ls(type="mesh", long=True)
        mel.eval('AbcImport -mode import "%s"' % input)
        newGeo = cmds.ls(type="mesh", long=True)
        newAbcNodes = cmds.ls(type="AlembicNode")

        abcNode = list(set(newAbcNodes)-set(oldAbcNodes))
        abcTempGeo = cmds.listConnections(abcNode[0], s=False, d=True)

        #Connect abc to geo
        abcConnect.connectSkins(abcNode[0], newRef)
        abcConnect.connectTrans(abcNode[0], newRef)
        cmds.listConnections(abcNode, s=False, d=True)

        #cleanup
        tempGeoShapes = list(set(newGeo)-set(oldGeo))
        tempGeo = cmds.listRelatives(tempGeoShapes, p=True)
        self.cleanUpAbc(tempGeo)


    def cleanUpAbc(self, geo):
        for g in geo:
            if not "unitConversion" in g:
                try:
                    cmds.delete(g)
                except:
                    pass

    def handler(self):
        '''Main def, for abc caching'''
##        shotLevel = self.shotLevel_checkBox.isChecked()
        shotLevel = False

        #list assets and shots
        shots = self.camListWidget.selectedItems()
        assets = self.assetListWidget.selectedItems()
        path = cmds.file(q=True, l=True)[0].rsplit("/",3)

        #Create Cache
        if not shots==[]:
            if not assets==[]:
                #Cache one file per shot and per asset
                if shotLevel:
                    for shot in shots:
                        for asset in assets:
                            if asset.whatsThis() == "True":
                                info = shot.text().split("_")
                                output = "%s/%s/%s/%s_%s_%s.abc" % (path[0], path[1], abcCachePath, path[1], info[0], asset.text())
                                self.cache(info[1], info[2], asset, output)
                                if self.swopref_checkBox.isChecked():
                                    refNode = self.refABC(asset.text())
                                    self.importABC(asset, refNode, output)

                #Cache one file per asset
                if not shotLevel:
                    framerange = self.fullSeqLengt()
                    for asset in assets:
                        print asset.whatsThis()
                        if asset.whatsThis() == "True":
                            output = "%s/%s/%s/%s_%s.abc" % (path[0], path[1], abcCachePath, path[1], asset.text())
                            self.cache(framerange[0], framerange[1], asset, output)
                            if self.swopref_checkBox.isChecked():
                                refNode = self.refABC(asset.text(), output.rsplit("/",1)[-1].rsplit(".",1)[0])
                                self.importABC(asset, refNode, output)
                        else:
                            print asset.text() + "  Skipped"
        else:
            print "PLEASE SELECT A SHOT"

        #Reload UI
        self.listAsset()

    def readSettings(self):
        '''Read application settings from the QT Settings object.'''
        settings = QtCore.QSettings("Duckling&Sonne", "abcCache")
        self.swoprefState = settings.value("swoprefState").toBool()
        self.swopref_checkBox.setChecked(self.swoprefState)
        self.shotlevelState = settings.value("shotlevelState").toBool()
        self.shotLevel_checkBox.setChecked(self.shotlevelState)

    def writeSettings(self):
        '''Write settings'''
        settings = QtCore.QSettings("Duckling&Sonne", "abcCache")
        settings.setValue("swoprefState", self.swopref_checkBox.isChecked())
        settings.setValue("shotlevelState", self.shotLevel_checkBox.isChecked())

    def closeEvent(self, event):
        self.writeSettings()

    def exitWidget(self):
        if dsOsUtil.mayaRunning() == True:
            global myWindow
            mel.eval('print "dsCache Dialog closed"')
            myWindow.close()
        else:
            self.close()

def dsABC():
    global myWindow
    myWindow = dsAbcCache()
    myWindow.show()