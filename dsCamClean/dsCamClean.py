import maya.cmds as cmds
import re

def newGrp(name):
    #Create a clean group
    try:
        cmds.select(name)
    except:
        cmds.sphere(n="temp")
        cmds.group("temp",n = name,world=True)
        cmds.delete("temp")

def camDict():
    list = []
    seqShots = cmds.sequenceManager(listShots=True)
    
    for each in seqShots:
        startFrame = cmds.getAttr(each+".startFrame")
        endFrame = cmds.getAttr(each+".endFrame")
        dict = {'shot': each, 'camera' : cmds.shot(each, q=True, cc = True), 'startFrame': int(startFrame), 'endFrame': int(endFrame)};
        list.append(dict)
    return list

def cleanCam(list):
    #Dupplicate, group, unlock, parentConstrain cameras
    for each in list:
        dict = each
        cam = dict['camera']
        cam = re.sub(r'Shape','',cam)
        start = dict['startFrame']
        end = dict['endFrame']
        shotName = dict['shot']
        newCam = cam+"_Clean"
        newCamShape = cam+"_CleanShape"
        cmds.duplicate(cam,n = newCam,rc=True)
        cmds.parent(newCam,"exportCam_Grp") 
        cmds.setAttr(newCam+".tx", lock=False )
        cmds.setAttr(newCam+".ty", lock=False )
        cmds.setAttr(newCam+".tz", lock=False )
        cmds.setAttr(newCam+".rx", lock=False )
        cmds.setAttr(newCam+".ry", lock=False )
        cmds.setAttr(newCam+".rz", lock=False )
        cmds.setAttr(newCamShape+".hfa", lock=False )
        cmds.setAttr(newCamShape+".vfa", lock=False )
        cmds.setAttr(newCamShape+".fl", lock=False )
        cmds.setAttr(newCamShape+".lsr", lock=False )
        cmds.setAttr(newCamShape+".fs", lock=False )
        cmds.setAttr(newCamShape+".fd", lock=False )
        cmds.setAttr(newCamShape+".sa", lock=False )
        cmds.setAttr(newCamShape+".coi", lock=False )
        cmds.connectAttr( cam+".hfa", newCamShape+".hfa" )
        cmds.connectAttr( cam+".vfa", newCamShape+".vfa" )
        cmds.connectAttr( cam+".fl", newCamShape+".fl" )
        cmds.connectAttr( cam+".lsr", newCamShape+".lsr" )
        cmds.connectAttr( cam+".fs", newCamShape+".fs" )
        cmds.connectAttr( cam+".fd", newCamShape+".fd" )
        cmds.connectAttr( cam+".sa", newCamShape+".sa" )
        cmds.connectAttr( cam+".coi", newCamShape+".coi" )
        cmds.parentConstraint( cam, newCam )
        cmds.bakeResults( newCam, t=(start,end), sb=1, at=["tx","ty","tz","rx","ry","rz"])
        cmds.bakeResults( newCamShape, t=(start,end), sb=1, at=["hfa","vfa","fl","lsr","fs","fd","sa","coi"])
        #remove parentContrain
        cmds.delete(newCam+"_parentConstraint1")
        cmds.shot(shotName, e=True, cc = newCam )
        
def selectCamSeq(list):
    selectList = []
    for each in list:
        dict = each
        newCam = dict['camera']
        shotName = dict['shot']
        selectList.append(shotName)
        selectList.append(newCam)
        selectList.append("sequencer1")
    return selectList
    
def exportCam(selectList):
    print selectList
    cmds.file( '/home/admin/betty.mb', type='mayaBinary', namespace='rubble', er=True )

def camClean():
    newGrp("exportCam_Grp")
    list = camDict()
    cleanCam(list)
    selectList = selectCamSeq(list)
    exportCam(selectList)
    
camClean()

cmds.file(q=True, expandName=True)