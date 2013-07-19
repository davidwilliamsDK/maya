import os,sys,re,subprocess

'''
import dsCommon.dsMetaDataTools as dsMDT
reload(dsMDT)

dsMDT.testMDNode()

update new ref's
dsMDT.addReferences()

dsMDT.addShots()

'''

import dsCommon.dsOsUtil as dsOsUtil
if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds

if sys.platform == 'linux2':
    sys.path.append('/dsGlobal/dsCore/shotgun')
else:
    sys.path.append('//192.168.0.161/dsGlobal/dsCore/shotgun')
import sgTools

def sceneCheck():
    sgTask = cmds.getAttr("dsMetaData.sgTask")
    tmpPath = cmds.file(q=True,l=True)[0]

    if not re.search(sgTask,tmpPath):
        try:
            updatedsMD()
            "dsMetaData node updated... please save"
            save = cmds.file(save=True, force=True)
        except:
            pass
        
def versionCheck():
    currentHeroVersion = cmds.getAttr("dsMetaData.Version")
    currentTask = cmds.getAttr("dsMetaData.sgTask")
    
    parsePath()
    projName = '%s' % os.getenv('PROJECT')
    epiName = '%s' % os.getenv('EPISODE')
    seqName = '%s' % os.getenv('SEQUENCE')
    shot = '%s' % os.getenv('SHOT')
    
    fullPath = cmds.file(q=True,sn=True)
    fileName = cmds.file(q=True,sn=True,shn=True)
    
    rootTaskPath = fullPath.replace(fileName,"")
    
    print rootTaskPath
    
    print rootTaskPath + "version/" + fileName
    
    

def initMDNode():
    if cmds.ls("dsMetaData"):
        cmds.delete("dsMetaData")
        createMDscriptNode()
    else:
        print "create"
        createMDscriptNode()

def testMDNode():
    if not cmds.ls("dsMetaData"):
        createMDscriptNode()
    else:
        print "dsMD node Present"

def createMDscriptNode():
    dsMetaDataScriptNode = cmds.scriptNode( st=1, bs='import dsCommon.dsMetaDataTools as dsMDT;reload(dsMDT);dsMDT.sceneCheck()', n='dsMetaData', stp='python')
    dsMDCreate() # creates sequence level attr's
    createShotAttrs()
    updatedsMD()
    #addReferences()

def dsMDCreate():
    cmds.select('dsMetaData')
    if not cmds.attributeQuery('Project',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='proj', longName='Project', dt='string',h=False,r=True)

    if not cmds.attributeQuery('Episode',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='epi', longName='Episode', dt='string',h=False,r=True)

    if not cmds.attributeQuery('Sequence',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='seq', longName='Sequence', dt='string',h=False,r=True)

    if not cmds.attributeQuery('sgSeqID',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='seqID', longName='sgSeqID', at='long',h=False,r=True)

    if not cmds.attributeQuery('sgTask',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='Task', longName='sgTask', dt='string',h=False,r=True)

    if not cmds.attributeQuery('sgTaskID',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='TaskID', longName='sgTaskID', dt='string',h=False,r=True)

    if not cmds.attributeQuery('FPS',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='FPS', longName='FPS', at='long',h=False,r=True)

    if not cmds.attributeQuery('ResolutionWidth',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='rezW', longName='ResolutionWidth', at='long',h=False,r=True)

    if not cmds.attributeQuery('ResolutionHeight',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='rezH', longName='ResolutionHeight', at='long',h=False,r=True)

    if not cmds.attributeQuery('User',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='dude', longName='User', dt='string',h=False,r=True)

    if not cmds.attributeQuery('Version',node="dsMetaData",ex=True):
        cmds.addAttr( shortName='ver', longName='Version', dt='string',h=False,r=True)

def parsePath():

    match = re.search('(?P<relative>.*)\/(?P<project>\w*)\/film\/(?P<episode>\w*)\/(?P<sequence>\w*)\/(?P<shot>\w*)', cmds.file(q=True,l=True)[0])

    if match:
        match = match.groupdict()
        relativePath = match['relative'];os.environ['RELATIVEPATH'] = relativePath
        project = match['project'];os.environ['PROJECT'] = project
        episode = match['episode'];os.environ['EPISODE'] = episode
        sequence = match['sequence'];os.environ['SEQUENCE'] = sequence
        shot = match['shot'];os.environ['SHOT'] = shot

