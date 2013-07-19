import os,re,subprocess,time
import maya.cmds as cmds
import maya.mel as mel
import itertools as it

## ONly works on windows at the moment... Need to have the realflow top node selected... Can select multipule####
##Usage vrMeshThis() with realflow nodes selected :D
ply2vrmesh = "C:/Program Files/Chaos Group/V-Ray/Maya 2012 for x64/bin/ply2vrmesh.exe"
#VRAY_TOOLS_MAYA2012_x64


def vrmeshMe(inPath,outPath):
    #command line to subprocess
    cmd = ply2vrmesh + " " + inPath + " " + outPath + " -flipNormals -mapChannel 0 -fps 24"
    p = subprocess.Popen(cmd, creationflags = subprocess.CREATE_NEW_CONSOLE)
    return p     
    
def parseMe(path,seqOff,obj,proc):
    # max_load is your amount of process at one time
    max_load = proc
    sleep_interval = 0.5
    pid_list = []
    
    #parse inPath and outPath to 
    roottmp = path.split("/")
    root = path.replace(roottmp[-1],"")
    tmpList = os.listdir(root)
    tmpList.sort()
    frameNum = int(seqOff)
    dstvrMesh = root + "vrMesh"
    if not os.path.exists(dstvrMesh):os.makedirs(dstvrMesh)
    for file in tmpList:
        #if not re.search("Realwave",file):
        if re.search(".bin",file):
            inPath = root + file
            val = "%05d" %(frameNum)
            fileNew = re.sub("_[0-9][0-9][0-9][0-9][0-9].","_" + str(val) + ".",file)
            fileNew = fileNew.replace(".bin",".vrmesh")
            outPath = dstvrMesh + "/" + fileNew
            pid = vrmeshMe(inPath,outPath)
            
            pid_list.append(pid)
            while len(filter(lambda x: x.poll() is None, pid_list)) >= max_load:
                time.sleep(sleep_interval)
                
            frameNum = frameNum + 1
                
    outSplit = outPath.split("/")
    fileSplit = outSplit[-1].split("_")
    rootPath = outPath.replace(fileSplit[-1],"%05d")
    rootPath = rootPath + ".vrmesh"
    createVrMesh(obj+"_vrMesh",rootPath)

def vrMeshThis(proc):
    #take realFLow object and vrayProxy it.
    objList = cmds.ls(selection=True)
    for obj in objList:
        objShape = cmds.listRelatives( obj, shapes=True )
        objSelect = obj
        rfSource = cmds.listConnections(objShape[0] + ".inMesh")
        obj = rfSource[0]
        path = cmds.getAttr(obj+".Path")
        seqOff = cmds.getAttr(obj+".Offset")
        stackPath = path.replace("00000","*")
        parseMe(path,seqOff,objSelect,proc)

def vrMeshAll(proc):
    #list and convert all Realflow objects to vrayProxy
    rfObject = cmds.ls(type='RealflowMesh')   
    for obj in rfObject:
        path = cmds.getAttr(obj+".Path")
        seqOff = cmds.getAttr(obj+".Offset")
        stackPath = path.replace("00000","*")
        parseMe(path,seqOff,obj,proc)
        
def createVrMesh(name,path):
    #add the final converted vray proxy to your secene
    mel.eval('vrayCreateProxyExisting("'+name+'", "' + path + '");')
        
#vrMeshThis(12)