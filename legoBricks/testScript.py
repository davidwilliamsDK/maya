#Importing Modules
import sys, os, sip
from PyQt4 import QtGui, QtCore, uic

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

guiName = "legoColors.ui"

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/legoBricks/%s' % guiName
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/legoBricks/%s' % guiName
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/legoBricks/%s' % guiName

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

class mayaTestGui(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        #Signals
        self.pushButton.clicked.connect(self.action)

    def action(self):
        print "button is clicked"
        checkBoxstate = self.checkBox.isChecked()
        if checkBoxstate:
            self.running()

    def running(self):
        print "this"

def testGui():
    global myWindow
    myWindow = mayaTestGui()
    myWindow.show()