import maya.cmds as cmds
import maya.mel as mel

import dsOsUtil as osUtil
import os

def listRelatedProxies(sel=""):
    '''This Will list all related proxies to a reference'''
    if str(sel) == "":
        sel = cmds.ls(sl=True, hd=1, type="transform")

    if not sel == "":
        RNfile = cmds.referenceQuery(sel, filename=True)
        RN = cmds.referenceQuery(RNfile, referenceNode=True)
        relatedRN = mel.eval("getRelatedProxies %s;" % RN)
        return relatedRN

def listCurrentProxy(sel=""):
    '''List the current proxy, the selection belongs to'''
    if str(sel) == "":
        sel = cmds.ls(sl=True, hd=1, type="transform")
    if not str(sel) == "":
        proxfile = cmds.referenceQuery(sel ,filename=True )
        prox = cmds.referenceQuery( proxfile, referenceNode=True )
    return prox

def removeNonActiveProxies(sel=""):
    if not sel == "":
        currentProxy = listCurrentProxy(sel)
        relatedProxies = listRelatedProxies(sel)
        relatedProxies.remove(currentProxy)

        for rn in relatedProxies:
            cmds.file(removeReference=True, referenceNode=rn)
            #If the line above fuckes up, use the one belov instead, it's using maya's own proxyRemove
            #mel.eval("dsProxyRemove %s;" % rn)

def addProxies(sel=""):
    if not sel == "":
        currentPath = cmds.referenceQuery(sel ,filename=True )
        refPath = currentPath.rsplit("/", 1)[0]+"/"
        currentFile = currentPath.rsplit("/", 1)[1]
        RN = listCurrentProxy(sel)
        ext = currentPath.rsplit(".", 1)[1]
        assetName = currentPath.rsplit("/", 1)[1].rsplit("_", 1)[0]
        currentProxy = currentPath.rsplit("_", 1)[1].rsplit(".", 1)[0]

        files = os.listdir(refPath)

        for f in files:
            if assetName in f:
                if ext in f:
                    if not currentFile in f:
                        proxyTag = f.rsplit("_", 1)[1].rsplit(".", 1)[0]
                        if "\\" in refPath:
                            proxyPath = refPath.split("\\")
                            proxyPath = proxyPath.join("/")
                        else:
                            proxyPath = refPath

                        addItem = 'proxyAdd %s "%s" "%s";' % (RN, (proxyPath + "/" + f), proxyTag)
                        mel.eval(addItem)