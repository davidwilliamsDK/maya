#Lego Cleanup
name = ()
### import regular expression
import re
###
import os
import os.path
###
import shutil
### import maya cmds
import maya.cmds as cmds
### import xml tools
from xml.etree import ElementTree as ET
from xml.dom import minidom

def deleteHistory(self):
    cmds.delete(all=True,constructionHistory=True,expressions=True,constraints=True,staticChannels=True)
    print "Done deleting history"
def exportScene(self):
    mesh = cmds.ls(type="mesh")
    print mesh
    cmds.select(mesh)
    currentScene = cmds.file(q=True,sceneName=True)
    newScene = currentScene.split(".")[0]+"_clean.mb"
    cmds.file( newScene, type='mayaBinary', force=True, es=True )
    cmds.file( newScene, force=True, open=True)
def cleanScene(self):
    deleteList = "nurbsCurve","nurbsSurface","unknownTransform","animCurveTU","wire","brush","unknown","choice","unitToTimeConversion","displayLayer"
    skippList = [u'time1', u'sequenceManager1', u'renderPartition', u'renderGlobalsList1', u'defaultLightList1', u'defaultShaderList1', u'postProcessList1', u'defaultRenderUtilityList1', u'defaultRenderingList1', u'lightList1', u'defaultTextureList1', u'lambert1', u'particleCloud1', u'initialShadingGroup', u'initialParticleSE', u'initialMaterialInfo', u'shaderGlow1', u'dof1', u'defaultRenderGlobals', u'defaultRenderQuality', u'defaultResolution', u'defaultLightSet', u'defaultObjectSet', u'defaultViewColorManager', u'hardwareRenderGlobals', u'hardwareRenderingGlobals', u'characterPartition', u'defaultHardwareRenderGlobals', u'ikSystem', u'hyperGraphInfo', u'hyperGraphLayout', u'globalCacheControl', u'dynController1', u'persp', u'perspShape', u'top', u'topShape', u'front', u'frontShape', u'side', u'sideShape', u'lightLinker1', u'brush1', u'strokeGlobals', u'layersFilter', u'objectTypeFilter74', u'animLayersFilter', u'objectTypeFilter75', u'notAnimLayersFilter', u'objectTypeFilter76', u'defaultRenderLayerFilter', u'objectNameFilter4', u'renderLayerFilter', u'objectTypeFilter77', u'objectScriptFilter10', u'renderingSetsFilter', u'objectTypeFilter78', u'relationshipPanel1LeftAttrFilter', u'relationshipPanel1RightAttrFilter', u'layerManager', u'defaultLayer', u'renderLayerManager', u'defaultRenderLayer']
    skippList = skippList + cmds.ls("m*", type = "mesh")
    assetTypeList = cmds.ls(type=deleteList)
    ###Rename shaders with m to shaderm to remove errors...
    list = "layeredShader","blinn","phongE"
    mShaders = cmds.ls("m*",type=list)
    print mShaders
    for each in mShaders:
        try:
            print each
            cmds.rename(each, "shader"+each)
        except:
            pass
    ###delete stuff we dont want...
    for asset in assetTypeList:
        if not asset in skippList:
            try:
                cmds.delete(asset)
            except:
                pass
        else:
            print "asset"
            pass
        
    ###delete object with locked visibility to off
    all = cmds.ls(type=["transform","mesh"])
    print all
    for each in all:
        try:
            if not cmds.getAttr(each+".v"):
                deleteThis = cmds.pickWalk( each, direction='up' )
                moveHere = cmds.pickWalk( deleteThis, direction='up' )
                cmds.parent(each,moveHere,shape=True)
                cmds.setAttr( each+".v", lock=False)
                cmds.setAttr( each+".v", 1)
                cmds.delete(deleteThis)
        except:
            pass
    ###delete empty transforms...
    all = cmds.ls(type="transform")
    for each in all:
        try:
            if cmds.pickWalk(each, direction='down')[0] == each:
                cmds.delete(each)
        except:
            pass
    print "Done cleaning"
def deleteUnusedShaders(self):
    #### check its deleting a bit too much :(
    meshes = cmds.ls(type="mesh")
    cmds.select(meshes)
    
    cmds.delete(cmds.ls(type="ramp"))
    
    shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1)
    shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
    shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
    
    ### Check from texture uppwards until layerdShader
    texture = cmds.ls(textures=1)
    print texture
    texturedShader = cmds.ls(cmds.listConnections(texture),materials=1)
    print texturedShader
    layerdShader = cmds.ls(cmds.listConnections(texturedShader),materials=1)
    print layerdShader
    
    shaders = shaders+texturedShader
    
    shaderTypes = "phongE","blinn","layeredShader"
    allShaders = cmds.ls(type = shaderTypes)
    
    for sh in allShaders:
        if not sh in shaders:
            cmds.delete(sh)
        else:
            pass
    print "Done deleating unused shaders"
