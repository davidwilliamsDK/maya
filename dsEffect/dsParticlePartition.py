import maya.cmds as cmds
import maya.mel as mel
import random,os,re

def dsPartition(partitions,start,end):
    
    filename = cmds.fileDialog2(fileMode=2, ds=1,caption="select Folder")
    path =  filename[0]
    path = path.replace("\\","//")
    
    rootPath = path
    
    mel.eval('realflowBINExportDialog 0;')
    mel.eval('deleteUI window1;')
    objList = cmds.ls(selection=True)
    
    for obj in objList:
        path = rootPath + obj + "/"
        objShape = cmds.listRelatives( obj, shapes=True )
        sParticle = obj
        part = 1
        while part <= partitions:
            newPath = path + "/" + "v%03d" %(part)
            if not os.path.isdir(path):os.mkdir(path)
            if not os.path.isdir(newPath):os.mkdir(newPath)
            cmds.setAttr(sParticle + ".seed[:0]", int(random.randint(part,1000)))
            
            cmds.setAttr("realflowBINExportOptions.path",newPath,type="string")
            cmds.setAttr("realflowBINExportOptions.prefix","<name>.",type="string")
            cmds.setAttr("realflowBINExportOptions.nameFormat",1)
            cmds.setAttr("realflowBINExportOptions.padding",4)
            cmds.setAttr("realflowBINExportOptions.particleType",2)
            cmds.setAttr("realflowBINExportOptions.usePlaybackRange",1)
            cmds.setAttr("realflowBINExportOptions.nodes[0]",sParticle,type="string")
            mel.eval('realflowBINExportLastSettings 0;')
            print part
            part = part + 1



def furyGroup(grpName):
    sParticleList = []
    furyList = cmds.ls(type="FuryEmitter")
    for fury in furyList:
        conList = cmds.listConnections(fury+".output[0]")
        sParticle = conList[0]
        sParticleList.append(sParticle)
    cmds.group(furyList,sParticleList, n=grpName)
    furyList = cmds.ls(type="FuryEmitter")
    cmds.select(grpName)
    
    cmds.addAttr( ln='percentShowed',at="long",defaultValue=10.0,min=0,max=100)
    cmds.addAttr( ln='minimumShowed',at="long",defaultValue=10.0,min=0,max=500)
    ## Diffuse
    cmds.addAttr( longName='diffuse', numberOfChildren=4, attributeType='compound' )
    cmds.addAttr( longName='diffuseActive',attributeType='bool',parent='diffuse')
    cmds.addAttr( longName='diffuseInput',attributeType="enum", en="velocity:force:vorticity:normal:neighbor:age:isolationTime:viscosity:density:pressure:mass:temperature:",parent='diffuse')
    cmds.addAttr( longName='diffuseMinimum',attributeType="long",defaultValue=0.0,parent='diffuse')
    cmds.addAttr( longName='diffuseMaximum',attributeType="long",defaultValue=10.0,parent='diffuse')

    '''
    cmds.addAttr( longName='diffuseColor', usedAsColor=1, attributeType="float3")
    cmds.addAttr( longName= 'diffuseColor' + "R", attributeType="float", parent='diffuseColor')
    cmds.addAttr( longName= 'diffuseColor' + "G", attributeType="float", parent='diffuseColor')
    cmds.addAttr( longName= 'diffuseColor' + "B", attributeType="float", parent='diffuseColor') 

    cmds.addAttr( longName='diffuseAlpha', usedAsColor=1, attributeType="float3")
    cmds.addAttr( longName= 'diffuseAlpha' + "_Position", attributeType="float", parent='diffuseAlpha')
    cmds.addAttr( longName= 'diffuseAlpha' + "_FloatValue", attributeType="float", parent='diffuseAlpha')
    cmds.addAttr( longName= 'diffuseAlpha' + "_Interp", attributeType="float", parent='diffuseAlpha') 
    '''
    ## emissive
    cmds.addAttr( longName='emissive', numberOfChildren=4, attributeType='compound' )
    cmds.addAttr( longName='emissiveActive',attributeType='bool',parent='emissive')
    cmds.addAttr( longName='emissiveInput',attributeType="enum", en="velocity:force:vorticity:normal:neighbor:age:isolationTime:viscosity:density:pressure:mass:temperature:",parent='emissive')
    cmds.addAttr( longName='emissiveMinimum',attributeType="long",defaultValue=0.0,parent='emissive')
    cmds.addAttr( longName='emissiveMaximum',attributeType="long", defaultValue=10.0,parent='emissive')

    for part in sParticleList:
        cmds.setAttr(part+".rotateY",-90)
        cmds.setAttr(part+".scaleZ",-1)
        
    for fury in furyList:
        root=grpName+".percentShowed"
        attr = fury+".percentShowed"
        cmds.connectAttr( root,attr )
        
        root=grpName+".minimumShowed"
        attr = fury+".minimumShowed"
        cmds.connectAttr( root,attr ) 
        
        root=grpName+".diffuse.diffuseActive"
        attr = fury+".diffuseActive"
        cmds.connectAttr( root,attr )
        
        root=grpName+".diffuse.diffuseInput"
        attr = fury+".diffuseInput"
        cmds.connectAttr( root,attr )
    
        root=grpName+".diffuse.diffuseMinimum"
        attr = fury+".diffuseMinimum"
        cmds.connectAttr( root,attr )

        root=grpName+".diffuse.diffuseMaximum"
        attr = fury+".diffuseMaximum"
        cmds.connectAttr( root,attr )
        
        root=grpName+".emissive.emissiveActive"
        attr = fury+".emissiveActive"
        cmds.connectAttr( root,attr )
        
        root=grpName+".emissive.emissiveInput"
        attr = fury+".emissiveInput"
        cmds.connectAttr( root,attr )
    
        root=grpName+".emissive.emissiveMinimum"
        attr = fury+".emissiveMinimum"
        cmds.connectAttr( root,attr )
    
        root=grpName+".emissive.emissiveMaximum"
        attr = fury+".emissiveMaximum"
        cmds.connectAttr( root,attr )
        
def loadRoot(fileName):
    offSet = "0"
    userRange = "1"
    minShow = "1"
    perShow = "1"
    mel.eval('exocortexFuryParticleLoader("'+fileName+'", '+offSet+', '+userRange+', '+minShow+', '+perShow+');')

def loadVersion(rootPath):
    rootSplit = rootPath.split("/")
    grpName = rootSplit[-1]
    folderList = os.listdir(rootPath)
    
    for folder in folderList:
        verRoot = rootPath + "/" + folder
        binList = os.listdir(verRoot)
        binList.sort()
        ext = binList[0].split(".")[-1]
        if ext == "bin":
            fileName = verRoot + "/" +  binList[0]
            loadRoot(fileName)

def getVersions(rootPath):
    nParticleList = os.listdir(rootPath)
    for part in nParticleList:
        print rootPath + "/" + part
        loadVersion(rootPath + "/" + part)
        
def importFuryCache():
    filename = cmds.fileDialog2(fileMode=2, ds=1,caption="select Folder")
    path =  filename[0]
    path = path.replace("\\","//")
    
    tmpList=os.listdir(path)
    if re.search("v[0-9][0-9][0-9]",str(tmpList[0])):
        print "getting one version"
        loadVersion(path)

    else:
        tmptmpList = os.listdir(path + "/" + tmpList[0])
        if re.search("v[0-9][0-9][0-9]",str(tmptmpList[0])):
            print "getting all versions"
            getVersions(path)

