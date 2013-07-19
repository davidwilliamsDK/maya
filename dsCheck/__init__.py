'''

Shot Check's

'''

import maya.cmds as cmds
import dsCommon.dsMetaDataTools as dsMDT
import dsSaveScene;reload(dsSaveScene)

def dsMDCheck():
    #print "dsMD preflight check"
    if not cmds.ls("dsMetaData"):
        #print "no dsMD node"
        filePath = cmds.file(q=True,sn=True)
        fileName = cmds.file(q=True,sn=True,shn=True)

        if fileName == "":
            print "your working in a untitled maya scene.. Please save file in correct position"
            dsSaveScene.dsSS()
        else:
            print "no dsMD node in your scene creating one.. may take 2 min."
            dsMDT.createMDscriptNode()
            

def dsSceneCheck():
    print "render preflight check"
    
    fileName = cmds.file(q=True,sn=True,shn=True)
    fps = cmds.currentUnit( query=True, t=True )    
    
    if fps == "game":fps=15
    if fps == "film":fps=24
    if fps == "pal":fps=25
    if fps == "ntsc":fps=30
    if fps == "show":fps=48
    if fps == "palf":fps=50
    if fps == "ntscf":fps=60    

    x = cmds.getAttr("defaultResolution.width")
    y = cmds.getAttr("defaultResolution.height")
    
    