def deleteUnusedShapes(self):
    sel = cmds.ls(long=True,type="transform")
    print sel
    
    for s in sel:
        shapes = cmds.listRelatives(s, s=True, fullPath=True)
        #print shapes
        i = 0
        if shapes:
            for shape in shapes:
                if not i == 0:
                    print shape
                    cmds.delete(shape)
                i = i + 1
def deleteUnusedPlace2dNodes(self):
    allplace2dTexture = cmds.ls(type="place2dTexture")
    print allplace2dTexture
    for each in allplace2dTexture:
        if not cmds.listConnections(each, t='file' ):
            print each
            cmds.delete(each)
def exportBricks(self):
    mList = cmds.ls('m*',long=True, type=["transform","mesh"])
    mBrickPath = '/dsPipe/Library/asset/3D/Bricks/testBricks/'
    tempIcon = '/dsPipe/Library/.local/Resources/Icons/Empty.png'
    newlist = []
    dictAdd = {}
    for mName in mList:
        try:
            lod = cmds.getAttr(mName+".LEGO_brickLOD")
        except:
            lod = 0
            pass
        if mName.split('|')[-1].split('_')[0] not in newlist:
            newlist.append(mName.split('|')[-1].split('_')[0])
            longName = mName
            shortName = mName.split('|')[-1].split('_')[0]
            lodNumber = lod
            dir = mBrickPath+shortName
            #dir_Cl = dir + "/dev/maya/" + dictAdd['shortName'] + "_Cl.ma"
            dir_LOD = dir + "/dev/maya/" + shortName +'_LOD'+ str(lodNumber) + ".ma"
            if not os.path.exists(str(dir)):
                dirMaya = 'mkdir -p ' + dir + "/dev/maya/"
                os.system(dirMaya)
                dirIcon = 'mkdir -p ' + dir + "/images/icon"
                os.system(dirIcon)
                dirIcon = dir + "/images/icon/" + shortName + '.png'
                print dirIcon
                shutil.copy(tempIcon, dirIcon)
                ### Render a icon
            if not os.path.exists(dir_LOD):
                try:
                    cmds.group(cmds.duplicate( longName, name = shortName, renameChildren=True), name = shortName + '_Grp', world=True)
                    cmds.sets(shortName, e = True, forceElement = 'initialShadingGroup')
                    cmds.setAttr(shortName+".t",0,0,0,type="double3")
                    cmds.setAttr(shortName+".r",0,0,0,type="double3")
                    cmds.setAttr(shortName+".s",l=False,type="double3")
                    cmds.setAttr(shortName+".s",1,1,1,type="double3")
                    deleteList = 'LEGO_materialID','LEGO_brickID','LEGO_groupID','LEGO_objectUniqueID','LEGO_brickRefID','LEGO_modifyDate','LEGO_DTuvset','LEGO_DTmap1created','LEGO_DTobjUniqueID','LEGO_DTcolorID','LEGO_DTname','LEGO_DTdecoID','LEGO_brickLOD'
                    for delAttr in deleteList:
                        try:
                            cmds.setAttr(shortName+'.'+delAttr,lock=False)
                        except:
                            pass
                        try:
                            cmds.deleteAttr(shortName,at=delAttr)
                        except:
                            pass
                    try:
                        cmds.deleteAttr(cmds.pickWalk(shortName, direction='down')[0],at='LEGO_materialID')
                    except:
                        pass
                except:
                    pass
                cmds.select(shortName+"_Grp")
                cmds.file(dir_LOD, f=True, options="V=0", type="mayaAscii", es=True)
                print dir_LOD+" has been exported."
                cmds.delete(shortName+"_Grp")
