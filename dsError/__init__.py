import sys
import sip
import maya.OpenMayaUI as mui
from PyQt4 import QtGui, QtCore, uic

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsError/ui.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsError/ui.ui'
 
form_class, base_class = uic.loadUiType(uiFile)

class dsErrorUI(base_class, form_class):
    def __init__(self, error = None, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.error = error
        if self.error:
            self.textEdit.setText(str(error))
            
    def set(self, string):
        #print self.textEdit.text()
        self.textEdit.append(str(string))
        
    def clear(self):
        self.textEdit.clear()
    
def error(error=None):
    global something
    something = dsErrorUI(error)
    something.show()