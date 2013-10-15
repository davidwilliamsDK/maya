#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Karsten
#
# Created:     27-05-2011
# Copyright:   (c) Karsten 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

#Import custome modules
import dsOsUtil
import os

#Set pipepaths
sgServer = "https://duckling.shotgunstudio.com"
currentOs = dsOsUtil.listOS()

pipePath = None
platform = str(currentOs)
animPaths = ["anim", "blocking", "light", "effect", "playBlast","renderFiles"]

if platform == "Windows":
    if os.path.exists("//vfx-data-server/dsPipe/"):
        pipePath = "//vfx-data-server/dsPipe/"
        pantryPath = "//vfx-data-server/dsDev"
        globalPath = "//vfx-data-server/dsGlobal/"
        devPath = "//vfx-data-server/dsDev/"

    else:
        pipePath = "P:/"
        pantryPath = "O:/"
        globalPath = "S:/"
        devPath = "S:/"

    #Paths for listing files
    assetTypePath = "/asset/3D/"
    referencePath = "/ref/"
    devPath = "/dev/maya/"
    iconPath = "/images/icon/"
    emptyIconPath = "/.local/resources/icons/empty.png"
    epPath = "/film/"
    iconExt = ".png"
    templatePath = "/.local/resources/asset"
    templateName = "asset"
    minifigTemplatePath = "/.local/resources/minifig"
    minifigTemplateName = "minifig"
    shotLetter = "s"
    library = "Library"


    projectInit = "\.local\config.xml"

if platform == "Linux":
    pipePath = "/dsPipe/"
    pantryPath = "/dsDev/"
    globalPath = "/dsGlobal/"
    devPath = "/dsDev/"

    #Paths for listing files
    assetTypePath = "/asset/3D/"
    referencePath = "/ref/"
    devPath = "/dev/maya/"
    iconPath = "/images/icon/"
    emptyIconPath = "/.local/resources/icons/empty.png"
    epPath = "/film/"
    iconExt = ".png"
    templatePath = "/.local/resources/asset"
    templateName = "asset"
    minifigTemplatePath = "/.local/resources/minifig"
    minifigTemplateName = "minifig"
    shotLetter = "s"
    library = "Library"

    projectInit = "/.local/config.xml"

def libraryPath():
    return pipePath + library

def abcCachePath():
    return "data/abc"

def minifigGlobalSource():
    return globalPath + "/globalMaya/Resources/minifig/"

def listPantryPath():
    print globalPath
    return globalPath

def listGlobalPath():
    return globalPath

def listDevPath():
    return devPath


def animPathList():
    return animPaths

def listProjects():
    '''This definition list all projects in the pipe'''
    folders = dsOsUtil.listFolder(pipePath)
    projects = None
    for folder in folders:
        folderPath = pipePath + folder + projectInit
        isProject = os.path.exists(folderPath)

        if isProject:
            if not projects:
                projects = [folder]
            else:
                projects.append(folder)
    return projects

def seqAnimPath(project, episode, seq):
    seqPath = "%s%s%s%s/%s/3D/" % (pipePath, project, epPath, episode, seq)
    return seqPath

def listAssetTypes(project):
    listAssetTypePath = pipePath + project + assetTypePath
    return listAssetTypePath

def listSubAssets(project, assetType):
    listSubAssetPath = pipePath + project + assetTypePath + assetType
    return listSubAssetPath

def listAssets(project, assetType, subAsset):
    listAssets = pipePath + project + assetTypePath + assetType + "/" + subAsset
    return listAssets

def listAssetRefPath(project, assetType, assetSubType, asset):
    listAssets = pipePath + project + assetTypePath + assetType + "/" + assetSubType +  "/" + asset + referencePath
    return listAssets

def listAssetDevPath(project, assetType, assetSubType, asset):
    listDevPath = pipePath + project + assetTypePath + assetType + "/" + assetSubType +  "/" + asset + devPath
    return listDevPath

def listEpisodes(project):
    '''This definition list all projects in the pipe'''
    listEpisodePath = "%s%s%s" % (pipePath, project, epPath)
    episodes = dsOsUtil.listFolder(listEpisodePath)
    return episodes

def seqList(project, episode):
    "list seqs"
    seqPath = "%s%s%s%s" % (pipePath, project, epPath, episode)
    seqs = dsOsUtil.listFolder(seqPath)
    return seqs

def shotList(project, episode, seq):
    "list shots"
    shotPath = "%s%s%s%s/%s/" % (pipePath, project, epPath, episode, seq)
    shots = dsOsUtil.listFolder(shotPath)
    return shots

def shotShotList(project, episode, seq):
    '''List Sequence Shots Files'''
    path = "%s%s%s%s/%s/" % (pipePath, project, epPath, episode, seq)
    shotFolders = dsOsUtil.listFolder(path)
    s = []
    for shot in shotFolders:
        if shot.startswith("s"):
            try:
                int(shot[1:4])
                s.append(shot)
            except:
                pass
    return s

def seqAnimPath(project, episode, seq):
    seqPath = "%s%s%s%s/%s/" % (pipePath, project, epPath, episode, seq)
    return seqPath

def shotAnimPath(project, episode, seq, shot):
    shotPath = "%s%s%s%s/%s/%s/3D/" % (pipePath, project, epPath, episode, seq, shot)
    return shotPath

def listAssetIcon(project, assetType, assetSubType, asset):
    picPath = pipePath + project + assetTypePath + assetType + "/" + assetSubType +  "/" + asset + iconPath + asset + iconExt
    if not os.path.exists(picPath):
        picPath = pipePath + project + emptyIconPath
    if not os.path.exists(picPath):
        picPath = None
    return picPath

def listTemplatePath(project):
    listAssetTemplatePath = pipePath + project + templatePath
    return listAssetTemplatePath, templateName

def listMinifigTemplatePath(project):
    listAssetTemplatePath = pipePath + project + minifigTemplatePath
    return listAssetTemplatePath, minifigTemplateName

def listShotgunServer():
    '''Returns Duckling Shotgun Server'''
    return sgServer

def listDevPath():
    return devPath

def listRefPath():
    return referencePath
