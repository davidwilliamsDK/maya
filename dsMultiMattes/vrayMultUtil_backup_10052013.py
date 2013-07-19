import maya.mel as mel
import maya.cmds as cmds

#APPLY ID's
def setVrayID(states=None, operation=None, shaders=None):
    if states:
        if operation:
            renderLayerOK=True
            if cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True) == "defaultRenderLayer":
                renderLayerOK=False
            if states["override"] == 0:
                renderLayerOK=True

            if renderLayerOK:
                if shaders:
                    sel = shaders
                else:
                    if states["allShaders"] == 0:
                        if states["objectOrMult"] == 2:
                            transforms = cmds.ls(sl=True, type="transform")
                            print "1"
                            sel = cmds.listRelatives(transforms, shapes=True, fullPath=True, ni=True, type=["mesh", "nurbsSurface"])
                        if states["objectOrMult"] == 0:
                            print "2"
                            sel = cmds.ls(sl=True, type=cmds.listNodeTypes("shader"))
                    if states["allShaders"] == 2:
                        if states["objectOrMult"] == 2:
                            print "3"
                            sel = cmds.ls(ni=True, type=["nurbsSurface", "mesh"])
                        if states["objectOrMult"] == 0:
                            print "4"
                            sel = cmds.ls(type=cmds.listNodeTypes("shader"))


                if states["objectOrMult"] == 2:
                    attribute = "vrayObjectID"
                if states["objectOrMult"] == 0:
                    attribute = "vrayMaterialId"

                print sel
                if sel:
                    index = states["startIndex"]
                    for s in sel:
                        if not cmds.objExists("%s.%s" % (s, attribute)):
                            print s
                            try:
                                if states["objectOrMult"] == 2:
                                    mel.eval('vrayAddAttr %s vrayObjectID;' % s)
                                if states["objectOrMult"] == 0:
                                    mel.eval('vrayAddAttr %s vrayColorId;vrayAddAttr %s vrayMaterialId;' % (s,s))
                            except:
                                pass
                        try:
                            try:
                                if states["override"] == 2:
                                    mel.eval('editRenderLayerAdjustment %s.%s;' % (s, attribute))
                            except:
                                pass
                            cmds.setAttr("%s.%s" % (s, attribute), index)

                            if operation == "unikID":
                                index = index+1
                        except:
                            pass

                    #Set MultiMattes
                    if states["multiMattes"] == 2:
                        states["endIndex"] = index
                        setVrayMult(states)
                    return index
            else:
                print "Can't add render override on default renderlayer"

#SETUP MULTIMATTES
def setVrayMult(states=None):
    if states:
        i = 0
        loopTime = 1
        if states["ids"]:
            for number in sorted(states["ids"]):
                print number
        if not states["ids"]:
            for number in range(states["startIndex"], states["endIndex"]+1, 1):
                if i == 0:
                    matteName = mel.eval("vrayAddRenderElement MultiMatteElement")
                    matteV = cmds.rename(matteName, "mask_%s_%02d" % (states["matteName"], loopTime))
                    cmds.setAttr(matteV + ".vray_redid_multimatte", number)
                    if states["objectOrMult"] == 0:
                        cmds.setAttr(matteV + ".vray_usematid_multimatte", 1)
                    cmds.setAttr(matteV + ".vray_affectmattes_multimatte", 0)
                    setName = "%s" % (matteV)
                    cmds.setAttr(matteV + ".vray_name_multimatte", setName, type="string")
                elif i == 1:
                    cmds.setAttr(matteV + ".vray_greenid_multimatte", number)
                elif i == 2:
                    cmds.setAttr(matteV + ".vray_blueid_multimatte", number)
                i = i+1
                if i == 3:
                    i = 0
                    loopTime = loopTime + 1

def findID(states=None):
    if states["objectOrMult"] == 2:
        attribute = "vrayObjectID"
        transforms = cmds.ls(type="transform")
        sel = cmds.listRelatives(transforms, shapes=True, fullPath=True, type=["mesh", "nurbsSurface"])
    if states["objectOrMult"] == 0:
        attribute = "vrayMaterialId"
        sel = cmds.ls(type=cmds.listNodeTypes("shader"))

    if sel:
        startIndex = cmds.getAttr("%s.%s" % (sel[0], attribute))
        endIndex = cmds.getAttr("%s.%s" % (sel[0], attribute))
        ids = []

        for s in sel:
            try:
                ID = cmds.getAttr("%s.%s" % (s, attribute))
                if ID < startIndex:
                    startIndex = ID
                if ID > endIndex:
                    endIndex = ID
                if not ID in ids:
                    ids.append(ID)
            except:
                pass
    return [startIndex, endIndex, ids]

def linkedShaders(states, operation=None):
    #Finding All Shaders
    shadersInScene = cmds.ls(type=cmds.listNodeTypes("shader"))
    geoInScene = cmds.ls(ni=True, type=["mesh", "nurbsSurface"])
    sel = cmds.ls(sl=True)
    files = []

    #Find References From Selection
    for s in sel:
        if ":" in s:
            ref = cmds.referenceQuery(s, filename=True)
            if not ref in files:
                files.append(ref)

    #Give The Mattes a Name
    matteName = str(states["matteName"])
    nodes=[]
    i=0

    #Create Render Layer
    if states["createRenderLayer"] == 2:
        for f in files:
            referenceNodes = cmds.referenceQuery(f, nodes=True)
            shaderNodes = list(set(referenceNodes) & set(shadersInScene))
            if ":" in shaderNodes[0]:
                nodes.append(shaderNodes[0].split(":")[0])
        if nodes:
            createRenderlayers(states, nodes)

    #Find Objects or Shaders and set the ID
    for f in files:
        referenceNodes = cmds.referenceQuery(f, nodes=True)
        if states["objectOrMult"] == 2:
            shaderNodes = list(set(referenceNodes) & set(geoInScene))
        if states["objectOrMult"] == 0:
            shaderNodes = list(set(referenceNodes) & set(shadersInScene))

        if shaderNodes:
            if ":" in shaderNodes[0]:
                mattePrefix = shaderNodes[0].split(":")[0]
                states["matteName"] = "%s_%s" % (matteName, mattePrefix)

                #Create ID's
                endID = setVrayID(states, operation, shaderNodes)

                if operation == "singleID":
                    states["startIndex"] = states["startIndex"] + 1
                else:
                    states["startIndex"] = states["startIndex"] + int(endID)

def createRenderlayers(states=None, nodes=None):
    layerName = str(states["matteName"])
    if nodes:
        objects = []
        for n in nodes:
            cmds.select("%s:*" % n)
            objects = objects + (cmds.ls(sl=True, long=True, type="transform"))
            cmds.select(objects)
        if objects:
            cmds.createRenderLayer(objects, n=layerName, number=1, noRecurse=True, mc=True)