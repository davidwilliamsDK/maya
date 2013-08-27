#Import Python Modules
import sys, os, re, shutil, random, sip

#Import Custome Modules
import dsCommon.dsOsUtil as osUtil
import dsCommon.dsProjectUtil as dsProjectUtil

#Import PyQt Modules
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Import UI
from dsPublishAssetUI import Ui_exportAsset
import dsPublishAssetUI
reload(dsPublishAssetUI)

#If maya is running import Maya cmds
if osUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

#If Maya is running, get the Maya UI
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

class assetExportForm(QtGui.QMainWindow):
    '''
    '''
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_exportAsset()
        self.ui.setupUi(self)

        #Setup vars
        if cmds.objExists("Rig_Grp"):
            self.ui.root = "Rig_Grp"
        elif cmds.objExists("Rig:Rig_Grp"):
            self.ui.root = "Rig:Rig_Grp"
        self.ui.aiSubAssets = "subAssets"
        self.ui.aiProxies = "proxies"

        #Update UI
        assetExportForm.subAssetListUpdate(self)
        assetExportForm.proxyListUpdate(self)

        #Create Action signals
        QtCore.QObject.connect(self.ui.updateListsPushButton, QtCore.SIGNAL("clicked()"), self.subAssetListUpdate)
        QtCore.QObject.connect(self.ui.updateListsPushButton, QtCore.SIGNAL("clicked()"), self.proxyListUpdate)

        QtCore.QObject.connect(self.ui.assetExportPushButton, QtCore.SIGNAL("clicked()"), self.exportAssetHandler)

        QtCore.QObject.connect(self.ui.subAssetListWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.subAssetSelUpdate)
        QtCore.QObject.connect(self.ui.proxyListWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.proxySelUpdate)

    def exportAssetHandler(self):
        curFile = cmds.file(q=True, l=True)[0]
        rootNodeName = "|Rig_Grp.assetName"
        rootNodeNameRef = "*:Rig_Grp.assetName"
