import maya.cmds as cmds
import maya.mel as mel
import os, shutil

import dsCommon.dsOsUtil as osUtil
reload(osUtil)

def handler(projInfo=None):
    print cmds.file(q=True, location=True)
    #Varibles
    keepNode = "Rig_Grp"
    subAssetName = "Render_Set"
    messageAttr = "proxies"
    tiledEXR ="False"
    subAssets = None
    vrayID = 1

    #Remove all Locked Nodes
    lockedNodes = cmds.ls(lockedNodes=True)

    if lockedNodes:
        for node in lockedNodes:
            if not node == keepNode:
                cmds.lockNode(node, l=False)
                cmds.delete(node)

    #Remove all Relative grps from the Rig_Grp
    rigRelatives = cmds.listRelatives(keepNode, children=True)
    if rigRelatives:
        for relative in rigRelatives:
            if not relative == keepNode:
                if cmds.objExists(relative):
                    cmds.delete(relative)

    #Import File
    cmds.select(all=True)
    topN = cmds.ls(sl=True, type="transform")
    print topN

    path = cmds.file(q=True, location=True).rsplit("Rig", 1)[0]
    cmds.file("%sModel.ma" % path, i=True, type="mayaAscii", mergeNamespacesOnClash=False, rpr="model", options="v=0", pr=True, loadReferenceDepth="all")

    cmds.select(all=True)
    nodes = cmds.ls(sl=True, type="transform")
    print nodes
    newNodes = list(set(nodes) - set(topN))

    #Center To World
    cmds.select(newNodes)
    cmds.delete(ch=True)
    geoShapes = cmds.ls(type=["mesh", "nurbsSurface", "nurbsCurve"])
    geo = cmds.listRelatives(geoShapes, parent=True, fullPath=True)
    print geo
    cmds.select(geo)
    #xform = cmds.xform(q=True, boundingBox=True)
    xform = cmds.polyEvaluate(b=True)
    grp = cmds.group(em=True, n="Geo_Grp")
    print grp
    cmds.delete(cmds.pointConstraint(geo, grp, mo=False))
    print xform
    cmds.setAttr("%s.translateY" % grp, xform[1][0])
    cmds.parent(newNodes, grp)

    cmds.setAttr("%s.translateX" % grp, 0)
    cmds.setAttr("%s.translateY" % grp, 0)
    cmds.setAttr("%s.translateZ" % grp, 0)

    cmds.parent(grp, keepNode)
    try:
        cmds.delete(cmds.ls(type=["parentConstraint", "pointConstraint", "orientConstraint", "scaleConstraint"]))
    except:
        print "No Constraints to delete"

    #Copy Textures and Replace Paths
    texturePath = cmds.file(q=True, location=True).rsplit("/dev/maya/", 1)[0] + "/textures/"
    textures = cmds.ls(type="file")

    for tex in textures:
        if cmds.objExists("%s.fileTextureName" % tex):
            filename = cmds.getAttr("%s.fileTextureName" % tex)
            shutil.copyfile(filename, "%s/%s" % (texturePath, filename.rsplit("/", 1)[-1]))
            try:
                cmds.setAttr("%s.fileTextureName" % tex, l=False)
            except:
                pass
            cmds.setAttr("%s.fileTextureName" % tex, "%s/%s" % (texturePath, filename.rsplit("/", 1)[-1]), type="string")

    #Create Selection Set For Publishing
    cmds.select(keepNode)
    subSet = cmds.sets(name=subAssetName)
    cmds.addAttr(subAssetName, at="message", ln=messageAttr)
    cmds.connectAttr("%s.%s" % (keepNode, messageAttr), "%s.%s" % (subAssetName, messageAttr))

    #Publish
    cmds.file(s=True)
    refPath = cmds.file(q=True, location=True).rsplit("/dev/maya/", 1)[0] + "/ref/"
    melCmd = ('source publishAssetBatch; exportBatchProcedures "%s" "%s" "%s" "%s" "%s";' % (subAssets, subAssetName, refPath, vrayID, tiledEXR))
    if str(osUtil.listOS()) == "Linux":
        os.system("maya -batch -command '%s' -file '%s'" % (melCmd, cmds.file(q=True, location=True)))
    if str(osUtil.listOS()) == "Windows":
        logFolder = refPath + "/log/"
        os.system("maya -batch -log '%s/%s_log.txt' -command '%s' -file '%s'" % (logFolder, subAssetName, melCmd, cmds.file(q=True, location=True)))
