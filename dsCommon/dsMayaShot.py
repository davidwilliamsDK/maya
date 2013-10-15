import sys, re, os, shutil,subprocess
import dsMayaEnv
import dsFolderStruct as dsFS
import sgTools
import dsCommon.dsOsUtil as dsOsUtil
reload(dsOsUtil)

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsCommon/dsMayaShot.ui'
    sys.path.append('/dsGlobal/dsCore/shotgun')
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsCommon/dsMayaShot.ui'
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun')

if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
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
        
        
        self.setUp()
        self.updateShots()
        
        self.newShot_B.clicked.connect(self.newShot)
        self.newShotCam_B.clicked.connect(self.newShotCam)
        
    def newShot(self):
        start = self.start_LE.text()
        end = self.end_LE.text()
        name = self.name_LE.text()
        
        if start != "":
            if end != "":
                if self.shotTest(name) == True:
                    self.createNewShot(int(start),int(end),str(name),'persp')
                    self.updateShots()
                    dsFS.dsCreateFs("3D",self.fullPath,name)
                    print "created folder struct"
                    path = self.fullPath
                    if sys.platform == "linux2":
                        path.replace('/dsPipe/','/dsComp/')
                    else:
                        path.replace('//vfx-data-server/dsPipe/','//xserv2.duckling.dk/dsComp/')
                    dsFS.dsCreateFs("COMP",path ,name)
                    print "created comp folder structure"
                    sgTools.sgTestShot("SHOT",str(self.dsProject),str(self.dsEpisode),str(self.dsSeq),str(name))
                    print "created shot in shotgun"

    def createNewShot(self,s,e,name,cam):
        cmds.shot(name,st=s,et=e,sst=s,set=e,cc=cam,shotName=name)
  
    def shotTest(self,n):
        if re.search("s[0-9][0-9][0-9][0-9]",n):
            if n not in self.shotNodeList:
                return True
            else:
                print "shot already present"
                return False
        else:
            return False

    def newShotCam(self):
        start = self.start_LE.text()
        end = self.end_LE.text()
        name = self.name_LE.text()
        
        cameraName = cmds.camera()
        cameraShape = cameraName[1]
        newName = str(name) + "_cam"
        print cameraName
        cmds.rename(cameraName[0],newName)
        
        if start != "":
            if end != "":
                if self.shotTest(name) == True:
                    self.createNewShot(int(start),int(end),str(name),newName)
                    self.updateShots()
                    dsFS.dsCreateFs("3D",self.fullPath,name)
                    print "created folder struct"
                    path = self.fullPath
                    if sys.platform == "linux2":
                        path.replace('/dsPipe/','/dsComp/')
                    else:
                        path.replace('//vfx-data-server/dsPipe/','//xserv2.duckling.dk/dsComp/')
                    dsFS.dsCreateFs("COMP",path ,name)
                    print "created comp folder structure"
                    sgTools.sgTestShot("SHOT",str(self.dsProject),str(self.dsEpisode),str(self.dsSeq),str(name))
                    print "created shot in shotgun"
        
    def updateShots(self):
        self.shots_LV.clear()
        self.shotNodeList = []
        shotNodeList_tmp = cmds.ls(type="shot")
        
        for shot in shotNodeList_tmp:
            if not re.search("_Reference",shot):
                self.shotNodeList.append(shot)
        for shot in self.shotNodeList:
            self.shots_LV.addItem(shot)
        
    def setUp(self):
        dsMayaEnv.setGlobals()
        self.dsRelative = str(os.getenv('RELATIVEPATH'))
        self.dsProject = str(os.getenv('PROJECT'))
        self.dsEpisode = str(os.getenv('EPISODE'))        
        self.dsSeq = str(os.getenv('SEQUENCE'))
        self.fullPath = self.dsRelative + "/" + self.dsProject + "/film/" + self.dsEpisode + "/" + self.dsSeq + "/" 
        
def dsMayaShot():
    global myWindow
    myWindow = Window()
    myWindow.show()