import os,re,subprocess
import maya.cmds as cmds
import maya.mel as mel


## ONly works on windows at the mooment... Need to have the realflow top node selected... Can select multipule####
##Usage vrMeshThis() with realflow nodes selected :D
ply2vrmesh = "C:/Program Files/Chaos Group/V-Ray/Maya 2012 for x64/bin/ply2vrmesh.exe"

def vrmeshMe(inPath,outPath):
    cmd = ply2vrmesh + " " + inPath + " " + outPath + " -flipNormals"
    p = subprocess.Popen(cmd, creationflags = subprocess.CREATE_NEW_CONSOLE)
    #p.wait()
    
def parseMe(path,seqOff,obj):
    roottmp = path.split("/")
    root = path.replace(roottmp[-1],"")
    tmpList = os.listdir(root)
    tmpList.sort()
    frameNum = int(seqOff)
    dstvrMesh = root + "vrMesh"
    if not os.path.exists(dstvrMesh):os.makedirs(dstvrMesh)
    for file in tmpList:
        if not re.search("Realwave",file):
            if re.search(".bin",file):
                inPath = root + file
                val = "%05d" %(frameNum)
                fileNew = re.sub("_[0-9][0-9][0-9][0-9][0-9].","_" + str(val) + ".",file)
                fileNew = fileNew.replace(".bin",".vrmesh")
                outPath = dstvrMesh + "/" + fileNew
                vrmeshMe(inPath,outPath)
                frameNum = frameNum + 1
    outSplit = outPath.split("/")
    fileSplit = outSplit[-1].split("_")
    rootPath = outPath.replace(fileSplit[-1],"%05d")
    rootPath = rootPath + ".vrmesh"
    createVrMesh(obj+"_vrMesh",rootPath)

def vrMeshThis():
    objList = cmds.ls(selection=True)
    for obj in objList:
        objShape = cmds.listRelatives( obj, shapes=True )
        objSelect = obj
        rfSource = cmds.listConnections(objShape[0] + ".inMesh")
        obj = rfSource[0]
        path = cmds.getAttr(obj+".Path")
        seqOff = cmds.getAttr(obj+".Offset")
        stackPath = path.replace("00000","*")
        parseMe(path,seqOff,objSelect)

def vrMeshAll():
    rfObject = cmds.ls(type='RealflowMesh')   
    for obj in rfObject:
        path = cmds.getAttr(obj+".Path")
        seqOff = cmds.getAttr(obj+".Offset")
        stackPath = path.replace("00000","*")
        parseMe(path,seqOff,)
        
def createVrMesh(name,path):
    mel.eval('vrayCreateProxyExisting("'+name+'", "' + path + '");')
        
#vrMeshThis()