def updatedsMD():
    fullPath = cmds.file(q=True,sn=True)
    fileName = cmds.file(q=True,sn=True,shn=True)

    pathTmp = fullPath.split("/")

    parsePath()
    projName = '%s' % os.getenv('PROJECT')
    epiName = '%s' % os.getenv('EPISODE')
    seqName = '%s' % os.getenv('SEQUENCE')
    shot = '%s' % os.getenv('SHOT')

    ''' log on to shotgun and get sequence id frame rate and resolution'''
    epiOBJ = sgTools.sgGetEpisode(epiName,projName,['sg_fps','sg_resolution'])
    fps = int(epiOBJ['sg_fps'])
    rez = epiOBJ['sg_resolution']
    rSplit = rez.split("x")
    rezW = int(rSplit[0])
    rezH = int(rSplit[-1])
    seq = sgTools.sgGetSequence(seqName,projName,epiName,['id'])
    seqID = seq['id']

    tasks = sgTools.sgGetSeqTasks(seqID,['step','content','id'])

    if re.search("3D",fullPath):
        for index, obj in enumerate(pathTmp):
            if obj == "3D":
                next = pathTmp[index + 1]
        task = next
    else:
        for index, obj in enumerate(pathTmp):
            if re.search("q[0-9][0-9][0-9][0-9]",obj):
                next = pathTmp[index]
        task = next

    for t in tasks:
        if t['step']['name'] == task:
            seqTaskID = t['id']
            taskID = t['step']['id']
            break
        else:
            seqTaskID = "none"

    try:
        userOBJ = sgTools.sgGetTask(taskID,['task_assignees','entity'])
        user =  userOBJ['task_assignees'][0]['name']
        if str(user) == "Shotgun Support":
            user = "not assigned"
        version = "v001"
    except:
        user = "not assigned"
        version = "v000"

    cmds.setAttr('dsMetaData.Project',projName,type="string")
    cmds.setAttr('dsMetaData.Episode',epiName,type="string")
    cmds.setAttr('dsMetaData.Sequence',seqName,type="string")
    cmds.setAttr('dsMetaData.sgSeqID',seqID)
    cmds.setAttr('dsMetaData.Task',task,type="string")
    cmds.setAttr('dsMetaData.sgTaskID',str(seqTaskID),type="string")
    cmds.setAttr('dsMetaData.FPS',fps)
    cmds.setAttr('dsMetaData.ResolutionWidth',rezW)
    cmds.setAttr('dsMetaData.ResolutionHeight',rezH)
    cmds.setAttr('dsMetaData.User',user,type="string")
    cmds.setAttr('dsMetaData.Version',version,type="string")

    shotList = cmds.ls(type = "shot")
    
    for dsShot in shotList:
        if re.search("s[0-9][0-9][0-9][0-9]",dsShot):
            updateShotAttrs(dsShot,task,seqID,seqName,projName,epiName)

