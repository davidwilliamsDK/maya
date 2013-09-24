'''
Created on 06/09/2013

@author: admin
'''
import maya.cmds as cmds

def swapRef():
    ##Swap Refenreces            
    refs = cmds.ls(references=True)
    currentLoaded = []
    for ref in refs:
        try:
            path = cmds.referenceQuery(ref ,filename=True )
            refNode = cmds.referenceQuery(path, referenceNode=True)
        except:
            pass
        
        if not refNode in currentLoaded:
            currentLoaded.append(refNode)
                 
    filetypeMB = "mayaBinary"
    
    for currentRef in currentLoaded:
        try:
            currentRefPath = cmds.referenceQuery(currentRef ,filename=True )
        except:
            currentRefPath = False
        if currentRefPath:
            if str(currentRefPath[:2]) == "P:":
                newReference = currentRefPath.replace("P:/","//vfx-data-server/dsPipe/")
                ext = newReference.split(".")[-1]
                if ext[:2] == "mb":
                    cmds.file(newReference, loadReference=currentRef, type=filetypeMB, options="v=0")


def swapTexture():
    ##Swap Textures                
    files = cmds.ls(type="file")
    print files
    
    for f in files:
        if cmds.objExists("%s.fileTextureName" % f):
            path = cmds.getAttr("%s.fileTextureName" % f)
            if path.startswith("P:/"):
                print f
                print path
                newPath = "//vfx-data-server/dsPipe/" + path.split("/", 1)[-1]
                print newPath
                cmds.setAttr("%s.fileTextureName" % f, newPath, type="string")
                
'''
refs = cmds.ls(references=True)
currentLoaded = []
for ref in refs:
    try:
        path = cmds.referenceQuery(ref ,filename=True )
        refNode = cmds.referenceQuery(path, referenceNode=True)
    except:
        pass
        
    if not refNode in currentLoaded:
        currentLoaded.append(refNode)
                 
filetypeMB = "mayaBinary"
filetypeMA = "mayaAscii"

for currentRef in currentLoaded:
    try:
        currentRefPath = cmds.referenceQuery(currentRef ,filename=True )
    except:
        currentRefPath = False
    if currentRefPath:
        print str(currentRefPath[:2])
        if str(currentRefPath[:2]) != "P:":
            #newReference = currentRefPath.replace("//vfx-data-server/dsPipe/","P:/")
            newReference = currentRefPath.replace("/dsPipe/","P:/")

            ext = newReference.split(".")[-1]
            if ext[:2] == "ma":
                cmds.file(newReference, loadReference=currentRef, type=filetypeMA, options="v=0")
                
files = cmds.ls(type="file")
    
for f in files:
    if cmds.objExists("%s.fileTextureName" % f):
        path = cmds.getAttr("%s.fileTextureName" % f)
        if path.startswith("//vfx-data-server/dsPipe/"):
            print f
            print path
            newPath = "P:/" + path.split("dsPipe/", 1)[-1]
            print newPath
            cmds.setAttr("%s.fileTextureName" % f, newPath, type="string")
try:       
    cmds.setAttr("__sceneSetup_Duplo_jro_Background_Tex.fileTextureName","P:/Lego_Duplo/asset/3D/light/Sky_day.png",type="string")
except:
    pass

try:
    cmds.setAttr("Duplo_lightSetup_jro_sceneSetup_Duplo_jro_Background_Tex.fileTextureName","P:/Lego_Duplo/asset/3D/light/Sky_day.png",type="string")
except:
    pass
'''