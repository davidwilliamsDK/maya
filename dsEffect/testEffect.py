import sys, re, os, shutil, subprocess, stat, webbrowser, time,string

sys.path.append(r'\\vfx-data-server\dsGlobal\globalMaya\Python\PyQt_Win64')
sys.path.append(r'\\vfx-data-server\dsGlobal\dsCore\maya')
uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsModelLib/modelLibUI02.ui'

import dsCommon.dsOsUtil as dsOsUtil;reload(dsOsUtil)

pyVal = dsOsUtil.getPyGUI()
    
if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui

  
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

if pyVal == "PySide":
    parentVar = getMayaWindow()
else:
    parentVar = None

class Window(base_class, form_class):
    def __init__(self, parent=parentVar):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        
        
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
        
def dsShotOpen():
    global dsShotOpenWindow
    try:
        dsShotOpenWindow.close()
    except:
        pass
    dsShotOpenWindow = Window()
    dsShotOpenWindow.show()