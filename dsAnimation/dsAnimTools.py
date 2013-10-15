import sys, re, os, shutil, subprocess
import sgTools, dsCommon
import dsPlayblast;reload(dsPlayblast)
import dsCommon.dsOsUtil as dsOsUtil;reload(dsOsUtil)
import dsSQLTools as dsSQL

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsAnimation/dsAnimTools.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsAnimation/dsAnimTools.ui'
    
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
        self.sgGetUser()
        self.updateShots()

        if sys.platform == "linux2":
            self.home = os.getenv("HOME")
            self.config_dir = '%s/.animTools' % (self.home)
            self.config_path = '%s/config.ini' % (self.config_dir)

        elif sys.platform == 'win32':
            self.home = 'C:%s' % os.getenv("HOMEPATH")
            self.config_dir = '%s/.animTools' % (self.home)
            self.config_dir = self.config_dir.replace("/","\\")
            self.config_path = '%s/config.ini' % (self.config_dir)
            self.config_path = self.config_path.replace("/","\\")

        self.load_config()
        self.User_CB.currentIndexChanged.connect(self.save_config)
        self.collect_B.clicked.connect(self.collect)
        self.blast_B.clicked.connect(self.pbShotAction)
        self.refresh_B.clicked.connect(self.updateShots)
        self.QT_B.clicked.connect(self.qtShot)
        #self.QT_All_B.clicked.connect(self.qtAll)
        #self.QT_V_B.clicked.connect(self.versionQT)

    def collect(self):
        print "collecting latest versions"
        sObj = self.shot_LW.selectedItems()
        shotList =[]
        for s in sObj:
            shotList.append(str(s.text()))
        shotList.sort()
        dsPlayblast.pbCollectShots(shotList)

    def pbShotAction(self):
        print "playBlast shot or shots"
        reload(dsPlayblast)
        sh = self.shot_LW.selectedItems()
        for s in sh:
            dsShot = str(s.text())
            os.environ['SHOT'] = dsShot
            user = self.User_CB.currentText()
            dsPlayblast.pbShot(dsShot,user)

    def qtShot(self):
        print "QT shot"
        sObj = self.shot_LW.selectedItems()
        shotList =[]
        for s in sObj:
            shotList.append(str(s.text()))
        shotList.sort()
        dsPlayblast.qtShot(shotList,self.dsEpisode,self.dsSeq)

    def getVersion(self,dsPublishPath):
        verList = []
        verList_tmp = os.listdir(dsPublishPath)
        for folder in verList_tmp:
            if re.search("v\d{3}",folder):
                if os.path.isdir(dsPublishPath + folder):
                    verList.append(folder)
        if len(verList) == 0:
            return 'v%03d' %int(1)
        else:
            for ver in verList:
                dsVer = 'v%03d' %int(ver[-3:])
                newVal = int(len(verList)) + 1
                val = '%03d' %int(newVal)
                return 'v%03d' %int(newVal)

    def setUp(self):
        dsCommon.dsMayaEnv.setGlobals()
        self.dsRelative = str(os.getenv('RELATIVEPATH'))
        self.dsProject = str(os.getenv('PROJECT'))
        self.dsEpisode = str(os.getenv('EPISODE'))
        self.dsSeq = str(os.getenv('SEQUENCE'))

    def updateShots(self):
        self.shot_LW.clear()
        self.shotNodeList = []
        shotNodeList_tmp = cmds.ls(type="shot")

        for shot in shotNodeList_tmp:
            if not re.search("_Reference",shot):
                self.shotNodeList.append(shot)
        for shot in self.shotNodeList:
            self.shot_LW.addItem(shot)

    def sgGetUser(self):
        self.User_CB.clear()
        self.userDict = {}
        self.userProject = {}
        self.group = {'type': 'Group', 'id': 5}
        self.myPeople = dsSQL.getValueDB("//vfx-data-server/dsGlobal/globalusers","Users","Status","act")
        
        #self.myPeople = sgTools.sgGetPeople()
        
        for user in sorted(self.myPeople):
            userName = str(user[1])
            self.User_CB.addItem(userName)
            self.userDict['id'] = user[0]

    def load_config(self):
        '''
        Load config which is a dictionary and applying setting.
        '''
        if os.path.exists(self.config_path):
            print 'Loading config file from:', self.config_path
            config_file = open( '%s' % self.config_path, 'r')
            list = config_file.readlines()
            config_file.close()

            config = {}
            for option in list:
                key, value = option.split('=')
                config[key] = value.strip()

            index = [i for i in range(self.User_CB.count()) if self.User_CB.itemText(i) == config.get('USER')][0]
            self.User_CB.setCurrentIndex(index)

    def save_config(self):
        '''
        Save setting to the config file as a dictionary.
        '''
        user = self.User_CB.currentText()
        if not os.path.exists(self.config_dir):
            #print self.config_dir, self.config_path
            os.mkdir(self.config_dir)
        config = open( '%s' % self.config_path, 'w')
        config.write('USER=%s\n' % (user))
        config.close()

        self.load_config()
        return self.config_path


def dsPB():
    global dsAnimToolsWindow
    try:
        dsAnimToolsWindow.close()
    except:
        pass
    dsAnimToolsWindow = Window()
    dsAnimToolsWindow.show()