
#import maya.cmds as cmds
#import maya.mel as mel

#def dsRenderLocal(start,end):
    #y = start
    #x = end
    #while y <= x:
        #cmds.currentTime(y)
        #mel.eval('renderWindowRender redoPreviousRender renderView;')
        #y = y + 1
        
#sRenderLocal(140,150)

import maya.cmds as cmds
import re

def dominoAlongPath(path,main,dist):
    y = 1
    x = 2000
    uValue = dist
    cmds.group( em=True, name=path + '_grp' )
    cmds.parent(path, path + '_grp' )
    try:
        while y <= x:
            dominObj = cmds.duplicate(main,rr=True,un=True)
            cmds.parent(dominObj,path + '_grp')
            motionObj = cmds.pathAnimation(dominObj, startTimeU=int(y),endTimeU=int(x),fa='X',ua="Y",follow=True,fractionMode=True,followAxis="X",c=curve)
            cmds.cutKey( motionObj, time=(y,x), attribute='uValue' )    
            cmds.setAttr(motionObj+".uValue",uValue)
            uValue = uValue + uValueStart
            y = y + 1
    except:
        pass

def offsetAnim(dominGrp,offset):
    print dominGrp
    grpList = cmds.listRelatives(dominGrp)
    for grp in grpList:
        intList = []
        for i in grp:
            if i.isdigit():
                intList.append(i)
        grpNum = int(''.join(intList))
        #val = grpNum + offset

        FallPos = grp + "|" + cmds.listRelatives(grp)[0] + ".FallPos"
        try:
            cmds.keyframe(FallPos,edit=True,relative=True,timeChange=offset)
        except:
            pass
    
#main = "domino_Grp"
#selGrp  = cmds.ls( selection=True )
#path = selGrp[0]
#dist = .02

#dominoAlongPath(path,main,dist)

selGrp  = cmds.ls( selection=True )
dominGrp = selGrp[0]
offset = 4

offsetAnim(dominGrp,offset)


val = 10
i = 4
frame = 0

while i <= 14:
    print i
    i = i + 1
    frame = frame + 1
#if (frame > domino_Grp1|domino_ctrl.domVal)
#    domino_Grp1|domino_ctrl.FallPos = 1 - .1*frame