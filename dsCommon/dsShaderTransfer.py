##### Only works bye changes namespace names. 
'''
Use-
First select imported Correctly Shaded asset
Second select Referenced Asset
Run script

'''

import maya.cmds as cmds
import re

def dsShaderTransfer():
    selectList = []
    tmpList = cmds.ls(selection=True)
    for tmp in tmpList:
        print tmp
        tmpNameSpace = tmp.split(":")[0]
        if tmpNameSpace not in selectList:
            selectList.append(tmpNameSpace)
    
    RefObj = []
    ShaderList = []
    SetList = []
    
    allObjects = cmds.ls(type="mesh")
    for obj in allObjects:
        objSplit = obj.split(":")
        if str(objSplit[0]) == str(selectList[1]):
            RefObj.append(objSplit[1])
                  
    for obj in RefObj:
        sObj = selectList[0] + ":" + obj
        nObj = selectList[1] + ":" + obj
        try:
            shadingGrps = cmds.listConnections(sObj,type='shadingEngine')
            if shadingGrps != None:
                shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
                if shaders != []:
                    if shaders[0] not in ShaderList:
                        ShaderList.append(shaders[0])
                        cmds.sets(em=True,n=shaders[0] + "_set")
                        
                    setName = shaders[0] + "_set"
                    if setName not in SetList:
                        SetList.append(setName)
                    cmds.sets(nObj ,include=str(setName))
        except:
            print " ######################### " + nObj + " Doesn't exsist on transfered Asset ########################################"

    for set in SetList:
        shaderSG = cmds.listConnections(set[:-4], d=True, et=True, t='shadingEngine')
        cmds.select(set)
        cmds.hyperShade(a = shaderSG[0])
        cmds.delete(set)