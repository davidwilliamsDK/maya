import sys, sip, re, os, shutil, subprocess
from PyQt4 import QtGui, QtCore, uic
import sgTools, dsCommon
import dsPlayblast as dsPB

try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
except:
    pass

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsAnimation/dsAnimTools.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsAnimation/dsAnimTools.ui'
 
form_class, base_class = uic.loadUiType(uiFile)

class Window(base_class, form_class):
    '''GI ONLY WORKS ON ASCII AND NOT MAYA BINARY'''
    def __init__(self, parent=getMayaWindow()):
        '''A custom window with a demo set of ui widgets'''
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.setUp()
        self.sgGetUser()
        self.updateShots()
        self.getRez()
        
        self.action100.triggered.connect(self.toggle100)
        self.action75.triggered.connect(self.toggle75)
        self.action50.triggered.connect(self.toggle50)

        self.pb_B.clicked.connect(self.pbShot)
        self.pbAll_B.clicked.connect(self.pbALL)
        self.pb_V_B.clicked.connect(self.versionRV)
        self.QT_B.clicked.connect(self.qtShot)
        self.QT_All_B.clicked.connect(self.qtAll)
        self.QT_V_B.clicked.connect(self.versionQT)

    def pbShot(self):
        print "pb shot"
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            dsShot = str(s.text())
            os.environ['SHOT'] = dsShot
            dsPB.pShot(self.dsSeq,dsShot)

    def qtShot(self):
        print "QT shot" 
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            dsShot = str(s.text())
            os.environ['SHOT'] = dsShot
            dsPB.qtShot(self.rez,self.dsProject,self.dsSeq,dsShot)
        
    def pbALL(self):
        print "pb ALL"
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            print s.text()
        
    def qtAll(self):
        print "qt ALL"
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            print s.text()
        
    def versionRV(self):
        print "RV latest versions"
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            print s.text()
        
    def versionQT(self):
        print "QT latest versions"
        sh = self.Shots_LW.selectedItems()
        for s in sh:
            print s.text()

    def playBlastCore(dsSeq,dsShot):
        self.HUD()
        startFrame = cmds.shot(dsShot, q=True, st=True)
        endFrame = cmds.shot(dsShot, q=True, et=True)
        cam = cmds.shot(dsShot,q=True,cc=True)
        self.filePath = cmds.file(q=True,l=True)[0]
    
        pathTmp = self.filePath.split("/")
        pbPath = self.filePath.replace(pathTmp[-1],"")
        newPath = ""
        for path in pathTmp:
            if newPath == "":
                newPath = path
            else:
                newPath = newPath + "/" + path
            if re.search("3D",path):
                break
            
        if sys.platform == "linux2":
            pbPathDir = "/" + newPath + "/playBlast/" + dsShot + "/"
        else:
            pbPathDir = newPath + "/playBlast/" + dsShot + "/"
    
        if not os.path.isdir(pbPathDir):
            os.makedirs(pbPathDir)
        ver = self.getVersion(pbPathDir)
        
        if sys.platform == "linux2":
            pbPath = "/" + newPath + "/playBlast/" + dsShot + "/" + ver + "/"
        else:
            pbPath = newPath + "/playBlast/" + dsShot + "/" + ver + "/"
        
        if os.path.isdir(pbPath):
            tmpList = os.listdir(pbPath)
            for file in tmpList:
                os.remove(pbPath + "/" + file)
        else:
            os.makedirs(pbPath)
        pbName = dsSeq + "_" + dsShot 
    
        if sys.platform == "linux2":    
            shutil.copy(self.filePath,"/" + pbPath + pathTmp[-1])
        else:
            shutil.copy(self.filePath,pbPath + pathTmp[-1])
            
        cmds.playbackOptions( min=str(startFrame), max=str(endFrame))
        pbPanel = cmds.getPanel( withFocus=True )
        self.rezX = cmds.getAttr("defaultResolution.width")
        self.rezY = cmds.getAttr("defaultResolution.height")
        if sys.platform =="linux2":
            self.pbFrames = "/" + pbPath + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver
        else:
            self.pbFrames = pbPath + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver
        cmds.setAttr("defaultRenderGlobals.imageFormat",8)
    
        frameRange = range(startFrame,endFrame + 1)
        cmds.playblast(frame=frameRange, orn=True, format='image', cc=True,fo=True, fp=4, st=startFrame, et=endFrame, qlt=100, p=100, f=self.pbFrames, h=self.rezY, w=self.rezX, os=True, v=False)
        mel.eval('camera -e -displayFilmGate off -displayResolution on -overscan 1.0 ' + cam + ';')
        
        if sys.platform == "linux2":
            self.frameStack = "/" + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"
        else:
            self.frameStack = + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"

    def updateShotGun(pbPath,ver,dsShot):
        us = self.User_CB.currentText()
        if sys.platform == "linux2":
            imageList = os.listdir("/" + pbPath[:-1] + "/")
            imageList.sort()
            imagePath = "/" + pbPath[:-1] + "/" +imageList[1]
        else:
            imageList = os.listdir(pbPath[:-1] + "/")
            imageList.sort()
            imagePath = pbPath[:-1] + "/" +imageList[1]
        sgTools.sgPublishFrameStack(str(imagePath),str(self.filePath),'blocking',str(us),ver,dsShot)

    def openRV(framestack):
        if sys.platform == "linux2":
            rvpush = '/usr/local/rv-Linux-x86-64-3.12.15/bin/rvpush'
        else:
            rvpush = '"C:/Program Files (x86)/Tweak/RV-3.12.16-32/bin/rvpush.exe"'
    
        if sys.platform == "linux2":
            cmd = rvpush + ' merge ' + "/" + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"
        else:
            cmd = rvpush + ' merge ' + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"
            
    def makeQT(rez,src,x,y,sq,sh,pr,dst):
        if rez == 100:
            cmd = self.rvio + ' -vv [ %s -uncrop %s %s 0 50 ] -fps 25 -overlay frameburn 1 1 40 -overlay textburn "" "" "" "%s_%s" "duckling A/S = %s" "" 1 40.0 -outsrgb -o %s' % (src,x,y,sq,sh,pr,dst)
            os.system(cmd)
        if rez == 75:
            cmd = self.rvio + ' -vv [ %s -uncrop %s %s 0 50 ] -scale 0.75 -fps 25 -overlay frameburn 1 1 25 -overlay textburn "" "" "" "%s_%s" "duckling A/S = %s" "" 1 25.0 -outsrgb -o %s' % (src,x,y,sq,sh,pr,dst)
            os.system(cmd)
        if rez == 50:
            cmd = self.rvio + ' -vv [ %s -uncrop %s %s 0 60 ] -scale 0.5  -fps 25 -overlay frameburn 1 1 20 -overlay textburn "" "" "" "%s_%s" "duckling A/S = %s" "" 1 20.0 -outsrgb -o %s' % (src,x,y,sq,sh,pr,dst)
            os.system(cmd)

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
    def getRez(self):
        if self.action100.isChecked():
            self.rez = 100
        if self.action75.isChecked():
            self.rez = 75
        if self.action50.isChecked():
            self.rez = 50
    def toggle100(self):
        self.rez = 100
        self.action75.setChecked(False)
        self.action50.setChecked(False)
    def toggle75(self):
        self.rez = 75
        self.action100.setChecked(False)
        self.action50.setChecked(False)
    def toggle50(self):
        self.rez = 50
        self.action100.setChecked(False)
        self.action75.setChecked(False)
    def updateShots(self):
        self.Shots_LW.clear()
        self.shotNodeList = []
        shotNodeList_tmp = cmds.ls(type="shot")
        
        for shot in shotNodeList_tmp:
            if not re.search("_Reference",shot):
                self.shotNodeList.append(shot)
        for shot in self.shotNodeList:
            self.Shots_LW.addItem(shot)
    def sgGetUser(self):
        self.User_CB.clear()
        self.userDict = {}
        self.userProject = {}
        self.group = {'type': 'Group', 'id': 5}
        self.myPeople = sgTools.sgGetPeople()
        for user in self.myPeople:
            userName = str(user['name'])
            self.User_CB.addItem(userName)
            self.userDict[userName] = user['id']
    def HUD(self):
        cmds.headsUpDisplay( rp=(5, 1) )
        cmds.headsUpDisplay( rp=(5, 2) )
        cmds.headsUpDisplay( rp=(7, 0) )
        cmds.headsUpDisplay( rp=(7, 1) )
        cmds.headsUpDisplay( rp=(9, 3) )
        cmds.headsUpDisplay( rp=(9, 2) )
        cmds.headsUpDisplay( rp=(9, 1) )
        cmds.grid(tgl=False)
        cmds.headsUpDisplay('HUDCameraName', s=7, b=1 ,dp=1,ba='left',bs='small',dfs='large', lfs='large', lw=75, dw=50, pre='cameraNames')
        cmds.headsUpDisplay('HUDCurrentFrame', s=9, b=1 ,dp=1,ba='left',label='FRAME',atr=True,bs='small',dfs='large', lfs='large', lw=75, dw=50, c='import dsAnimation.HUDInfo;dsAnimation.HUDInfo.GetFrame()')
        cmds.headsUpDisplay('HUDShot', s=9, b=3 ,dp=1, ba='left',label='SEQ',atr=True,bs='small',dfs='large', lfs='large', lw=75, dw=50 , c='import dsAnimation.HUDInfo;dsAnimation.HUDInfo.GetSeqName()')
        cmds.headsUpDisplay('HUDSequence', s=9, b=2,dp=1, ba='left',label='SHOT', atr=True, bs='small',dfs='large', lfs='large', lw=75, dw=50, c='import dsAnimation.HUDInfo;dsAnimation.HUDInfo.GetShotName()')
        cmds.headsUpDisplay('HUDShotDuration', s=5, b=1,dp=1,ba='left',label='DURATION', atr=True, da="right", bs='small',dfs='large', lfs='large', lw=75, dw=50, c='import dsAnimation.HUDInfo;dsAnimation.HUDInfo.GetShotDuration()')
    def removeHUD(self):
        cmds.headsUpDisplay('HUDCameraName',rem=True)
        cmds.headsUpDisplay('HUDCurrentFrame',rem=True)
        cmds.headsUpDisplay('HUDShot',rem=True)
        cmds.headsUpDisplay('HUDSequence',rem=True)
        cmds.headsUpDisplay('HUDShotDuration',rem=True)
    
def dsAnim():
    global myWindow
    myWindow = Window()
    myWindow.show()