import os,sys,sip
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import dsCommon.dsOsUtil as osUtil
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

guiName = "dsVrayElementsPreset.ui"
clashNameSpace = "CLASSINGELEMENT_"

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsRender/%s' % guiName
    presetPath = '/' + status +  "/globalMaya/presets/vrayElements/"
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsRender/%s' % guiName
        presetPath = server + "/globalMaya/presets/vrayElements/"
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsRender/%s' % guiName
        presetPath = server + "/globalMaya/presets/vrayElements/"

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

#Importing maya UI
try:
    import maya.OpenMayaUI as mui
except:
    pass

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    ptr = long(ptr)
    return sip.wrapinstance(long(ptr), QtCore.QObject)
    print "woop"

class dsVrayElementTool(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        self.findPresets()

        self.loadPreset.clicked.connect(self.presetLoad)
        self.savePreset.clicked.connect(self.presetSave)
        self.presetName.returnPressed.connect(self.presetSave)
        self.presetList.itemDoubleClicked.connect(self.presetLoad)

    def findPresets(self):
        presets = osUtil.listMb(presetPath)
        self.presetList.clear()
        i = 0
        item = QtGui.QListWidgetItem(self.presetList)
        for preset in presets:
            self.presetList.addItem("")
            self.presetList.item(i).setText(QtGui.QApplication.translate("Vray Render Elements", preset.split(".", 1)[0], None, QtGui.QApplication.UnicodeUTF8))
            i=i+1

    def presetSave(self):
        currentSelection = cmds.ls(sl=True)
        newPresetName = self.presetName.text()

        if not newPresetName == "":
            print self.allElements.isChecked()
            if self.allElements.isChecked():
                elementsToSave = self.getVrayElements()
            else:
                elementsToSave = mel.eval("treeView -query -selectItem listAdded")

            if elementsToSave:
                cmds.select(elementsToSave)
                print "saving %s " % elementsToSave
                cmds.file("%s%s" % (presetPath, newPresetName), force=True, options="v=0", type="mayaBinary", pr=True, es=True)
                self.findPresets()

            self.presetName.clear()

            if currentSelection:
                cmds.select(currentSelection)
            else:
                cmds.select(d=True)
        else:
            print "please give the preset a name before saving"

    def presetLoad(self):
        render = mel.eval("currentRenderer")
        if not render == "vray":
             cmds.setAttr("defaultRenderGlobals.currentRenderer", "vray", type="string")
        origRenderElements = self.getVrayElements()
        selectedPreset = self.presetList.currentItem().text()
        if selectedPreset:
            print ("%s%s.mb" % (presetPath, selectedPreset))
            cmds.file("%s%s.mb" % (presetPath, selectedPreset),i=True, type="mayaBinary", mergeNamespacesOnClash=False, rpr=clashNameSpace, options="v=0", pr=True)

        if self.checkBox.isChecked():
            newRenderElements = self.getVrayElements()
            self.cleanClashingElements(origRenderElements, newRenderElements)

    def getVrayElements(self):
        return cmds.ls(type="VRayRenderElement")

    def cleanClashingElements(self, origRenderElements, newRenderElements):
        for newElement in newRenderElements:
            if clashNameSpace in newElement:
                if not newElement.split(clashNameSpace)[-1] in origRenderElements:
                    classingBaseName = newElement.split(clashNameSpace + "_")[-1]
                    cmds.delete(classingBaseName)
                    cmds.rename(newElement, classingBaseName)


def vrayElementUI():
    global myWindow
    myWindow = dsVrayElementTool()
    myWindow.show()
