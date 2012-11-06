#Importing Modules
import sys, os, sip
from PyQt4 import QtGui, QtCore, uic
import dsCommon.dsProjectUtil as projectUtil

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsSmooth/dsSmoothCtrlUI.ui'
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsSmooth/dsSmoothCtrlUI.ui'
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsSmooth/dsSmoothCtrlUI.ui'

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

#Importing maya UI
try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
except:
    pass


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    ptr = long(ptr)
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class dsSmoothCtrl(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
##        base_class.__init__(self, parent=getMayaWindow())
        self.setupUi(self)

        #GUI
        self.label = []
        self.slider = []
        self.spinbox = []

        #Init
        self.createSliders()
        self.getSmoothState()

        #Signals
        self.smooth_pushButton.clicked.connect(self.createSmoothAttr)
        self.smooth_pushButton.clicked.connect(self.createSmoothNodes)
        self.delete_pushButton.clicked.connect(self.deleteSmoothNodes)

    def listAssets(self):
        fullname = cmds.ls("*:Rig_Grp")
        nicename = []
        for name in fullname:
            nicename.append(name.split(":",1)[0])
        return nicename

    def deleteSmoothNodes(self):
        for asset in self.label:
            if cmds.objExists("%s:Rig_Grp.smooth" % asset.text()):
                smooth = cmds.listConnections("%s:Rig_Grp.smooth" % asset.text(), s=False, d=True, type="polySmoothFace")
                cmds.delete(smooth)

    def getSmoothState(self):
        self.oldVal = []
        for asset in self.label:
            if cmds.objExists("%s:Rig_Grp.smooth" % asset.text()):
                smoothVal = cmds.getAttr("%s:Rig_Grp.smooth" % asset.text())
                index = self.label.index(asset)
                self.slider[index].setValue(smoothVal)

    def setSmoothState(self, val):
        sender = self.sender()
        index = self.spinbox.index(sender)
        asset = self.label[index]

        if cmds.objExists("%s:Rig_Grp.smooth" % asset.text()):
            cmds.setAttr("%s:Rig_Grp.smooth" % asset.text(), val)


    def createSmoothAttr(self):
        for asset in self.label:
            if not cmds.objExists("%s:Rig_Grp.smooth" % asset.text()):
                cmds.addAttr("%s:Rig_Grp" % asset.text(), ln="smooth", at="long", min=0, max=2)
                cmds.setAttr("%s:Rig_Grp.smooth" % asset.text(), e=True, keyable=True)
                index = self.label.index(asset)
                val = self.spinbox[index].value()
                cmds.setAttr ("%s:Rig_Grp.smooth" % asset.text(), val)

    def createSmoothNodes(self):
        rendertime = self.rendertime_checkBox.checkState()
        if not rendertime == 2:
            for asset in self.label:
                if cmds.objExists("%s:Rig_Grp.smooth" % asset.text()):
                    smoothedMesh = []
                    smoothNode = cmds.listConnections("%s:Rig_Grp.smooth" % asset.text(), s=False, d=True, type="polySmoothFace")
                    if smoothNode:
                        for node in smoothNode:
                            meshSmoothed = cmds.listConnections("%s.output" % node, s=False, d=True, type="mesh")[0]
                            smoothedMesh.append(meshSmoothed)

                    mesh = cmds.ls("%s:mesh_*" % asset.text(), l=True, type="transform")
                    for m in mesh:
                        if cmds.objectType(m, isType='transform') == 1:
                            if not m.rsplit("|",1)[-1] in smoothedMesh:
                                smoothNode = cmds.polySmooth(m)[0]
                                cmds.connectAttr("%s:Rig_Grp.smooth" % asset.text(), "%s.divisions" % smoothNode )

    def createSliders(self):
        assets = self.listAssets()

        #Set Font
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        yInt = 35
        yStart = 90

        i = 0
        for asset in assets:
            mesh = cmds.ls("%s:mesh_*" % asset, l=True, type="transform")
            if not mesh == []:
                self.label.append("")
                self.slider.append("")
                self.spinbox.append("")

                #Make Label
                self.label[i] = QtGui.QLabel(asset, self)
                self.label[i].move(25,yStart + (yInt*i))
                self.label[i].setFont(font)

                #Make slider
                self.slider[i] = QtGui.QSlider(self)
                self.slider[i].setMaximum(2)
                self.slider[i].setTickInterval(1)
                self.slider[i].setOrientation(QtCore.Qt.Horizontal)
                self.slider[i].move(150,yStart + (yInt*i))
                self.slider[i].setMinimumSize(QtCore.QSize(160, 35))
                self.slider[i].setMaximumSize(QtCore.QSize(160, 35))

                #Make Spinbox
                self.spinbox[i] = QtGui.QSpinBox(self)
                self.spinbox[i].setMaximum(2)
                self.spinbox[i].move(320,yStart + 7 + (yInt*i))
                self.spinbox[i].setMinimumSize(QtCore.QSize(35, 20))
                self.spinbox[i].setMaximumSize(QtCore.QSize(35, 20))

                QtCore.QObject.connect(self.slider[i], QtCore.SIGNAL("valueChanged(int)"), self.spinbox[i].setValue)
                QtCore.QObject.connect(self.spinbox[i], QtCore.SIGNAL("valueChanged(int)"), self.slider[i].setValue)
                QtCore.QObject.connect(self.spinbox[i], QtCore.SIGNAL("valueChanged(int)"), self.setSmoothState)

                i = i+1

def dsSmooth():
    global myWindow
    myWindow = dsSmoothCtrl()
    myWindow.show()