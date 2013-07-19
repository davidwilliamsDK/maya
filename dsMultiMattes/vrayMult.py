#Importing Modules
import sys, os, sip
from PyQt4 import QtGui, QtCore, uic
import vrayMultUtil as vmult
reload(vmult)
import webbrowser
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

guiName = "vrayMultUI_v02.ui"

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsMultiMattes/%s' % guiName
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsMultiMattes/%s' % guiName
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsMultiMattes/%s' % guiName

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

class vrayMultTool(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        #GUI
        self.spinbox = []
        self.createSpinbox()

        #Signals
        self.pushButton_multimmattes.clicked.connect(self.multMattes)
        self.pushButton_ID.clicked.connect(self.ID)
        self.pushButton_linkedAssetID.clicked.connect(self.assetID)
        self.checkBox_multiForAllID.clicked.connect(self.endIndexDis)
        self.checkBox_createRenderlayer.clicked.connect(self.elementDis)
        self.radioButton_objectID.clicked.connect(self.radioCheck)
        self.radioButton_multiID.clicked.connect(self.radioCheck)

##        self.connect(self.actionAbout, QtCore.SIGNAL("activated(int)"), self.aboutMenu);
        self.actionID_Setup_Help.triggered.connect(self.help)

    def radioCheck(self):
        if self.radioButton_objectID.isChecked():
            self.checkBox_allShaders.setText("Apply ID to all objects in the scene")
        else:
            self.checkBox_allShaders.setText("Apply ID to all shaders in the scene")

    def help(self):
        print "http://vfx.duckling.dk/"

    def assetID(self):
        states = self.returnAttr()
        if states["operationState"] == 2:
            operation = "singleID"
        else:
            operation = "unikID"
        vmult.linkedShaders(states, operation)

    def elementDis(self):
        if self.checkBox_createRenderlayer.checkState() == 2:
            self.checkBox_disableElements.setEnabled(True)
        if self.checkBox_createRenderlayer.checkState() == 0:
            self.checkBox_disableElements.setEnabled(False)

    def endIndexDis(self):
        if self.checkBox_multiForAllID.checkState() == 0:
            self.spinbox[1].setEnabled(True)
        if self.checkBox_multiForAllID.checkState() == 2:
            self.spinbox[1].setEnabled(False)

    def ID(self):
        if self.checkBox_singleID.checkState() == 2:
            operation = "singleID"
        else:
            operation = "unikID"

        states = self.returnAttr()
        vmult.setVrayID(states, operation)

    def multMattes(self):
        states = self.returnAttr()
        if states["multiForAllID"] == 2:
            ids = vmult.findID(states)
            states["startIndex"] = ids[0]
            states["endIndex"] = ids[1]
            states["ids"] = ids[2]

        vmult.setVrayMult(states)

    def returnAttr(self):
        if self.radioButton_objectID.isChecked():
            objectOrMult = 2
        else:
            objectOrMult = 0
        allState = self.checkBox_allShaders.checkState()
        multiState = self.checkBox_multimattesForID.checkState()
        overrideState = self.checkBox_override.checkState()
        nameState = self.lineEdit_multimatteName.text()
        startState = self.spinbox[0].value()
        endState = self.spinbox[1].value()
        multiForAllID = self.checkBox_multiForAllID.checkState()
        createRenderLayer = self.checkBox_createRenderlayer.checkState()
        disableElements = self.checkBox_disableElements.checkState()
        operationState = self.checkBox_singleID.checkState()

        #Return all gui settings
        return {"operationState":operationState, "objectOrMult":objectOrMult, "allShaders":allState, "multiMattes":multiState, "override":overrideState, "matteName":nameState, "startIndex":startState, "endIndex":endState, "multiForAllID":multiForAllID, "createRenderLayer":createRenderLayer, "disableElements":disableElements, "ids":None}

    def createSpinbox(self):
        #Make Spinbox A
        y = [308, 498]
        for i in range(0,2):
            self.spinbox.append("")
            self.spinbox[i] = QtGui.QSpinBox(self)
            self.spinbox[i].setMaximum(10000000)
            self.spinbox[i].move(160,y[i])
            self.spinbox[i].setMinimumSize(QtCore.QSize(170, 22))
            self.spinbox[i].setMaximumSize(QtCore.QSize(170, 22))

            QtCore.QObject.connect(self.spinbox[i], QtCore.SIGNAL("valueChanged(int)"), self.setSpinVal)

    def setSpinVal(self):
        '''Set spindbox Values'''
        sender = self.sender()
        attr = self.returnAttr()
        if sender == self.spinbox[0]:
            if attr["startIndex"] > attr["endIndex"]:
                self.spinbox[1].setValue(attr["startIndex"])
        if sender == self.spinbox[1]:
            if attr["startIndex"] > attr["endIndex"]:
                self.spinbox[0].setValue(attr["endIndex"])

###Store Window Settings
##    def closeEvent(self, event):
##        self.writeSettings()
##
##    def writeSettings(self):
##        '''Write settings'''
##        settings = QtCore.QSettings("Duckling&Sonne", "VrayMultiMatteSettings")
##
##        settings.setValue("checkBox_allShaders", self.checkBox_allShaders.isChecked())
##        settings.setValue("checkBox_multimattesForID", self.checkBox_multimattesForID.isChecked())
##        settings.setValue("checkBox_override", self.checkBox_override.isChecked())
##        settings.setValue("lineEdit_multimatteName", self.lineEdit_multimatteName.isChecked())
##        settings.setValue("checkBox_multiForAllID", self.checkBox_multiForAllID.isChecked())
##        settings.setValue("checkBox_createRenderlayer", self.checkBox_createRenderlayer.isChecked())
##        settings.setValue("checkBox_disableElements", self.checkBox_disableElements.isChecked())

def vrayMult():
    global myWindow
    myWindow = vrayMultTool()
    myWindow.show()