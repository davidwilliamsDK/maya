import os, sys
import maya.cmds as cmds

if sys.platform == "linux2":
    img2tiledexr = "/dsCore/maya/dsTiledExr/img2tiledexr"
else:
    img2tiledexr = "U:/dsCore/maya/dsTiledExr/img2tiledexr"

def currentSceneHandler():
    '''This Handles the texture converting.'''
    allTextures = listAllTextures()
    converToExrHandler(allTextures)
    swopTexture("exr")

def listAllTextures():
    files = cmds.ls(type="file")
    fileTextures = []
    for tex in files:
        if cmds.objExists("%s.fileTextureName" % tex):
            filename = cmds.getAttr("%s.fileTextureName" % tex)
            if not filename in fileTextures:
                if not filename.endswith(".hdr"):
                    fileTextures.append(filename)

    return fileTextures

def converToExrHandler(textures):
    for texture in textures:
        input = texture
        output = texture.rsplit(".",1)[0] + ".exr"
        convertToExr(input, output)

def convertToExr(input=None, output=None):
    "This Def needs an input and output and will generate tiled exr's from this"
    if input and output:
        if os.path.exists(input):
            os.system("%s %s %s -linear off" % (img2tiledexr, input, output))
            print "File output: %s" % (output)
        else:
            print "The Specified input file does not exist"
    else:
        print "Please provide input file and output file ex. file.png file.exr"

def swopTexture(origOrExr = "orig"):
    '''This Def swops between the exr texture or the orig texture the exr was created from'''
    '''IF There's more than one non exr frame with the same name in the same position it will not beable to figure out which one that is the correct one'''
    '''Run the command swopTextures("exr") to swop to exr or leave it empty to fallbact to orig textures.'''
    files = cmds.ls(type="file")
    for tex in files:
        print tex
        if cmds.objExists("%s.fileTextureName" % tex):
            filename = cmds.getAttr("%s.fileTextureName" % tex)
            if not filename.endswith(".hdr"):
                if filename.endswith(".exr"):
                    if origOrExr == "orig":
                        path = filename.rsplit("/",1)[0] + "/"
                        print path
                        filesInDir = os.listdir(path)
                        origFiles = []
                        for file in filesInDir:
                            if filename.rsplit("/",1)[-1].rsplit(".",1)[0] in file:
                                origFiles.append(file)
                        print origFiles
                        if len(origFiles) > 1:
                            for orig in origFiles:
                                if not filename.rsplit("/",1)[-1] in orig:
                                    origTexture = filename.rsplit("/", 1)[0] + "/" + orig
                                    print origTexture
                                    cmds.setAttr("%s.fileTextureName" % tex, origTexture, type="string")
                    else:
                        print "already exr"
                else:
                    if origOrExr == "exr":
                        exrTexture = filename.rsplit(".", 1)[0] + ".exr"
                        print exrTexture
                        if os.path.exists(exrTexture):
                            cmds.setAttr("%s.fileTextureName" % tex, exrTexture, type="string")
                        else:
                            print "Exr does not Exist please convert files first"
                    else:
                        print "already original texture"