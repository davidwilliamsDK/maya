import sys
import maya.OpenMayaUI as mui
import dsCommon.dsOsUtil as dsOsUtil

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsError/ui.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsError/ui.ui'
    
pyVal = dsOsUtil.getPyGUI()

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

class Window(base_class, form_class):

    def __init__(self, parent=getMayaWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.error = error
        if self.error:
            self.textEdit.setText(str(error))
            
    def set(self, string):
        #print self.textEdit.text()
        self.textEdit.append(str(string))
        
    def clear(self):
        self.textEdit.clear()
    
    
def dsErrorUI(error=None):
    global myWindow
    myWindow = Window()
    myWindow.show()