#Import Python Modules
import sys, os, re, shutil, random, sip
import dsCommon.dsOsUtil as osUtil

#Import PyQt Modeules
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from dsPublishSetsUI import Ui_dsPublishSetsGUI
try:
    reload(dsPublishSetsUI)
except:
    pass
import dsPublishSetsUI

#Check if runned inside Maya
if osUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

#If inside Maya, get Maya Window
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

#Variables
subAssetMessageAttr = "subAssets"
proxyMessageAttr = "proxies"

class MyForm(QtGui.QMainWindow):
    '''
    '''
    def __init__(self, parent=None):
        #Var
        global oldPanel
        oldPanel = None

        #Setup Window
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_dsPublishSetsGUI()
        self.ui.setupUi(self)

        #Init definitions to update UI
        MyForm.listSubSets(self)
        MyForm.listProxySets(self)
        MyForm.isolateView(self)


        #Create Action signals
        QtCore.QObject.connect(self.ui.createSubAssetPushButton, QtCore.SIGNAL("clicked()"), self.createSubSetUI)
        QtCore.QObject.connect(self.ui.createProxyPushButton, QtCore.SIGNAL("clicked()"), self.createProxySetUI)

        QtCore.QObject.connect(self.ui.removeSubAssetPushButton, QtCore.SIGNAL("clicked()"), self.removeSubSetUI)
        QtCore.QObject.connect(self.ui.removeProxyPushButton, QtCore.SIGNAL("clicked()"), self.removeProxySetUI)

        QtCore.QObject.connect(self.ui.addSelSubAssetPushButton, QtCore.SIGNAL("clicked()"), self.addSubSetToSet)
        QtCore.QObject.connect(self.ui.addSelProxyPushButton, QtCore.SIGNAL("clicked()"), self.addProxyToSet)

        QtCore.QObject.connect(self.ui.removeSelSubAssetPushButton, QtCore.SIGNAL("clicked()"), self.removeSubSetFromSet)
        QtCore.QObject.connect(self.ui.removeSelProxyPushButton, QtCore.SIGNAL("clicked()"), self.removeProxyFromSet)

        QtCore.QObject.connect(self.ui.isolateViewCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.isolateView)
        QtCore.QObject.connect(self.ui.subAssetListWidget, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.isolateView)
        QtCore.QObject.connect(self.ui.proxyListWidget, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *,QListWidgetItem *)"), self.isolateView)

        QtCore.QObject.connect(self.ui.actionExit, QtCore.SIGNAL("activated(int)"), self.close);
        QtCore.QObject.connect(self.ui.actionIsolateView, QtCore.SIGNAL("activated(int)"), self.toggleIsolate);
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("activated(int)"), self.aboutMenu);

        #Set Default Vars
        self.defaultSetState = "Select Default Set"
        self.proxySets = ["Blocking", "Proxy", "Anim", "Render", "Cache"]
        self.subAssetSets = ["FG", "BG"]


    def listSubSets(self):
        if cmds.objExists("Rig_Grp"):
            root = "|Rig_Grp"
        elif cmds.objExists("Rig:Rig_Grp"):
            root = "Rig:Rig_Grp"

        self.ui.subAssetListWidget.clear()
        i=1

        if cmds.objExists("%s.%s" % (root, subAssetMessageAttr)):
            proxySets = cmds.listConnections("%s.%s" % (root, subAssetMessageAttr))

            if proxySets:
                QtGui.QListWidgetItem(self.ui.subAssetListWidget)
                self.ui.subAssetListWidget.item(0).setText(QtGui.QApplication.translate("SubAssetWindow", "Show All", None, QtGui.QApplication.UnicodeUTF8))
                for item in proxySets:
                    QtGui.QListWidgetItem(self.ui.subAssetListWidget)
                    self.ui.subAssetListWidget.item(i).setText(QtGui.QApplication.translate("SubAssetWindow", str(item), None, QtGui.QApplication.UnicodeUTF8))
                    i=i+1

    def listProxySets(self):
        if cmds.objExists("Rig_Grp"):
            root = "Rig_Grp"
        elif cmds.objExists("Rig:Rig_Grp"):
            root = "Rig:Rig_Grp"

        self.ui.proxyListWidget.clear()
        i=1

        if cmds.objExists("%s.%s" % (root, proxyMessageAttr)):
            proxySets = cmds.listConnections("%s.%s" % (root, proxyMessageAttr))

            if proxySets:
                QtGui.QListWidgetItem(self.ui.proxyListWidget)
                self.ui.proxyListWidget.item(0).setText(QtGui.QApplication.translate("SubAssetWindow", "Show All", None, QtGui.QApplication.UnicodeUTF8))
                for item in proxySets:
                    QtGui.QListWidgetItem(self.ui.proxyListWidget)
                    self.ui.proxyListWidget.item(i).setText(QtGui.QApplication.translate("SubAssetWindow", str(item), None, QtGui.QApplication.UnicodeUTF8))
                    i=i+1

    def toggleIsolate(self):
        if self.ui.isolateViewCheckBox.isChecked():
            self.ui.isolateViewCheckBox.setChecked(False)
        else:
            self.ui.isolateViewCheckBox.setChecked(True)

    def isolateView(self):
        global oldPanel

        panel = cmds.getPanel(withFocus=True)
        panelType = cmds.getPanel(typeOf=panel)

        if not panelType == "modelPanel":
            if oldPanel:
                panel = oldPanel
                panelType = cmds.getPanel(typeOf=panel)

        if panelType == "modelPanel":
            itemList = []
            oldPanel = panel

            #Store selection
            if self.ui.isolateViewCheckBox.isChecked():
                currentSel = cmds.ls(sl=True)

                #Find Sub Asset Items
                if self.ui.subAssetListWidget.currentItem():
                    subAsset = str(self.ui.subAssetListWidget.currentItem().text())
                    if not str(subAsset) == "Show All":
                        cmds.select(subAsset)
                        if not len(cmds.ls(sl=True))==0:
                            subAssetSel = cmds.ls(sl=True)
                        else:
                            subAssetSel = "__Empty__"
                    else:
                        subAssetSel = None
                else:
                    subAssetSel = None

                #Find Proxy Items
                if self.ui.proxyListWidget.currentItem():
                    proxy = str(self.ui.proxyListWidget.currentItem().text())
                    if not str(proxy) == "Show All":
                        cmds.select(proxy)
                        if not len(cmds.ls(sl=True))==0:
                            proxySel = cmds.ls(sl=True)
                        else:
                            proxySel = None
                    else:
                        proxySel = None
                else:
                    proxySel = None

                #Isolate View
                #If SubAsset is selected for isolated view
                if subAssetSel:
                    if subAssetSel == "__Empty__":
                        cmds.select(d=True)
                        mel.eval('enableIsolateSelect %s true;' % panel)
                    else:
                        if proxySel:
                            for proxy in proxySel:
                                if proxy in subAssetSel:
                                    itemList.append(str(proxy))
                                    self.ui.statusbar.showMessage("")
                                elif "|" in proxy:
                                    proxySplit = proxy.split("|")
                                    for split in proxySplit:
                                        if split in subAssetSel:
                                            itemList.append(str(proxy))
                                            self.ui.statusbar.showMessage("")
                            if not len(itemList) == 0:
                                cmds.select(itemList)
                                mel.eval('enableIsolateSelect %s true;' % panel)
                                self.ui.statusbar.showMessage("")
                            else:
                                cmds.select(d=True)
                                mel.eval('enableIsolateSelect %s true;' % panel)
                                self.ui.statusbar.showMessage("Nothing to isolate - Action skipped")
                        else:
                            cmds.select(subAssetSel)
                            mel.eval('enableIsolateSelect %s true;' % panel)
                            self.ui.statusbar.showMessage("")
                #If no SubAsset is selected for isolated view, but a proxy set is
                else:
                    if proxySel:
                        cmds.select(proxySel, replace=True)
                        mel.eval('enableIsolateSelect %s true;' % panel)
                        self.ui.statusbar.showMessage("")
                    else:
                        mel.eval('enableIsolateSelect %s false;' % panel)
                        self.ui.statusbar.showMessage("")

                #Reselect orig selection
                if not len(currentSel) == 0:
                    cmds.select(currentSel, replace=True)
                else:
                    cmds.select(d=True)
            else:
                mel.eval('enableIsolateSelect %s false;' % panel)
        else:
            self.ui.statusbar.showMessage("%s selected! Please select modelPandel to isolate" % panelType)


    def addSubSetToSet(self):
        item=None
        try:
            item = self.ui.subAssetListWidget.currentItem().text()
        except:
            pass

        if item:
            if not item == "Show All":
                MyForm.addToSet(self, item)
                MyForm.isolateView(self)
            else:
                self.ui.statusbar.showMessage("Please select Set")
        else:
            self.ui.statusbar.showMessage("Please select Set")

    def addProxyToSet(self):
        item=None
        try:
            item = self.ui.proxyListWidget.currentItem().text()
        except:
            pass

        if item:
            if not item == "Show All":
                MyForm.addToSet(self, item)
                MyForm.isolateView(self)
            else:
                self.ui.statusbar.showMessage("Please select Set")
        else:
            self.ui.statusbar.showMessage("Please select Set")

    def addToSet(self, item=None):
        sel = cmds.ls(sl=True)
        itemList=[]

        if sel:
            for s in sel:
                itemList.append(str(s))

            cmds.sets(itemList, include=str(item))
        else:
            self.ui.statusbar.showMessage("Nothing selected to add to set!")


    def removeSubSetFromSet(self):
        item=None
        try:
            item = self.ui.subAssetListWidget.currentItem().text()
        except:
            pass

        if not item == "Show All":
            if item:
                MyForm.removeFromSet(self, item)
            else:
                self.ui.statusbar.showMessage("Please select Set")
        else:
            self.ui.statusbar.showMessage("Please select Set")

    def removeProxyFromSet(self):
        item=None
        try:
            item = self.ui.proxyListWidget.currentItem().text()
        except:
            pass

        if not item == "Show All":
            if item:
                MyForm.removeFromSet(self, item)
            else:
                self.ui.statusbar.showMessage("Please select Set")
        else:
            self.ui.statusbar.showMessage("Please select Set")

    def removeFromSet(self, item=None):
        sel = cmds.ls(sl=True)
        itemList=[]

        if sel:
            for s in sel:
                itemList.append(str(s))

            cmds.sets(itemList, remove=str(item))
        else:
            self.ui.statusbar.showMessage("Nothing selected to add to set!")


    def removeSubSetUI(self):
        self.setType = "SubAsset"
        item=None
        try:
            item = self.ui.subAssetListWidget.currentItem().text()
        except:
            pass

        if item:
            self.removeSetDialog = dsPublishSetsUI.Ui_RemoveSetDialog(self.setType, item)
            QtCore.QObject.connect(self.removeSetDialog.deletePushButton, QtCore.SIGNAL("clicked()"), self.removeSet)
            self.removeSetDialog.exec_()
        else:
            self.ui.statusbar.showMessage("Please select a Set to delete")

    def removeProxySetUI(self):
        self.setType = "Proxy"
        item=None
        try:
            item = self.ui.proxyListWidget.currentItem().text()
        except:
            pass

        if item:
            self.removeSetDialog = dsPublishSetsUI.Ui_RemoveSetDialog(self.setType, item)
            QtCore.QObject.connect(self.removeSetDialog.deletePushButton, QtCore.SIGNAL("clicked()"), self.removeSet)
            self.removeSetDialog.exec_()
        else:
            self.ui.statusbar.showMessage("Please select a Set to delete")

    def removeSet(self):
        if self.setType == "SubAsset":
            item = str(self.ui.subAssetListWidget.currentItem().text())
        if self.setType == "Proxy":
            item = str(self.ui.proxyListWidget.currentItem().text())

        if cmds.objExists(item):
            if cmds.lockNode(item, q=True, lock=False):
                cmds.lockNode(item, lock=False)
            cmds.delete(item)

            #Refresh UI
            MyForm.listProxySets(self)
            MyForm.listSubSets(self)
            self.ui.statusbar.showMessage("%s has been deleted" % item)

            self.removeSetDialog.close()


    def subAssetAdd(self, setType=None, messageAttr=None):
        '''Create Selection set and add connection to root Ctrl'''
        root = "|Rig_Grp"
        subSetPrefix = "_Set"

        if not setType:
            setType = self.setType

        if setType == "Proxy":
            messageAttr = "proxies"
        else:
            messageAttr = "subAssets"

        subAssetName = self.createSetDialog.lineEdit.text()
        subAssetName = str(subAssetName + subSetPrefix)

        #If the subset is given a name
        if subAssetName:
            #If the subset dosen't already exists
            if not cmds.objExists(subAssetName):
                #if the root exists
                if cmds.objExists(root):
                    #if the attr dosen't exists create attr
                    if not cmds.objExists("%s.%s" % (root, messageAttr)):
                        cmds.addAttr(root, at="message", ln=messageAttr)

                #If the attr exists connect it
                if cmds.objExists("%s.%s" % (root, messageAttr)):
                    subSet = cmds.sets(name=subAssetName)
                    cmds.addAttr(subAssetName, at="message", ln=messageAttr)
                    cmds.connectAttr("%s.%s" % (root, messageAttr), "%s.%s" % (subAssetName, messageAttr))
                else:
                    self.ui.statusbar.showMessage("%s.%s dosen't exist" % (root, messageAttr))

                #lock Set after creation
                cmds.lockNode(subSet, lock=True)

                #Refresh UI
                MyForm.listProxySets(self)
                MyForm.listSubSets(self)

                self.ui.statusbar.showMessage("subAsset %s created" % subAssetName)
            else:
                self.ui.statusbar.showMessage("%s already exists" % subAssetName)
        else:
            self.ui.statusbar.showMessage("Please Type a Name for the set")

        sel = cmds.ls(sl=True)

        if sel:
            cmds.select(sel, r=True)

        if subAssetName:
            self.createSetDialog.close()

    def createSubSetUI(self):
        self.setType = "SubAsset"
        MyForm.createSetUI(self, self.setType)

    def createProxySetUI(self):
        self.setType = "Proxy"
        MyForm.createSetUI(self, self.setType)

    def createSetUI(self, setType):
        '''hejsa'''
        self.createSetDialog = dsPublishSetsUI.Ui_Dialog(setType)
        QtCore.QObject.connect(self.createSetDialog.lineEdit, QtCore.SIGNAL("returnPressed()"), self.subAssetAdd)
        QtCore.QObject.connect(self.createSetDialog.okPushButton, QtCore.SIGNAL("clicked()"), self.subAssetAdd)
        QtCore.QObject.connect(self.createSetDialog.comboBox, QtCore.SIGNAL("activated(int)"), self.setDefaultSet)

        self.setDefaultSetCombobox(setType)

        self.createSetDialog.exec_()

    def setDefaultSetCombobox(self, setType):
        #Pass XML to find Default sets
        read = []
        if setType == "Proxy":
            read = self.proxySets
        if setType == "SubAsset":
            read = self.subAssetSets
        i=0

        self.createSetDialog.comboBox.addItem("")
        self.createSetDialog.comboBox.setItemText(i, QtGui.QApplication.translate("dialog", self.defaultSetState, None, QtGui.QApplication.UnicodeUTF8))

        if not read == []:
            for item in read:
                i=i+1
                self.createSetDialog.comboBox.addItem("")
                self.createSetDialog.comboBox.setItemText(i, item)

    def setDefaultSet(self):
        setState = self.createSetDialog.comboBox.currentText()

        if setState == self.defaultSetState:
            self.createSetDialog.lineEdit.clear()
        else:
            self.createSetDialog.lineEdit.setText(setState)

    def aboutMenu(self):
        aboutDialog = QDialog()
        aboutDialog.setObjectName("About")
        aboutDialog.resize(450, 250)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutDialog.sizePolicy().hasHeightForWidth())
        aboutDialog.setSizePolicy(sizePolicy)
        aboutDialog.textBrowser = QtGui.QTextBrowser(aboutDialog)
        aboutDialog.textBrowser.setEnabled(True)
        aboutDialog.textBrowser.setGeometry(QtCore.QRect(10, 10, 430, 230))
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
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Publish Sets Dialog</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Updated: Monday, 11 June 2011</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">By Karsten Friis Nielsen</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">karsten@duckling.dk</span></p>\n"
        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Duckling&Sonne (c)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        aboutDialog.exec_()
        aboutDialog.setVisible()

def UI():
    if cmds.objExists("Rig_Grp"):
        global createSubAssetForm
        createSubAssetForm = MyForm(getMayaWindow())
        createSubAssetForm.show()
    else:
        cmds.error('This is not a Valid scene. File has to contain a "Root_Group" with all of it\'s costume attributes')