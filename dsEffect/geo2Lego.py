'''
Only works with the asset we created...
'''

import maya.cmds as cmds

obj = cmds.ls(selection=True)
objShape = cmds.listRelatives( obj, shapes=True )

val = objShape[-1] + ".worldMesh[0]"

try:
    cmds.connectAttr( val, 'bound1.inGeometry',f=True )
except:
    print "could not connect \n" + val + "\n to bound1.inGeometry" 
    
try:
    cmds.connectAttr( val, 'scatterShape1.inWorldMatrix',f=True )
except:
    print "could not connect \n" + val + "\n to scatterShape1.inWorldMatrix" 
    
try:
    cmds.connectAttr( val, 'scatterShape1.inGeometry',f=True )
except:
    print "could not connect \n" + val + "\n to scatterShape1.inGeometry"
    
    
    
import maya.cmds as cmds


def reCenterPivot(obj):
    locName = obj + "_loc"
    
    cmds.spaceLocator(n=locName )
    cmds.parent( locName, obj )
    
    cmds.setAttr(locName + ".translateX",0)
    cmds.setAttr(locName + ".translateY",0)
    cmds.setAttr(locName + ".translateZ",0)
    cmds.setAttr(locName + ".rotateX",0)
    cmds.setAttr(locName + ".rotateY",0)
    cmds.setAttr(locName + ".rotateZ",0)
    
    cmds.Unparent(locName)
    pConst = cmds.parentConstraint(obj,locName,mo=True,w=1)
    
    cmds.bakeResults(locName,sm=True, t=(0,44),at=["tx","ty","tz","rx","ry","rz"])
    cmds.delete(pConst)
    newObj = cmds.duplicate(obj,n=obj+"_new")

    cmds.xform(newObj[0],cp=True)
    nConst = cmds.parentConstraint(locName,newObj, mo=True,w=1)
    
    cmds.bakeResults(newObj,sm=True, t=(0,44),at=["tx","ty","tz","rx","ry","rz"])
    
    cmds.delete(nConst)
    cmds.delete(locName)
    
    
obj = cmds.ls(selection=True)

for o in obj:
    reCenterPivot(o)
 