def exportShaders(self):
    #Find all phongE shaders and create a clean list without duplicates
    sList = cmds.ls(type='phongE')
    cleanList = []
    #print 'sList', sList
    pattern = "(\w+?)(?=\d+$)"
    #pattern = "(\D+)"
    patternEndNumber = "(\d+)"
    for s in sList:
        #print s
        match = re.search(pattern,s)
        #print match
        if match:
            noNumberName = match.group()
            #print noNumberName
            if not noNumberName in cleanList:
                cleanList.append(noNumberName)
        if not match:
            if not s in cleanList:
                cleanList.append(s)
    print 'cleanList', cleanList
    
    #Path to xml
    xml_file = os.path.abspath("/home/admin/Desktop/")
    xml_file = os.path.dirname(xml_file+"/")
    xml_file = os.path.join(xml_file, "legoS.xml")
    
    #Read the xml
    try:
        tree = ET.parse(xml_file)
    except Exception, inst:
        print "Unexpected error opening %s: %s" % (xml_file, inst)
        return
    
    #Root is the whole xml
    root = tree.getroot()
    
    #Go through the cleanList and get the values from the shaders
    for each in cleanList:
        try:
            ### Get id from the object
            cmds.hyperShade(objects=each)
            objList = cmds.ls(selection=True)
            print objList
            objID = cmds.getAttr(objList[0]+".LEGO_materialID")
            if objID<10:
                objID = "00"+str(objID)
            if objID<100:
                objID = "0"+str(objID)
            lID = objID
        except:
            #lID = "none"
            cmds.select(each)
            sgName = cmds.listConnections(type="shadingEngine",destination=True)
            nID = re.split(patternEndNumber,str(sgName))
            lID = nID[1]
            pass
        lShader = each
        try:
            lRed = cmds.getAttr(lShader+'.colorR')
            lGreen = cmds.getAttr(lShader+'.colorG')
            lBlue = cmds.getAttr(lShader+'.colorB')
            lRGB = int(lRed*255), int(lGreen*255) , int(lBlue*255)
            print lRGB
        except:
            pass
        newChild=[]
        for child in root:
            newChild.append(child.get("name"))
            child.append()
        if not lShader in newChild:
            #create the child
            child = ET.Element("legoS",name=str(lShader),oldRGB=str(lRGB),newRGB="0,0,0",ID=str(lID),transparent="False",metallic="False",chrome="False",pearl="False",glow="False",glitter="False",neon="False")
            #now append the shader to the root
            root.append(child)
    
    #Save the xml again
    save(xml_file, root)    
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(str(rough_string))
    return reparsed.toprettyxml(indent="")
    
    f = open(xml_file, 'w')
    if elem:
        try:
            clean = prettify(elem)
        except Exception as e:
            print e
        print clean
        for line in clean.split('\n'):
            if line.strip():
                f.write('%s\n' % line)
    else:
        f.write(prettify(ET.Element( 'root' )))
        
    f.close()
