import sys, os, re, shutil, random, sip, platform
import maya.cmds as cmds
import maya.mel as mel

def chimaFillerSwopTextures():
    jpgFolder = "JPEG/"
    jpgExt = ".jpg"
    assetFile = cmds.file( q=True, l=True )
    path = assetFile[0].rsplit("/",1)[0] + "/sourceimages/"
    textures = cmds.ls(type="file")
    removeGamma()
    for t in textures:
        if cmds.objExists(t + ".fileTextureName"):
            cmds.setAttr(t + ".fileTextureName", l=False)
            textureName = cmds.getAttr(t + ".fileTextureName")
            textureName = textureName.rsplit("/", 1)[-1]
            if ".tiff" in textureName:
                textureName = textureName.rsplit(".",1)[0] + ".tif"

            newTextureName = path + textureName

            #Try Setting jpg path
            if ".tif" in textureName:
                testPath = path + jpgFolder + textureName.rsplit(".",1)[0] + jpgExt
                print testPath

                if os.path.exists(testPath) == True:
                    newTextureName = testPath

            cmds.setAttr(t + ".fileTextureName", newTextureName, type="string")


def vrayObjectProp(enable=0):
    sel = cmds.ls(sl=True)
    if sel:
        for s in sel:
            shapes = cmds.listRelatives(c=True, type="mesh")
            if shapes:
                for shape in shapes:
                    mel.eval("vray addAttributesFromGroup %s vray_subdivision %s;" % (shape, enable))

def vraySmoothNode(add=True):
    sel = cmds.ls(sl=True)
    shapes = cmds.listRelatives(sel, ad=True, fullPath=True, type=["mesh", "nurbsSurface", "subdiv"])
    for shape in shapes:
        mel.eval("vray addAttributesFromGroup %s vray_subdivision %s" % (shape, add))


def removeGamma():
    textureFiles = cmds.ls(type ="file")
    for each in textureFiles:
        try:
            cmds.setAttr(each+".vrayFileGammaEnable", 0)
        except:
            pass