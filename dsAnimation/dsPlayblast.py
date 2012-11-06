import maya.cmds as cmds
import maya.mel as mel
import os, re,shutil, subprocess,sys
import dsCommon.dsMayaEnv

import dsAnimation.HUDInfo;reload(dsAnimation.HUDInfo)

if sys.platform == "linux2":
    sys.path.append('/dsGlobal/dsCore/shotgun/')
else:
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun/')

import sgTools;reload(sgTools)

from xml.etree import ElementTree as ET
from xml.dom import minidom

def HUD():
    print "HUD"
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

def removeHUD():
    print "remove HUD"
    cmds.headsUpDisplay('HUDCameraName',rem=True)
    cmds.headsUpDisplay('HUDCurrentFrame',rem=True)
    cmds.headsUpDisplay('HUDShot',rem=True)
    cmds.headsUpDisplay('HUDSequence',rem=True)
    cmds.headsUpDisplay('HUDShotDuration',rem=True)

def setUp():
    global dsRelative,dsProject,dsEpisode,dsSeq,dsShot
    dsCommon.dsMayaEnv.setGlobals()
    dsRelative = str(os.getenv('RELATIVEPATH'))
    dsProject = str(os.getenv('PROJECT'))
    dsEpisode = str(os.getenv('EPISODE'))		
    dsSeq = str(os.getenv('SEQUENCE'))
    dsShot = checkCamSeq()
    print dsShot
    os.environ['SHOT'] = dsShot
    print dsProject

def checkCamSeq():
    currentShot = None
    camSeqTime = mel.eval('float $newTime = getSequenceTime();')
    shotNodeList = []
    shotNodeList_tmp = cmds.ls(type="shot")
    
    for shot in shotNodeList_tmp:
        if not re.search("_Reference",shot):
            shotNodeList.append(shot)
            
    for shotName in shotNodeList:
        startVal = cmds.shot(shotName, q=True, st=True)
        endVal = cmds.shot(shotName, q=True, et=True)
        nameVal = cmds.shot(shotName, q=True, sn=True)
        camVal = cmds.shot(shotName,q=True,cc=True)
        if int(camSeqTime) <= int(endVal) and int(camSeqTime) >= int(startVal):
            currentShot = shotName
        else:
            print 'Shot %s is outside of the camera sequencer timeframe.' % shotName
    return currentShot

def checkShot():
    dsShot = str(os.getenv('SHOT'))
    print dsShot
    shotNode = cmds.ls(type="shot")
    if shotNode != []:
        startVal = int(cmds.shot(str(dsShot), q=True, sst=True))
        endVal = int(cmds.shot(str(dsShot), q=True, set=True))
        camVal = cmds.shot(str(dsShot), q=True,cc=True)
        cmds.playbackOptions( min='0', max=str(endVal))
        #pbShot(dsRelative,dsProject,dsEpisode,dsSeq,dsShot)
    else:
        startVal = int(cmds.playbackOptions(q=True,minTime=True))
        endVal = int(cmds.playbackOptions(q=True,maxTime=True))
        pbPanel = cmds.getPanel( withFocus=True )
        activeCam = cmds.modelEditor(pbPanel,q=True,cam=True)
        print activeCam
        myShot = cmds.shot(dsShot, st=startVal, et=endVal)
        cmds.shot(myShot, e=True, sst=startVal, set=endVal)
        cmds.shot(myShot, e=True, cc=activeCam)

        cmds.playbackOptions( min='0', max=str(endVal))
        #pbShot(dsRelative,dsProject,dsEpisode,dsSeq,dsShot)
        print "Please run DS Shot Global from dsMenu/dsCommercial"

def getVersion(dsPublishPath):
    verList = []
    verList_tmp = os.listdir(dsPublishPath)
    for folder in verList_tmp:
        if re.search("v\d{3}",folder):
            if os.path.isdir(dsPublishPath + folder):
                verList.append(folder)
    print verList
    if len(verList) == 0:
        return 'v%03d' %int(1)
    else:  
        for ver in verList:
            dsVer = 'v%03d' %int(ver[-3:])
            newVal = int(len(verList)) + 1
            val = '%03d' %int(newVal)
            return 'v%03d' %int(newVal)
    
def pbShot():
    
    setUp()
    checkShot()
    HUD()
    startFrame = cmds.shot(dsShot, q=True, st=True)
    endFrame = cmds.shot(dsShot, q=True, et=True)
    cam = cmds.shot(dsShot,q=True,cc=True)
    filePath = cmds.file(q=True,l=True)[0]
    
    pathTmp = filePath.split("/")
    pbPath = filePath.replace(pathTmp[-1],"")
    newPath = ""
    
    if re.search("3D",filePath):
    	for path in pathTmp:
    		if newPath == "":
    			newPath = path
    		else:
    			newPath = newPath + "/" + path
    		if re.search("3D",path):
    			break
    else:
        for path in pathTmp:
            if newPath == "":
                newPath = path
            else:
                newPath = newPath + "/" + path
            print newPath
            if re.search("q[0-9][0-9][0-9][0-9]",path):
                break
    
    print newPath
        
    if sys.platform == "linux2":
        pbPathDir = "/" + newPath + "/playBlast/" + dsShot + "/"
    else:
        pbPathDir = newPath + "/playBlast/" + dsShot + "/"

    if not os.path.isdir(pbPathDir):
        os.makedirs(pbPathDir)
    ver = getVersion(pbPathDir)

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
        shutil.copy(filePath,"/" + pbPath + pathTmp[-1])
    else:
        shutil.copy(filePath,pbPath + pathTmp[-1])

    cmds.playbackOptions( min=str(startFrame), max=str(endFrame))
    pbPanel = cmds.getPanel( withFocus=True )
    rezX = cmds.getAttr("defaultResolution.width")
    rezY = cmds.getAttr("defaultResolution.height")
    if sys.platform =="linux2":
        pbFrames = "/" + pbPath + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver
    else:
        pbFrames = pbPath + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver
    cmds.setAttr("defaultRenderGlobals.imageFormat",8)
    
    frameRange = range(startFrame,endFrame + 1)
    cmds.playblast(frame=frameRange, orn=True, format='image', cc=True,fo=True, fp=4, st=startFrame, et=endFrame, qlt=100, p=100, f=pbFrames, h=rezY, w=rezX, os=True, v=False)
    mel.eval('camera -e -displayFilmGate off -displayResolution on -overscan 1.0 ' + cam + ';')
    
    if sys.platform == "linux2":
        rvpush = '/usr/local/rv-Linux-x86-64-3.12.15/bin/rvpush'
    else:
        rvpush = '"C:/Program Files (x86)/Tweak/RV-3.12.16-32/bin/rvpush.exe"'

    if sys.platform == "linux2":
        cmd = rvpush + ' merge ' + "/" + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"
    else:
        cmd = rvpush + ' merge ' + pbPath[:-1] + "/" + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver + ".####.jpeg"

    os.system(cmd)
    removeHUD()

    if sys.platform == "linux2":
        imageList = os.listdir("/" + pbPath[:-1] + "/")
        imageList.sort()
        imagePath = "/" + pbPath[:-1] + "/" +imageList[1]
    else:
        imageList = os.listdir(pbPath[:-1] + "/")
        imageList.sort()
        imagePath = pbPath[:-1] + "/" +imageList[1]
    
    sgTools.sgPublishFrameStack(str(imagePath),str(filePath),'blocking',str(''),ver,dsShot)