def replaceBricks(self):
    try:
        libraryPath = '/dsPipe/Library/asset/3D/Bricks/mBricks/'
        texturePath = '/dsPipe/Library/asset/3D/Bricks/LEGO_Colors/'
        try:
            name = cmds.ls('m*',long=True,type='transform',geometry=False,dependencyNodes=False,dagObjects=False,shapes=False,textures=False,materials=False)
            for each in name:
                shapeList=[]
                #print 'each='+each
                meshName = each.split('|')[-1]
                #print 'meshName='+str(meshName)
                shapeName = cmds.listRelatives(each,type='shape')[-1]
                shapeList = cmds.ls(shapeName, long=True)[0]
                #print 'shapeName='+shapeName
                #print 'shapeList='+shapeList
                materialID = 0
                try:
                    IDPath = shapeList+'.LEGO_materialID'
                    #print 'IDPath='+IDPath
                    materialID = cmds.getAttr(IDPath)
                    materialID = '%03d' % materialID
                    #print 'materialID=',materialID
                except:
                    try:
                        shapeS = cmds.listConnections( shapeName,t="shadingEngine",s=True)[0]
                        shaderS = cmds.listConnections(shapeS,t="phongE")[0]
                        pattern = "(\D+)"
                        nameShader = re.search(pattern,shaderS)
                        nameShader = nameShader.group()
                        #print nameShader
                        lRed = cmds.getAttr(shaderS+'.colorR')
                        lGreen = cmds.getAttr(shaderS+'.colorG')
                        lBlue = cmds.getAttr(shaderS+'.colorB')
                        lRGB = int(lRed*255), int(lGreen*255) , int(lBlue*255)
                        #print lRGB
                        root = Lego_Assign_Shader.readLegoSXML()
                        for child in root:
                            if child.get("oldRGB") == lRGB:
                                materialID = child.get("ID")
                            else:
                                if child.get("name") == nameShader:
                                    materialID = child.get("ID")
                    except:
                        materialID = "000"
                        pass
                #print materialID
                removeLong = meshName.split('|')[-1]
                #print 'removeLong='+removeLong
                nName = removeLong.split('_')[0]
                #print 'nName='+nName
                #filePath = libraryPath +"/" + nName +'_LOD2.ma'
                filePath = libraryPath + nName + '/dev/maya/' + nName +'_Cl.ma'
                #print 'file dont exist = '+filePath
                if not os.path.exists(filePath):
                    print 'Not cleaned = '+filePath
                    pass
                else:
                    #print 'filePath='+filePath
                    importedFile = cmds.file( filePath, r=True, type='mayaAscii',returnNewNodes=True, namespace='LOD')
                    last = importedFile[-1]
                    #print 'last='+last
                    lastSplit = last.split('|')[1]
                    shadingAssign = last.split('|')[2]
                    #print 'lastSplit='+lastSplit
                    if materialID == 0:
                        shadingGrp = cmds.listConnections(shapeList, type="shadingEngine")[0]
                        #print 'shadingGrp='+shadingGrp
                        cmds.sets(shadingAssign, forceElement = shadingGrp)
                    else:
                        ### It looks at the materialID fetches that texture and assigns it to a Vray shader and assign it too the brick....
                        try:
                            print materialID
                            shader = Lego_Assign_Shader.main(materialID)
                        except Exception as e:
                            print e
                            print 'fail creating shadingNode'
                            pass
                        try:
                            cmds.sets(name='LegoS_'+str(materialID)+'SG', empty = True,renderable = True,noSurfaceShader = True)
                        except:
                            print 'fail creating SG'
                            pass
                        try:
                            cmds.connectAttr('LegoS_'+str(materialID)+'.outColor', 'LegoS_'+str(materialID)+'SG.surfaceShader',f = True)
                        except:
                            print 'fail connecting'
                            pass
                        try:
                            cmds.sets(shadingAssign, forceElement = 'LegoS_'+str(materialID)+'SG')
                        except:
                            print 'fail connecting mesh to shader'
                            pass
                    ### Parents back to the groupe it was from...
                    cmds.parent( lastSplit, cmds.pickWalk( each, direction='up' ))
                    ### Copys location and so on..
                    cmds.copyAttr(each ,lastSplit ,inConnections=True,values=True)
                    ### Deletes the old brick...
                    cmds.delete(each)
        except Exception as e:
            print 'ERROR:', e
            print 'Fail sort names'
            pass
    except Exception as e:
        print 'ERROR:', e
        print 'fail'
        pass
