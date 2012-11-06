import maya.cmds as cmds
import maya.mel as mel
import dsSgUtil as sgBridge
reload(sgBridge)

def exportCleanSets(subAsset=None, proxy=None, refPath=None, vraySet=0):
    print "Start on Script --------------------------------------"
    #list proxies and subAssets
    if cmds.objExists("Rig_Grp.subAssets"):
        subAssets = cmds.listConnections("Rig_Grp.subAssets", source=True)
    else:
        subAssets = "None"
    if cmds.objExists("Rig_Grp.proxies"):
        proxies = cmds.listConnections("Rig_Grp.proxies", source=True)
    else:
        proxies = "None"

    #Unhide hidden
    exportUnhide(subAsset)
    exportUnhide(proxy)

    #IF THERE's A SUBASSET LIKE ON SETS
    if subAsset and not subAsset=="None":
        print "SubAsset ----------------------------------------------"
        #find all subAsset transforms beloing to set
        #These nodes may not be deleted
        cmds.select(subAsset, r=True)
        subAssetSel = cmds.ls(sl=True, long=True, type="transform")

        #find all subAsset transforms
        cmds.select(subAssets, r=True)
        subAssetsSel = cmds.ls(sl=True, long=True, type="transform")

        deleteSet=[]

        for item in subAssetsSel:
            if not item in subAssetSel:
                deleteSet.append(item)

        if proxy and not proxy == "None":
            #find all proxy transforms beloing to set
            #These nodes may not be deleted
            cmds.select(proxy, r=True)
            proxySel = cmds.ls(sl=True, long=True, type="transform")

            #find all proxies transforms
            cmds.select(proxies, r=True)
            proxiesSel = cmds.ls(sl=True, long=True, type="transform")

            for item in proxiesSel:
                if not item in proxySel:
                    deleteSet.append(item)
        else:
            cmds.select(proxies, r=True)
            relativ = cmds.listRelatives(allDescendents=True, fullPath=True, type="transform")

            if relativ:
                for asset in subAssetsSel:
                    if not asset in relativ:
                        for item in relative:
                            deleteSet.append(item)

        if proxies:
            deleteSets(proxies)

        deleteSets(subAssets)

        try:
            deleteItem = cmds.listRelatives(deleteSet, fullPath=True, ad=True, type="transform")
            cmds.select(deleteItem, deleteSet, r=True)
            cmds.lockNode(l=False)
            cmds.delete()
        except:
            pass


    #IF THERE's ONLY PROXIES NO SUBASSETS LIKE ON CHARS
    if not subAssets or subAssets == "None":
        print "Proxy -----------------------------------------------------"
        if proxies:
            #find all proxy transforms beloing to set
            cmds.select(proxy, r=True)
            proxySel = cmds.ls(sl=True, long=True, type="transform")

            #find all proxies transforms
            cmds.select(proxies, r=True)
            proxiesSel = cmds.ls(sl=True, long=True, type="transform")

            deleteSet=[]

            for item in proxiesSel:
                if not item in proxySel:
                    deleteSet.append(item)

            if not deleteSet == []:
                unlockHierarchy(deleteSet)
                cmds.select(deleteSet, r=True)
                print "Delete --------------------------"
                cmds.delete()

            deleteSets(proxies)

    #Clean file
    print"Cleaning files ----------------------------------"
    deleteNodes()
    cleanShaders(True)
    setVrayID(vraySet)

    #find file basename and path
    if cmds.objExists("|Rig_Grp.assetName"):
        print "IT's DOING THIS"
        fileBaseName = cmds.getAttr("|Rig_Grp.assetName")
        filePath = refPath

    #Find baseAsset Name
    if subAsset.endswith("_Set"):
        subAsset = subAsset.split("_Set", 1)[0]

    #Find baseProxy Name
    if proxy.endswith("_Set"):
        proxy = proxy.split("_Set", 1)[0]

    #Set Proxy Name
    if cmds.objExists("|Rig_Grp.assetProxy"):
        if subAsset and not subAsset=="None":
            if proxy:
                cmds.setAttr("|Rig_Grp.assetProxy", "%s_%s" % (subAsset, proxy), type="string")
            else:
                cmds.setAttr("|Rig_Grp.assetProxy", subAsset, type="string")
        elif proxy:
            cmds.setAttr("|Rig_Grp.assetProxy", proxy, type="string")

    #rename subAsset file
    if subAsset and not subAsset=="None":
        if proxy and not proxy == "None":
            renamefile = "%s/%s_%s_%s.mb" % (filePath, fileBaseName, subAsset,proxy)
            cmds.file(rename=renamefile)
        else:
            renamefile = "%s/%s_%s.mb" % (filePath, fileBaseName, subAsset)
            cmds.file(rename=renamefile)

    #rename Proxy file
    if not subAssets or subAssets == "None":
        renamefile = "%s/%s_%s.mb" % (filePath, fileBaseName, proxy)
        cmds.file(rename=renamefile)

    cmds.file(save=True, force=True, type='mayaBinary' )
    print "ENDING CLEAN UP"

