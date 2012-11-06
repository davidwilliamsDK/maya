import maya.cmds as cmds

def connectSkins(abc, asset):
    cmds.select("%s:mesh_*" % asset)
    sel = cmds.ls(sl=True, type="transform")
    selShape = cmds.listRelatives(shapes=True)
    selShapeLong = cmds.listRelatives(shapes=True, fullPath=True)

    list = cmds.listConnections(abc + ".outPolyMesh", connections=True, plugs=True)
    sourceList = []

    for l in list:
        if abc in l:
            sourceList.append(l)

    for source in sourceList:
        connect = cmds.listConnections(source, connections=True, plugs=True)
        for c in connect:
            if not abc in c:
                cleanName = c.rsplit("|",1)[-1].rsplit(":",1)[-1].rsplit(".",1)[0]
                attr = "." + c.rsplit("|",1)[-1].rsplit(".",1)[-1]
                if cleanName in sel:
                    print "sel"
                temp = selShape[0].split(":",1)[0]
                if ("%s:%s" % (temp, cleanName)) in selShape:
                    index = selShape.index("%s:%s" % (temp, cleanName))
                    cmds.connectAttr(connect[0], selShapeLong[index] + attr, force=True)

def connectTrans(abc, asset):
    cmds.select("%s:mesh_*" % asset)
    sel = cmds.ls(sl=True, type="transform", sn=True)
    selLong = cmds.ls(sl=True, type="transform", long=True)

    print abc
    list = cmds.listConnections(abc + ".transOp", connections=True, plugs=True)
    sourceList = []

    if list:
        for l in list:
            if abc in l:
                sourceList.append(l)

        selShort = []
        for s in sel:
            if "|" in s:
                selShort.append(s.rsplit("|",1)[-1])
            else:
                selShort.append(s)

        for source in sourceList:
            connect = cmds.listConnections(source, connections=True, plugs=True)
            for c in connect:
                if not abc in c:
                    cleanName = c.rsplit("|",1)[-1].rsplit(":",1)[-1].rsplit(".",1)[0]
                    attr = "." + c.rsplit("|",1)[-1].rsplit(".",1)[-1]
                    temp = sel[0].split(":",1)[0]

                    if "unitConversion" in cleanName:
                        unitList = cmds.listConnections(cleanName + ".output", connections=True, plugs=True)
                        destName = unitList[1].rsplit("|",1)[-1].rsplit(":",1)[-1].rsplit(".",1)[0]
                        attr = "." + unitList[1].rsplit(".",1)[-1]

                        if ("%s:%s" % (temp,destName)) in selShort:
                            index = selShort.index(("%s:%s" % (temp,destName)))
                            cmds.connectAttr(unitList[0], sel[index] + attr, force=True)

                    if ("%s:%s" % (temp, cleanName)) in selShort:
                        index = selShort.index("%s:%s" % (temp, cleanName))
                        cmds.connectAttr(abc + "." + connect[0].rsplit(".",1)[-1], sel[index] + attr, force=True)