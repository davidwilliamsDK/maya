import dsCommon.dsOsUtil as dsOsUtil
if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds

def createCams(shotData, camGrp):
    if not cmds.objExists(camGrp):
        cmds.group(em=True, n=camGrp)

    #CreateCams
    for shot in shotData:
        name = shot['code']
        cam = cmds.camera()
        cmds.rename(cam[0], 'cam_%s' % name)
        cam = cmds.ls(sl=True, type='transform')[0]
        print cam
        cmds.parent(cam, camGrp)
        shot['cam_name'] = cam

        #setCamSettings
        camShape = cmds.listRelatives(cam, children=True)[0]
        cmds.camera(cam, e=True, displayFilmGate=False, displayResolution=True, overscan=1.3)
        cmds.setAttr("%s.displayGateMaskColor" % camShape, 0, 0, 0, type="double3")
        cmds.setAttr("%s.displayGateMaskOpacity" % camShape, 1)

    return(shotData)

def createCamSequencer(shotData, handle=25):
    i = 0
    for shot in shotData:
        cutIn = shot['sg_cut_in']
        cutOut = shot['sg_cut_out']
        if handle:
            offset = i * handle
            print cutIn
            print cutOut
            cutIn = cutIn + offset
            cutOut = cutOut + offset
            i = i + 1
        print shot['cam_name']
        cmds.shot(shot['code'], startTime=cutIn, endTime=cutOut, sequenceStartTime=cutIn, sequenceEndTime=cutOut, currentCamera=shot['cam_name'])