def exportUnhide(item=None):
    if cmds.objExists("Rig_Grp.subAssets"):
        subAssets = cmds.listConnections("Rig_Grp.subAssets", source=True)
    else:
        subAssets = None
    if cmds.objExists("Rig_Grp.proxies"):
        proxies = cmds.listConnections("Rig_Grp.proxies", source=True)
    else:
        proxies = None

    cmds.select(subAssets, proxies, r=True)
    sets = cmds.ls(sl=True, type="transform")

    for item in sets:
        if cmds.objExists("%s.visibility" % item):
            if not cmds.getAttr("%s.visibility" % item, lock=True):
                try:
                    cmds.setAttr("%s.visibility" % item, 1)
                except:
                    pass

def deleteSets(setArray=None):
    '''This function is only to delete the selections sets'''
    print "Running deleteSets ----------------------------"
    if setArray:
        for item in setArray:
            print item
            try:
                cmds.select(item, r=True, ne=True)
                cmds.lockNode(l=False)
                cmds.delete()
            except:
                pass
    else:
        print "No array of sets passed to funktion"

def deleteNodes():
    '''This function deletes everything thats not inside the Root_Group'''
    print "Running delete Nodes -----------------------------"
    cmds.select(all=True)
    root = "|Rig_Grp"
    allTopNodes = cmds.ls(sl=True, long=True, type="transform")

    for topNode in allTopNodes:
        if not root == topNode:
            try:
                cmds.select(topNode, hi=True)
                cmds.lockNode(l=False)
                cmds.delete()
            except:
                pass

def unlockHierarchy(list):
    print "Unlocking Hierarchy ----------------------------"

    for item in list:
        cmds.select(item, hi=True)
        relatives = cmds.ls(sl=True, long=True)
        for child in relatives:
            cmds.lockNode(child, l=0)

def cleanShaders(action=None):
    try:
        if action:
            print "Optimizing Scene"
            mel.eval('source "cleanUpScene";')
            mel.eval('deleteEmptyLayers("Display");')
            mel.eval('removeDuplicateShadingNetworks(0);')
            mel.eval('deleteUnusedBrushes();')
            mel.eval('deleteUnknownNodes();')
            mel.eval('scOpt_performOneCleanup( { "shaderOption" } );')
    except:
        pass

def importRef():
    '''Imports all refs and cleans the object names for : '''
    refs = cmds.file( q=True, l=True )
    print "This is the refs: %s" % refs

    for ref in refs:
        if not ref == cmds.file(expandName=True, q=True):
            suffix = ref.rsplit(".",1)[1]
            if suffix.startswith("ma") or suffix.startswith("mb"):
                try:
                    print suffix
                    print ref
                    cmds.file(ref, loadReference=True)
                    cmds.file(ref, importReference=True, force=True)
                except:
                    pass

    cmds.select(all=True)
    #nodes = cmds.ls(sl=True, type="transform")
    allNodes = cmds.listRelatives(ad=True, fullPath=True)
    cmds.select(allNodes, r=True)

    allNodes = cmds.ls(sl=True, long=True)

    allNodes.sort()
    allNodes.reverse()

    lockedState = False

    for node in allNodes:
        if cmds.objExists(node):
            if (":") in node:
                try:
                    lockedState = cmds.lockNode(node, l=True, q=True)[0]
                    cmds.lockNode(node, l=False)
                    name = node.rsplit(":")[-1]

                    newName = cmds.rename(str(node), str(name))

                    if lockedState:
                        cmds.lockNode(newName, l=True)
                except:
                    pass

    cmds.select(all=True, r=True, ne=True)
    topNodes = cmds.ls(sl=True, type=["transform", "objectSet"])

    print topNodes

    for node in topNodes:
        if cmds.objExists(node):
            if (":") in node:
                try:
                    lockedState = cmds.lockNode(node, l=True, q=True)[0]
                    cmds.lockNode(node, l=False)
                    name = node.rsplit(":")[-1]

                    newName = cmds.rename(str(node), str(name))

                    if lockedState:
                        cmds.lockNode(newName, l=True)
                except:
                    pass

def setVrayID(vraySet):
    try:
        typeSet = 0
        if cmds.objExists("|Rig_Grp.assetType"):
            assetType = cmds.getAttr("|Rig_Grp.assetType")
            if assetType == "char":
                typeSet = 1
            elif assetType == "character":
                typeSet = 1


        if vraySet == 1 or typeSet == 1:
            if cmds.objExists("|Rig_Grp.project"):
                if cmds.objExists("|Rig_Grp.assetName"):
                    if cmds.objExists("|Rig_Grp.assetSubType"):
                        projName = cmds.getAttr("|Rig_Grp.project")
                        assetName = cmds.getAttr("|Rig_Grp.assetName")
                        assetSubType = cmds.getAttr("|Rig_Grp.assetSubType")

                        val = sgBridge.sgGetAssetID(projName, assetName, assetType, assetSubType) #"get from Shotgun"
                        print val[0]["id"]
                        shapes =  cmds.ls(type="mesh", long=True)

                        if shapes:
                            for shape in shapes:
                                mel.eval("vrayAddAttr %s vrayObjectID;" % str(shape))
                                mel.eval("vrayUpdateAE;")
                                if cmds.objExists("%s.vrayObjectID" % shape):
                                    print shape
                                    cmds.setAttr("%s.vrayObjectID" % shape, val[0]["id"])
    except:
        pass