##        referencePath = "/ref/"
##        devPath = "/dev/"
        referencePath = dsProjectUtil.listRefPath()
        devPath = dsProjectUtil.listDevPath()

        #Check if this Asset have a name
        if cmds.objExists(rootNodeName) or cmds.objExists(rootNodeNameRef):
            if cmds.objExists(rootNodeName):
                assetName = cmds.getAttr(rootNodeName)
            elif cmds.objExists(rootNodeNameRef):
                refRoots = cmds.ls(rootNodeNameRef)
                if len(refRoots) is 1:
                    assetName = cmds.getAttr(rootNodeNameRef)
                elif len(refRoots) is not 1:
                    print "woooop"
                    for r in refRoots:
                        if cmds.getAttr(r) in cmds.file(q=True, sceneName=True):
                            print cmds.getAttr(r)
                            print cmds.file(q=True, sceneName=True)
                            assetName = cmds.getAttr(r)

            if assetName in curFile:
                subAssetList = None
                proxyList = None
                filePath = cmds.file(q=True, sn=True)

                #check that the asset is set correct!
                refPath =  (curFile.split(devPath, -1)[0] + referencePath)

                subAssetSets = self.ui.subAssetListWidget.selectedItems()
                if subAssetSets:
                    subAssetList = []
                    for subAssetSet in subAssetSets:
                        item = str(subAssetSet.text())
                        subAssetList.append(item)

                proxySets = self.ui.proxyListWidget.selectedItems()
                if proxySets:
                    proxyList = []
                    for proxySet in proxySets:
                        item = str(proxySet.text())
                        proxyList.append(item)

                tiledEXR = self.ui.iconCheckBox.isChecked()
                assetExportForm.exportBatch(self, filePath, refPath, subAssetList, proxyList, assetName, tiledEXR)
            else:
                print "the asset might not have the right attributes or naming "
        else:
            print "there's no valid 'Root_Ctrl' in the scene"

    def exportBatch(self, filePath, refPath, subAssets=None, proxies=None, assetName=None, tiledEXR="False"):
        print "####################################################"
        print tiledEXR
        vrayID = 1
        logFolder = "_Log"
        versions = "versions"
        tmpFile = ("/_%s_%s" % (assetName, "export_tmp.ma"))
        path = filePath.rsplit("/", 1)[0]

        cmds.file( save=True, type='mayaAscii' )

        shutil.copy(filePath, ("%s%s" % (path, tmpFile)))

        if not os.path.exists(("%s/%s" % (refPath, logFolder))):
            os.mkdir(("%s/%s" % (refPath, logFolder)))

        if not os.path.exists(("%s/%s" % (refPath, versions))):
            os.mkdir(("%s/%s" % (refPath, versions)))

        logFolder = ("%s/%s" % (refPath, logFolder))

        #If subAssets export
        if subAssets:
            for subAsset in subAssets:
                if ":" in subAsset:
                        subAsset = subAsset.rsplit(":")[-1]
                if proxies:
                    for proxy in proxies:
                        if ":" in proxy:
                            proxy = proxy.rsplit(":")[-1]
                        melCmd = ('source publishAssetBatch; exportBatchProcedures "%s" "%s" "%s" "%s" "%s";' % (subAsset, proxy, refPath, vrayID, tiledEXR))
                        if str(osUtil.listOS()) == "Linux":
                            os.system("maya -batch -command '%s' -file '%s%s'" % (melCmd, path, tmpFile))
                        if str(osUtil.listOS()) == "Windows":
                            os.system("maya -batch -log '%s/%s_%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, subAsset, proxy, melCmd, path, tmpFile))
                else:
                    melCmd = ('source publishAssetBatch; exportBatchProcedures "%s" "%s" "%s" "%s" "%s";' % (subAsset, proxies, refPath, vrayID, tiledEXR))
                    if str(osUtil.listOS()) == "Linux":
                        os.system("maya -batch -command '%s' -file '%s%s'" % (melCmd, path, tmpFile))
                    if str(osUtil.listOS()) == "Windows":
                        os.system("maya -batch -log '%s/%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, subAsset, melCmd, path, tmpFile))
            else:
                pass
            pass


        #If no subAssets Export Proxies
        if not subAssets:
            if proxies:
                for proxy in proxies:
                    if ":" in proxy:
                        proxy = proxy.rsplit(":")[-1]

                    melCmd = ('source publishAssetBatch; exportBatchProcedures "%s" "%s" "%s" "%s" "%s";' % (subAssets, proxy, refPath, vrayID, tiledEXR))
                    if str(osUtil.listOS()) == "Linux":
                        os.system("maya -batch -command '%s' -file '%s%s'" % (melCmd, path, tmpFile))
                    if str(osUtil.listOS()) == "Windows":
                        os.system("maya -batch -log '%s/%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, proxy, melCmd, path, tmpFile))
            else:
                print "No files to export"

        os.remove("%s%s" % (path, tmpFile))

    def subAssetSelUpdate(self):
        if self.ui.subAssetListWidget.currentItem().text() == "None":
            self.ui.subAssetListWidget.setItemSelected(self.ui.subAssetListWidget.currentItem(), True)

            subAssetSets = self.ui.subAssetListWidget.selectedItems()
            for subAssetSet in subAssetSets:
                if not subAssetSet.text() == "None":
                    self.ui.subAssetListWidget.setItemSelected(subAssetSet, False)
        else:
            subAssetSets = self.ui.subAssetListWidget.selectedItems()
            for subAssetSet in subAssetSets:
                if subAssetSet.text() == "None":
                    self.ui.subAssetListWidget.setItemSelected(subAssetSet, False)
                if  subAssetSet.text() == "":
                    self.ui.subAssetListWidget.setItemSelected(subAssetSet, False)


    def proxySelUpdate(self):
        if self.ui.proxyListWidget.currentItem().text() == "None":
            self.ui.proxyListWidget.setItemSelected(self.ui.proxyListWidget.currentItem(), True)

            subAssetSets = self.ui.proxyListWidget.selectedItems()
            for proxySet in subAssetSets:
                if not proxySet.text() == "None":
                    self.ui.proxyListWidget.setItemSelected(proxySet, False)
        else:
            subAssetSets = self.ui.proxyListWidget.selectedItems()
            for proxySet in subAssetSets:
                if proxySet.text() == "None":
                    self.ui.proxyListWidget.setItemSelected(proxySet, False)
                if  proxySet.text() == "":
                    self.ui.proxyListWidget.setItemSelected(proxySet, False)


    def subAssetListUpdate(self):
        i=1
        if cmds.objExists("%s.%s" % (self.ui.root, self.ui.aiSubAssets)):
            subAssetSets = cmds.listConnections("%s.%s" % (self.ui.root, self.ui.aiSubAssets))

            if subAssetSets:
                QtGui.QListWidgetItem(self.ui.subAssetListWidget)
                self.ui.subAssetListWidget.item(0).setText(QtGui.QApplication.translate("SubAssetWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
                for item in subAssetSets:
                    QtGui.QListWidgetItem(self.ui.subAssetListWidget)
                    self.ui.subAssetListWidget.item(i).setText(QtGui.QApplication.translate("SubAssetWindow", str(item), None, QtGui.QApplication.UnicodeUTF8))
                    i=i+1


    def proxyListUpdate(self):
        i=1
        if cmds.objExists("%s.%s" % (self.ui.root, self.ui.aiProxies)):
            proxySets = cmds.listConnections("%s.%s" % (self.ui.root, self.ui.aiProxies))

            if proxySets:
                QtGui.QListWidgetItem(self.ui.proxyListWidget)
                self.ui.proxyListWidget.item(0).setText(QtGui.QApplication.translate("SubAssetWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
                for item in proxySets:
                    QtGui.QListWidgetItem(self.ui.proxyListWidget)
                    self.ui.proxyListWidget.item(i).setText(QtGui.QApplication.translate("SubAssetWindow", str(item), None, QtGui.QApplication.UnicodeUTF8))
                    i=i+1

def UI():
    if cmds.objExists("Rig_Grp") or cmds.objExists("*:Rig_Grp"):
        global exportAssetForm
        exportAssetForm = assetExportForm(getMayaWindow())
        exportAssetForm.show()
    else:
        cmds.error('This is not a Valid scene. File has to contain a "Root_Group" with all of it\'s c tume attributes')