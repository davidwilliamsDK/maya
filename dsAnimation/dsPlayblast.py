import maya.cmds as cmds
import maya.mel as mel
import os, re,shutil, subprocess,sys

import dsCommon.dsMayaEnv
import dsAnimation.HUDInfo;reload(dsAnimation.HUDInfo)

if sys.platform == "linux2":
    sys.path.append('/dsGlobal/dsCore/shotgun/')
    sys.path.append('/dsGlobal/dsCore/maya/common/')
else:
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun/')
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/maya/common/')
    
import dsCommon.dsCollect as dsCollect;reload(dsCollect)
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
    os.environ['SHOT'] = dsShot
    #dsShot = checkCamSeq()
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
    return currentShot

def checkShot():
    dsShot = str(os.getenv('SHOT'))
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

def getRoot():
    filePath = cmds.file(q=True,l=True)[0]
    pathTmp = filePath.split("/")
    newPath = ""

    if re.search("3D",filePath):
        for path in pathTmp:
            if newPath == "":
                newPath = path
            else:
                newPath = newPath + "/" + path
            if re.search("3D",path):
                    break

    if re.search("P:/",newPath):
        newPath = newPath.replace("P:/","vfx-data-server/dsPipe/")
    '''
    if re.search("q[0-9][0-9][0-9][0-9]",filePath):
        for path in pathTmp:
            if newPath == "":
                newPath = path
            else:
                newPath = newPath + "/" + path
            if re.search("q[0-9][0-9][0-9][0-9]",path):
                break
    '''
    return newPath

def test3DPath(path):
    if sys.platform == "linux2":
        if os.path.isdir("/" + path):
            return path
        else:
            newPath = path.replace("/3D","")
            if os.path.isdir("/" + newPath):
                return "/" + newPath
            else:
                print "Path does not exist"
    else:
        return path

def qtShot(shotList,dsEpisode,dsSeq):
    fileName = cmds.file(q=True,sn=True,shn=True)

    fps = cmds.currentUnit( query=True, t=True )    
    
    if fps == "game":fps=15
    if fps == "film":fps=24
    if fps == "pal":fps=25
    if fps == "ntsc":fps=30
    if fps == "show":fps=48
    if fps == "palf":fps=50
    if fps == "ntscf":fps=60    

    x = cmds.getAttr("defaultResolution.width")
    y = cmds.getAttr("defaultResolution.height")
    
    fsList = []
    newPath = getRoot()
    #collectPath = newPath + "/3D/playBlast/collected"

    collectPath = test3DPath(newPath + "/playBlast/quicktime")
    
    for shot in shotList:
        sPBPath = newPath + "/playBlast/" + shot
        sPBPath = test3DPath(newPath + "/playBlast/" + shot)
        ver = dsCollect.getLatest(sPBPath)
        rootPath = sPBPath + "/" + ver
        tl = os.listdir(rootPath)
        for t in tl:
            if not re.search('.ma',t):
                newName = t[0:-9] + ".####" + t[-4:]
                outName = t[0:-9]
        filePath = rootPath + "/" + newName
        fsList.append(filePath)
    fsList.sort()    
   
    input = ' '.join(fsList)
    outputName = '_'.join(fsList)
    if not os.path.isdir(collectPath): os.mkdir(collectPath)
    qtName = dsEpisode + "_" + dsSeq

    fnSplit= fileName.split("_")
    verInt = int(ver[-3:]) + 1   
    newVer = "v%03d" % verInt
    for v in fnSplit:
        if re.search("v[0-9][0-9][0-9]",v):
            verName = v[:-3]
        
    opPath = collectPath +"/"+ dsEpisode + "_" + dsSeq + "_" + newVer + ".mov"

    dsCollect.rvQT(input,fps,x,y,opPath)

def pbCollectShots(shotList):
    fsList = []
    newPath = getRoot()
    for shot in shotList:
        
        if sys.platform == "linux2":
            sPBPath = "/" + newPath + "/playBlast/" + shot
        else:
            sPBPath = "//" + newPath + "/playBlast/" + shot
        ver = dsCollect.getLatest(sPBPath)
        rootPath = sPBPath + "/" + ver
        tl = os.listdir(rootPath)
        for t in tl:
            if not re.search('.ma',t):
                newName = t[0:-9] + ".####" + t[-4:]
        filePath = rootPath + "/" + newName
        fsList.append(filePath)
        
    fsList.sort()    
    rvPathList = ' '.join(fsList)
    dsCollect.rvPush(rvPathList)

def pbCollectAll():
    filePath = cmds.file(q=True,l=True)[0]
    
    pathTmp = filePath.split("/")
    newPath = ""
    
    if re.search("3D",filePath):
        for path in pathTmp:
            if newPath == "":
                newPath = path
            else:
                newPath = newPath + "/" + path
            if re.search("3D",path):
                break
            
    dsCollect.parseLatest(newPath,"playBlast")
    
def pbShot(shot,user):
    global dsShot
    dsShot = shot
    
    filePath = cmds.file(q=True,l=True)[0]
    pathTmp = filePath.split("/")
    setUp()
    HUD()
    startFrame = cmds.shot(dsShot, q=True, st=True)
    endFrame = cmds.shot(dsShot, q=True, et=True)
    cam = cmds.shot(dsShot,q=True,cc=True)
    
    cmds.sequenceManager(currentTime=startFrame)
    
    newPath = getRoot()
    
    ### check and create shot folder in PB
    if sys.platform == "linux2":
        pbPathDir = "/" + newPath + "/playBlast/" + dsShot + "/"
    else:
        pbPathDir = newPath + "/playBlast/" + dsShot + "/"
    
    if not os.path.isdir(pbPathDir):os.makedirs(pbPathDir)
    
    ver = getVersion(pbPathDir)
    ### check and create version folder in PB
    if sys.platform == "linux2":
        pbPath = pbPathDir + ver + "/"
    else:
        pbPath = pbPathDir + ver + "/"
    
    if os.path.isdir(pbPath):
        tmpList = os.listdir(pbPath)
        for file in tmpList:
            os.remove(pbPath + "/" + file)
    else:
        os.makedirs(pbPath)
    pbName = dsSeq + "_" + dsShot 
    
    ### copy maya anim file to the version folder in PB
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
        pbFrames = "//" + pbPath + pbName + "_" + str(pathTmp[-1][:-3]) + "_" + ver
    
    print pbFrames
    
    cmds.setAttr("defaultRenderGlobals.imageFormat",8)
    
    frameRange = range(int(startFrame),int(endFrame) + 1)
    mel.eval('camera -e -displayFilmGate off -displayResolution on -overscan 1.0 ' + cam + ';')
    cmds.playblast(frame=frameRange, orn=True, format='image', cc=True,fo=True, fp=4, st=startFrame, et=endFrame, qlt=100, p=100, f=pbFrames, h=rezY, w=rezX, os=True, v=False)
    mel.eval('camera -e -displayFilmGate off -displayResolution on -overscan 1.0 ' + cam + ';')

    removeHUD()
    tmpList = [dsShot]
    pbCollectShots(tmpList)

    if sys.platform == "linux2":
        imageList = os.listdir("/" + pbPath[:-1] + "/")
        imageList.sort()
        imagePath = pbPath[:-1] + "/" +imageList[1]
    else:
        imageList = os.listdir("//" + pbPath[:-1] + "/")
        imageList.sort()
        imagePath = "//" + pbPath[:-1] + "/" +imageList[1]
    
    print dsShot
    
    sgTools.sgPublishFrames(str(imagePath),str(filePath),'anim',str(user),ver,dsShot)