def replaceShaders(self):
    #materialID = "297"
    #print materialID
    root = readLegoSXML()
    RGB = searchRGBLegoSXML(root,materialID)
    sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl = searchAttrLegoSXML(root,materialID)
    shader = CreateLegoShader(RGB,materialID,sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl)
    return shader
    
    ###readLegoSXML
    xml_file = os.path.abspath("/dsGlobal/dsCore/maya/mBricks/")
    xml_file = os.path.dirname(xml_file+"/")
    xml_file = os.path.join(xml_file, "legoS.xml")
    #Read the xml
    try:
        tree = ET.parse(xml_file)
    except Exception, inst:
        print "Unexpected error opening %s: %s" % (xml_file, inst)
        return    
    #Root is the whole xml
    root = tree.getroot()
    return root
    
    ###searchRGBLegoSXML
    ### Serch xml for ID get RGB
    RGB = "0,0,0"
    for subelement in root:
        if subelement.get("ID") == str(materialID):
            if subelement.get("newRGB") == "0,0,0":
                if subelement.get("oldRGB") == "(0, 0, 0)":
                    RGB = "255,0,255"
                    print materialID+" Has no color assigned"     
                else:
                    RGB = subelement.get("oldRGB")
                    print "Old RGB assigned"
            else:
                RGB = subelement.get("newRGB")
                print "New RGB assigned"
    return RGB
    
    ###searchAttrLegoSXML
    sTransparent = 0
    sChrome = 0
    sGlitter = 0
    sGlow = 0
    sMetallic = 0
    sNeon = 0
    sPearl = 0
    for subelement in root:
        if subelement.get("ID") == materialID:
            if subelement.get("chrome")=="True":
                sChrome = 1
            if subelement.get("glitter")=="True":
                sGlitter = 1
            if subelement.get("glow")=="True":
                sGlow = 1
            if subelement.get("metallic")=="True":
                sMetallic = 1
            if subelement.get("neon")=="True":
                sNeon = 1
            if subelement.get("pearl")=="True":
                sPearl = 1
            if subelement.get("transparent")=="True":
                sTransparent = 1
    return sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl
    
    ###CreateLegoShader
    ### Create Shader with correct name
    try:
        cmds.select('LegoS_'+ str(materialID))
        print 'LegoS_'+ str(materialID)+" allready exist"
    except:
        print 'LegoS_'+ str(materialID)+" created"
        shader = 'LegoS_'+ str(materialID)
        ### 
        ### Regular expression to remove , and ( then split out into the 3 different colors
        p = re.compile('\d+')
        RGB = p.findall(RGB)
        print RGB
        R = float(RGB[0])/255
        G = float(RGB[1])/255
        B = float(RGB[2])/255
        ### Create Vray shader with correct name:
        cmds.shadingNode( 'VRayMtl' , asShader=True, name=shader)
        ### Sett global
        cmds.setAttr(shader+".roughnessAmount", 0.15)
        cmds.setAttr(shader+".hilightGlossinessLock", 0)
        cmds.setAttr(shader+".hilightGlossiness", 0.6)
        cmds.setAttr(shader+".reflectionColorAmount", 0.15)
        cmds.setAttr(shader+".reflectionColor", 1,1,1)
        
        cmds.setAttr(shader+".refractionIOR", 1.460)
        
        cmds.setAttr(shader+".traceReflections", 0)
        cmds.setAttr(shader+".traceRefractions", 0)
        cmds.setAttr(shader+".refractionsMaxDepth", 1)
        cmds.setAttr(shader+".reflectionsMaxDepth", 1)
        ### Sett Diffuse color:
        cmds.setAttr(shader+".diffuseColor", R,G,B)
        ### Sett Transparency
        if sTransparent == 1:
            cmds.setAttr(shader+".refractionColorAmount", 1)
            cmds.setAttr(shader+".refractionColor", R/1.5,G/1.5,B/1.5)
            cmds.setAttr(shader+".traceRefractions", 1)
            cmds.setAttr(shader+".refractionsMaxDepth", 3)
        ### Sett Metallic
        if sMetallic == 1:
            cmds.setAttr(shader+".hilightGlossinessLock", 1)
            cmds.setAttr(shader+".hilightGlossiness", 1)
            cmds.setAttr(shader+".reflectionsMaxDepth", 2)
            cmds.setAttr(shader+".useFresnel", 1)
            cmds.setAttr(shader+".reflectionColor", 1,1,1)
            cmds.setAttr(shader+".reflectionColorAmount", 1)
            cmds.setAttr(shader+".traceReflections", 1)
        ### Sett Chrome
        if sChrome == 1:
            cmds.setAttr(shader+".hilightGlossinessLock", 1)
            cmds.setAttr(shader+".hilightGlossiness", 1)
            cmds.setAttr(shader+".reflectionsMaxDepth", 3)
            cmds.setAttr(shader+".useFresnel", 0)
            cmds.setAttr(shader+".reflectionColor", 1,1,1)
            cmds.setAttr(shader+".reflectionColorAmount", 0.5)
            cmds.setAttr(shader+".traceReflections", 1)
        ### Sett Pearl
        if sPearl == 1:
            cmds.setAttr(shader+".hilightGlossinessLock", 1)
            cmds.setAttr(shader+".hilightGlossiness", 1)
            cmds.setAttr(shader+".reflectionsMaxDepth", 1)
            cmds.setAttr(shader+".reflectionGlossiness", 0.6)
            cmds.setAttr(shader+".useFresnel", 0)
            cmds.setAttr(shader+".reflectionColor", R/2,G/2,B/2)
            cmds.setAttr(shader+".reflectionSubdivs", 5)
            cmds.setAttr(shader+".traceReflections", 1)
        ### Sett Neon
        if sNeon == 1:
            cmds.setAttr(shader+".illumColor", 0.2,0.2,0.2)
        ### Sett Glow    
        if sGlow == 1:
            cmds.setAttr(shader+".illumColor", 0.2,0.2,0.2)
        ### Sett Glitter
        if sGlitter == 1:
            sFlakes = shader+"_Flakes"
            sBlend = shader+"_Blend"
            cmds.shadingNode('VRayFlakesMtl' , asShader=True, name=sFlakes)
            cmds.shadingNode('VRayBlendMtl' , asShader=True, name=sBlend)
            cmds.connectAttr(shader+'.outColor',sBlend+'.base_material')
            cmds.connectAttr(sFlakes+'.outColor',sBlend+'.coat_material_0')
            shader = sBlend
        print shader
        return shader