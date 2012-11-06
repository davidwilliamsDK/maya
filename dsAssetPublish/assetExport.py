import sys, os, re, shutil, random, sip
import common.osUtil as osUtil
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from exportAssetUI import Ui_exportAsset
import exportAssetUI

import aiPipeline.aiConfig as aiConfig
assetPath = aiConfig.expandSetting("ai_ProductionAssetsPaths")

if osUtil.mayaRunning() == True:
    import maya.cmds as cmds
    #import maya.mel as mel
    import maya.OpenMayaUI as mui

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
        if cmds.objExists("Root_Group"):
            self.ui.root = "Root_Group"
        elif cmds.objExists("Rig:Root_Group"):
            self.ui.root = "Rig:Root_Group"
        self.ui.aiSubAssets = "aiSubAssets"
        self.ui.aiProxies = "aiProxies"

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
        rootNodeName = "Root_Group.aiNodeName"
        rootNodeNameRef = "*:Root_Group.aiNodeName"
        if cmds.objExists(rootNodeName) or cmds.objExists(rootNodeNameRef):
            if cmds.objExists(rootNodeName):
                aiConfig.settings["ai_AssetName"] = cmds.getAttr(rootNodeName)
            elif cmds.objExists(rootNodeNameRef):
                aiConfig.settings["ai_AssetName"] = cmds.getAttr(rootNodeNameRef)
            assetName = aiConfig.settings["ai_AssetName"]

            subAssetList = None
            proxyList = None
            filePath = cmds.file(q=True, sn=True)

            #check that the asset is set correct!
            assetPath =  aiConfig.expandSetting("ai_AssetPath")

            if assetPath in filePath:
                refPath = aiConfig.expandSetting("ai_AssetRefPath")

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

                assetExportForm.exportBatch(self, filePath, refPath, subAssetList, proxyList, assetName)
            else:
                print "the asset might not have the right attributes or naming "
        else:
            print "there's no valid 'Root_Ctrl' in the scene"

    def exportBatch(self, filePath, refPath, subAssets=None, proxies=None, assetName=None):
        logFolder = "_Log"
        tmpFile = ("/_%s_%s" % (assetName, "export_tmp.ma"))
        path = filePath.rsplit("/", 1)[0]
        print path

        cmds.file( save=True, type='mayaAscii' )

        shutil.copy(filePath, ("%s%s" % (path, tmpFile)))

        if not os.path.exists(("%s/%s" % (refPath, logFolder))):
            os.mkdir(("%s/%s" % (refPath, logFolder)))

        logFolder = ("%s/%s" % (refPath, logFolder))
        print logFolder

        #If subAssets export
        if subAssets:
            for subAsset in subAssets:
                if ":" in subAsset:
                        subAsset = subAsset.rsplit(":")[-1]
                if proxies:
                    for proxy in proxies:
                        if ":" in proxy:
                            proxy = proxy.rsplit(":")[-1]
                        melCmd = ('source exportBatch; exportBatchProcedures "%s" "%s" "%s";' % (subAsset, proxy, refPath))
                        os.system("maya -batch -log '%s\%s_%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, subAsset, proxy, melCmd, path, tmpFile))
                else:
                    melCmd = ('source exportBatch; exportBatchProcedures "%s" "%s" "%s";' % (subAsset, proxies, refPath))
                    os.system("maya -batch -log '%s\%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, subAsset, melCmd, path, tmpFile))
            else:
                pass
            pass


        #If no subAssets Export Proxies
        if not subAssets:
            if proxies:
                for proxy in proxies:
                    if ":" in proxy:
                        proxy = proxy.rsplit(":")[-1]
                    melCmd = ('source exportBatch; exportBatchProcedures "%s" "%s" "%s";' % (subAssets, proxy, refPath))
                    os.system("maya -batch -log '%s\%s_log.txt' -command '%s' -file '%s%s'" % (logFolder, proxy, melCmd, path, tmpFile))
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
    if cmds.objExists("Root_Group") or cmds.objExists("*:Root_Group"):
        global exportAssetForm
        exportAssetForm = assetExportForm(getMayaWindow())
        exportAssetForm.show()
    else:
        cmds.error('This is not a Valid scene. File has to contain a "Root_Group" with all of it\'s c tume attributes')