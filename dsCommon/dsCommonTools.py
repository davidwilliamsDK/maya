import maya.cmds as cmds
import re



def playbackToShot():
    # takes plaback range and filename in this format q####_anim_hero.ma and creates shot with current camera
    shotNodeList = []
    shotNodeList_tmp = cmds.ls(type="shot")

    filePath = cmds.file(q=True,l=True)[0]
    fileSplit = filePath.split("/")
    nameSplit = fileSplit[-1].split("_")
    dsShot = nameSplit[0]

    for s in shotNodeList_tmp:
        if re.search("s[0-9][0-9][0-9][0-9]",s):
            shotNodeList.append(s)

    if shotNodeList == []:
        startVal = int(cmds.playbackOptions(q=True,minTime=True))
        endVal = int(cmds.playbackOptions(q=True,maxTime=True))
        pbPanel = cmds.getPanel( withFocus=True )
        activeCam = cmds.modelEditor(pbPanel,q=True,cam=True)
        myShot = cmds.shot(dsShot, st=startVal, et=endVal)
        cmds.shot(myShot, e=True, sst=startVal, set=endVal)
        cmds.shot(myShot, e=True, cc=activeCam)


def cameraWork():
    camList = cmds.ls(type="camera")
    pbPanel = cmds.getPanel( withFocus=True )
    activeCam = cmds.modelEditor(pbPanel,q=True,cam=True)

    camShape = cmds.listRelatives(activeCam)[0]
    print camShape

    for cam in camList:
        if cam != camShape:
            try:
                cmds.setAttr(cam + ".renderable",0)
                cmds.setAttr(cam + ".displayGateMask",0)
                print cam
            except:
                pass
        else:
            cmds.setAttr(cam + ".renderable",1)
            cmds.setAttr(cam + ".displayGateMask",1)
            print cam

def renderFix():

    cmds.setAttr ('defaultRenderGlobals.currentRenderer', "vray", type = "string" )
    cmds.setAttr('vraySettings.imageFormatStr', 'exr (multichannel)', type='string')
    cmds.setAttr("vraySettings.width", 1920)
    cmds.setAttr("vraySettings.height",1080)
    cmds.setAttr("vraySettings.aspectRatio", 1.777)


def consolidateShaders(mainMat_sel):

    mainMatSG = None
    matList = cmds.ls(materials=True, r=True)

    mainMatSplit = mainMat_sel.split(":")
    mainMat = mainMatSplit[-1]
    try:
        tmpList = cmds.listConnections(mainMat_sel)
        
        mainSplit = mainMat_sel.split(":")
        matVal = mainSplit[-1]
            
        for t in tmpList:
            if re.search("SG",t):
                mainMatSG = t
                break
                
        matList.sort()
        
        if mainMatSG != None:
            for m in matList:
                if m.split(":")[-1] == matVal:
                    cmds.select(m)
                    cmds.hyperShade(objects="")
                    cmds.sets( e=True, forceElement= mainMatSG )
                    
                    if m != mainMat_sel:
                        cmds.delete(m)
    except:
        pass

def getMaterials():
    headList = []
    slList = cmds.ls(materials=True, r=True)
    for sl in slList:
        shadeSplit = sl.split(":")
        if shadeSplit[-1] not in headList:
            headList.append(shadeSplit[-1])
            
    for head in headList:
        for sl in slList:
            if re.search(head,sl):
                print sl
                consolidateShaders(sl)
    
#getMaterials()





def cFF():
    playbackToShot()
    cameraWork()
    renderFix()