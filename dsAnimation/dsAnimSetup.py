#import maya.cmds as cmds
import os, ast, shutil
import dsAnimSG as animSG
import dsAnimUtil as animUtil
import dsCommon.dsProjectUtil as projectUtil
import dsCommon.dsOsUtil as dsOsUtil
import dsSgUtil as sgBridge
import dsCommon.dsMetaDataTools as dsMDT
reload(dsMDT)
reload(sgBridge)
reload(animSG)
reload(animUtil)
reload(projectUtil)

if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.mel as mel

os.environ['PATH'] = "%PATH%;C:/Program Files/Autodesk/Maya2013/bin/"
os.environ['PYTHONPATH']="%PYTHONPATH%;//vfx-data-server/dsGlobal/dsCore/maya;//vfx-data-server/dsGlobal/globalMaya/Resources/PyQt_Win64;//vfx-data-server/dsGlobal/globalResources/Shotgun;//vfx-data-server/dsGlobal/dsCore/shotgun;"
os.environ['MAYA_SCRIPT_PATH']="%MAYA_SCRIPT_PATH%;//vfx-data-server/dsGlobal/globalMaya/Mel;C:/Program Files/Autodesk/Maya2013/scripts/others;C:/Program Files/Autodesk/Maya2013/mentalray/scripts"

#Ressource Files
emptyMA = 'U:\\globalMaya\\Resources\\emptyScene.ma'
emptyREF = 'U:/globalMaya/Resources/emptyRef.mb'
logPath = 'C:\\log.txt'
prefferedAssetTag = 'Anim'
preffedSaveTag = '/3D/template/'
ext = ".mb"
camGrp = "Cam_Grp"
assetGrp = "Asset_Grp"
prefferedFileTag = 'template'
shotgunTaskTemplate = 'sceneSetupTemplate'
grpExt= "_Grp"

errorLog = []

def handler(projInfo):
    projInfo = stringToDict(projInfo)
    #set fps, resolution, render software
    filmInfo = animSG.getEpisodeInfo(projInfo)
    setSceneSpecs(filmInfo)

    #Set RenderSettings
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "vray", type="string")
    if not cmds.objExists('vraySettings'):
        cmds.createNode("VRaySettingsNode", n="vraySettings")
    cmds.setAttr('vraySettings.width', 1920)
    cmds.setAttr('vraySettings.height', 1280)
    cmds.setAttr('vraySettings.aspectRatio', 1.777)

    #get sequence shots from shotgun
    shots = animSG.getSequenceShots(projInfo['sequenceName'], projInfo['projName'], projInfo['episode'])

    #create cams
    shots = animUtil.createCams(shots, camGrp)

    #create cam sequences
    sequences = animUtil.createCamSequencer(shots)

    #get linked assets from shotgun
    try:
        assets = animSG.getSequenceAssets(projInfo['sequenceName'], projInfo['projName'], projInfo['episode'])
        refAsset(assets, projInfo, assetGrp)
    except:
        errorLog.append({"Warning Level": 1, "ERROR": "Could not Ref Assets"})

    #Save File
    filePath = savefile(projInfo)

    #Set META DATA
    dsMDT.createMDscriptNode()

    cmds.file( save=True, type='mayaAscii' )


    #Shotgun Update
    #Create Task in shotgun
    seqs = sgBridge.sgGetSeqTasks(int(projInfo["sequenceId"]), ['content'])
    createTask = True
    id = None
    for seq in seqs:
        if str(seq['content']) == prefferedFileTag:
            createTask = None
            id = int(seq['id'])

    if createTask:
        sgBridge.setSequenceTemplate(int(projInfo["sequenceId"]), shotgunTaskTemplate)

    #Update Status in shotgun
    if id == None:
        seqs = sgBridge.sgGetSeqTasks(int(projInfo["sequenceId"]), ['content'])
        for seq in seqs:
            if str(seq['content']) == prefferedFileTag:
                id = int(seq['id'])

    projObj= sgBridge.getProjectID(str(projInfo["projName"]))
    seqObj = {'type': 'Sequence', 'id': int(projInfo["sequenceId"])}
    taskObj ={'type': 'Task', 'id': id}

    #Error Logging + Update Shotgun
    if errorLog == []:
        sgBridge.sgSetSeqTaskStatus(id, "fin")
        print "No Errors occured doing Setup"
    else:
        warningLevel = 2
        for log in errorLog:
            print log
            if int(log["Warning Level"]) == 1:
                warningLevel = 1
                break
        if warningLevel == 1:
            sgBridge.sgSetSeqTaskStatus(id, "cor")
        else:
            sgBridge.sgSetSeqTaskStatus(id, "rend")

        subject = "ERROR LOG"
        content = "ERRORS: %s" % errorLog
        noteInfo = sgBridge.sgAddSeqNote(subject, content, taskObj, seqObj, projObj)

        print "%s Error(s) occured doing the Setup, Please Check Errors!" % len(errorLog)

    print projInfo