def updateShotAttrs(dsShot,task,seqID,seqName,projName,epiName):
    dsTask = task
    startVal = cmds.shot(dsShot, q=True, st=True)
    endVal = cmds.shot(dsShot, q=True, et=True)
    shotDur = cmds.shot(dsShot,q=True,sd=True)
    camVal = cmds.shot(dsShot,q=True,cc=True)

    ## TALK TO SHOTGUN ##
    seqObj = sgTools.sgGetSequence(seqName,projName,epiName,['shots','id'])
    shotObj = seqObj['shots']

    """ remove name spaces"""
    if re.search(":",dsShot):
        sSplit = dsShot.split(":")
        dsShot = sSplit[-1]

    for shot in shotObj:

        if str(shot['name']) == str(dsShot):
            shotID = shot['id']
            break
        else:
            shotID = 0

    ## TALK TO SHOTGUN ##
    shotTasks = sgTools.sgGetShotTasks(shotID,["step","content"])

    for t in shotTasks:
        if str(t['step']['name']) == str(task):
            shotTaskID = t['id']
            taskID = t['step']['id']
            break
        else:
            shotTaskID = 000000

    ## TALK TO SHOTGUN ##
    try:
        userOBJ = sgTools.sgGetTask(shotTaskID,['task_assignees','entity'])
        user =  userOBJ['task_assignees'][0]['name']
        version = "v000"
    except:
        user = "not assigned"
        version = "none"

    cmds.setAttr('dsMetaData.'+str(dsShot)+'_shotID',shotID)
    cmds.setAttr('dsMetaData.'+str(dsShot)+'_shotStart',startVal)
    cmds.setAttr('dsMetaData.'+str(dsShot)+'_shotEnd',endVal)
    cmds.setAttr('dsMetaData.'+str(dsShot)+'_shotTaskName',dsTask,type="string")
    cmds.setAttr('dsMetaData.'+str(dsShot)+'_shotTaskID',shotTaskID)
    cmds.setAttr('dsMetaData.'+str(dsShot)+'_User',user,type="string")

def connectReferences(dsMDNode,reference,refFile):
    if cmds.objExists(reference + ":Geo_Grp.dsMD"):
        cmds.connectAttr(reference + ":Geo_Grp.dsMD", "dsMetaData." + dsMDNode)
    else:
        cmds.addAttr(reference + ":Geo_Grp",at="message",ln="dsMD")
        cmds.connectAttr(reference + ":Geo_Grp.dsMD", "dsMetaData." + dsMDNode)

    cmds.connectAttr(reference+":Rig_Grp.assetID","dsMetaData." + dsMDNode + "_assetID")

    cmds.setAttr("dsMetaData." + dsMDNode + "_version",refFile + "_v001",type="string")
    #cmds.connectAttr(reference+":Rig_Grp.version","dsMetaData." + dsMDNode + "_version")

def addReferences():
    cmds.select("dsMetaData")
    shotList = cmds.ls(type = "shot")
    refList = cmds.ls(rf=True)
    for shot in shotList:
        
        """ skips namespaces"""
        if re.search(":",shot):
            sSplit = shot.split(":")
            shot = sSplit[-1]
        
        for ref in refList:
            if cmds.referenceQuery(ref,n=True,dp=True) != None:
                refNs = cmds.referenceQuery(ref,ns=True,shn=True)
                refN = cmds.referenceQuery(ref,f=True,shn=True)
                
                print refNs
                print refN
                
                if not cmds.objExists("dsMetaData." + str(shot) + "_" + refNs):
                    cmds.addAttr(ln= str(shot) + "_" + refNs, at="message", h=False,r=True)
                    cmds.addAttr(ln= str(shot) + "_" + refNs + "_viz", at='bool', h=False,r=True)
                    cmds.addAttr(ln= str(shot) + "_" + refNs + "_assetID",at="long",h=False,r=True)
                    cmds.addAttr(ln= str(shot) + "_" + refNs + "_version",dt="string",h=False,r=True)
                    connectReferences(str(shot)+ "_" + refNs,refNs,refN)

def createShotAttrs():
    shotList = cmds.ls(type = "shot")
    for shot in shotList:
        
        """ skips namespaces"""
        if re.search(":",shot):
            sSplit = shot.split(":")
            shot = sSplit[-1]
            
        if not cmds.objExists("dsMetaData."+ str(shot) + "_shotID"):
            if re.search("s[0-9][0-9][0-9][0-9]",shot):
                cmds.addAttr( ln= str(shot) + '_shotID', at='long', h=False,r=True)
                cmds.addAttr( ln= str(shot) + '_shotStart', at='long', h=False,r=True)
                cmds.addAttr( ln= str(shot) + '_shotEnd',  at='long', h=False,r=True)
                cmds.addAttr( ln= str(shot) + '_shotTaskName',  dt='string', h=False,r=True)
                cmds.addAttr( ln= str(shot) + '_shotTaskID',  at='long', h=False,r=True)
                cmds.addAttr( ln= str(shot) + '_User', dt='string', h=False,r=True)
                cmds.addAttr( ln=str(shot)  + '_singleFrame', at='bool', h=False,r=True)