def setSceneSpecs(filmInfo):
    print filmInfo['sg_fps']
    if str(filmInfo['sg_fps']) == "24":
        cmds.currentUnit(time='film')
    if str(filmInfo['sg_fps']) == "25":
        cmds.currentUnit(time='pal')

    try:
        cmds.setAttr("vraySettings.width", 1920)
        cmds.setAttr("vraySettings.height", 1080)
    except:
        pass

def refAsset(assets, projInfo, assetGrp):
    if not cmds.objExists(assetGrp):
        cmds.group(em=True, n=assetGrp)

    cmds.select(all=True)
    topN = cmds.ls(sl=True, type="transform")

    #Create Assets Refs
    for asset in assets:
        assetInfo = animSG.getAssetAttr(asset)
        refPath = projectUtil.listAssetRefPath(projInfo['projName'], assetInfo['sg_asset_type'], assetInfo['sg_subtype'], assetInfo['code'])

        ref = refFile(refPath, assetInfo['code'])
        if not os.path.exists(ref):
            print emptyREF
            if os.path.exists(emptyREF):
                #IF NO REF EXIST MAKE IT AND SEND ERROR WARNING
                errorLog.append({"Warning Level": 2, "ERROR": "%s, no Publish Found" % asset})
                #errorLog.append("%s, no Publish Found" % asset)
                shutil.copyfile(str(emptyREF), str(ref))

        if os.path.exists(ref):
            cmds.file(ref, r=True, type="mayaBinary", gl=True, loadReferenceDepth="all", shd=["displayLayers", "shadingNetworks", "renderLayersByName"], namespace=assetInfo['code'], options="v=0")

            #Clean up scene
            cmds.select(all=True)
            nodes = cmds.ls(sl=True, type="transform")
            newNodes = list(set(nodes) - set(topN))

            if not assetInfo['sg_asset_type'][0].isdigit():
                grp = "%s%s" % (assetInfo['sg_asset_type'], grpExt)
            else:
                grp = "%s%s" % (assetInfo['sg_subtype'], grpExt)

            if not cmds.objExists(grp):
                if not assetInfo['sg_asset_type'][0].isdigit():
                    grp = cmds.group(em=True, n="%s%s" % (assetInfo['sg_asset_type'], grpExt))
                else:
                    grp = cmds.group(em=True, n="%s%s" % (assetInfo['sg_subtype'], grpExt))

                cmds.parent(grp, assetGrp)
            cmds.parent(newNodes, grp)

def refFile(refPath, assetName):
    if os.path.exists(refPath):
        print "ref path does exist"
        prefferedRef = "%s%s_%s%s" % (refPath, assetName, prefferedAssetTag,ext)
        print prefferedRef
        if os.path.exists(prefferedRef):
            return prefferedRef
            print "preffered asset exists"
        else:
            return prefferedRef
            print "asset does not exist find another"
            #Check for other files in ref path
            #Decide which one to use
            #if no refs in path create empty file with preffered asset ref name.

def stringToDict(string=None):
    if string:
        dict = string.rsplit('}')[0].split('{')[-1]
        dict = dict.replace(" ", "")
        dict = dict.split(",")
        newDict = {}
        for entry in dict:
            entry = entry.split(":")
            newDict[entry[0]] = entry[1]
        return newDict

def savefile(projInfo):
    seqPath = projectUtil.seqAnimPath(projInfo['projName'], projInfo['episode'], projInfo['sequenceName'])
    path = '%s%s' % (seqPath, preffedSaveTag)

    if not os.path.exists(path):
        os.mkdir(path)

    saveAs = '%s%s_%s.ma' % (path, projInfo['sequenceName'],  prefferedFileTag)
    print saveAs
    cmds.file( rename=saveAs )
    return saveAs

def launch(projInfo):
    info = {}
    if os.path.exists(emptyMA):
        #FOR SEQUENCE WORKFLOW
        if "sequences" in projInfo:
            print projInfo['sequences']
            for sequence in projInfo['sequences']:
                seq = str(sequence)
                info['projName'] = projInfo['projName']
                info['episode'] = projInfo['episode']

                info['sequenceName'] = seq.split("_")[0]
                info['sequenceId'] = int(seq.split("_")[1])
                melCmd = ('source animBatchSetup; cleanMaya "%s";' % (str(info)))
                print "printing mel commands"
                print melCmd

                #Finding LOG save path
                logPath = "C:\\%s_log.txt" % (info['sequenceName'])

                os.system("maya -batch -log '%s' -command '%s' -file '%s'" % (logPath, str(melCmd), emptyMA))
                #os.system("maya -log '%s' -command '%s' -file '%s'" % (logPath, str(melCmd), emptyMA))
            print "Run Selected Sequences"

        if "shots" in projInfo:
            print "Run Selected Shots"
        if not "sequences" or "shots" in projInfo:
            print "Run Whole Episode"

        print "is running launch"