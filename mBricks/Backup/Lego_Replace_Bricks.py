#-------------------------------------------------------------------------------
# Name:        LegoReplaceBricks_Master.py
# Purpose:     import LegoBricks replacing bricks with refferences
#
# Author:      Per Sundin
#
# Created:     18/1/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python
name = ()
import os
import os.path
import maya.cmds as cmds
import shutil
class legoReplace:
    def DeleteUnUsed(self):
        try:
            #Delete unwanted nodes add too the list when found!!!!
            try:
                cmds.delete('STRETCH*')
            except:
                pass
            try:
                cmds.delete('oppe*')
            except:
                pass
            try:
                cmds.delete('nede*')
            except:
                pass
            try:
                cmds.delete('LXFMLImport*')
            except:
                pass
            try:
                cmds.delete('DONT_TOUCH*')
            except:
                pass
            try:
                cmds.delete('column*')
            except:
                pass
            try:
                cmds.delete('LEGO_EasyFlex*')
            except:
                pass
            try:
                cmds.delete('EasyFlexControl*')
            except:
                pass
            try:
                cmds.delete('EasyFlexStart*')
            except:
                pass
            #try:
                #cmds.delete('stud*')
            #except:
                #pass
            try:
                cmds.delete('column*')
            except:
                pass
            try:
                cmds.delete('*EasyFlexDeformer*')
            except:
                pass
            try:
                cmds.delete('EasyFlexControl*')
            except:
                pass
            try:
                cmds.delete('*LEGO_scenePrefs*')
            except:
                pass
            try:
                cmds.delete('EasyFlexEnd*')
            except:
                pass
            try:
                delNurbs = cmds.ls(type='nurbsCurve*')
                cmds.delete(delNurbs)
            except:
                pass
            try:
                cmds.delete('Start*')
            except:
                pass
            try:
                cmds.delete('curv*')
            except:
                pass
            try:
                cmds.delete('Copy_of_BEND*')
            except:
                pass
            try:
                cmds.delete('BEND*')
            except:
                pass
            try:
                cmds.delete('Start*')
            except:
                pass
            try:
                cmds.delete('End*')
            except:
                pass
            try:
                cmds.delete('thin_column*')
            except:
                pass
            try:
                cmds.delete('Column*')
            except:
                pass
            try:
                cmds.delete('Column*')
            except:
                pass
            try:
                unkown = cmds.ls(type='unknown')
                cmds.select(unkown)
                cmds.delete()
            except:
                pass
        except:
            print 'Failed on DeleteUnwandted'
            pass
    def Rebuild(self):
        try:
            libraryPath = '/dsPipe/Library/asset/3D/Bricks/mBricks/'
            texturePath = '/dsPipe/Library/asset/3D/Bricks/LEGO_Colors/'
            #libraryPath = 'C:\Users\Per\Documents\Test'
            #print 'libraryPath='+libraryPath
            try:
                name = cmds.ls('m*',long=True,type='transform',geometry=False,dependencyNodes=False,dagObjects=False,shapes=False,textures=False,materials=False)
                for each in name:
                    #list()
                    shapeList=[]
                    #print 'each='+each
                    meshName = each.split('|')[-1]
                    #print 'meshName='+str(meshName)
                    shapeName = cmds.listRelatives(each,type='shape')[-1]
                    shapeList = cmds.ls(shapeName, long=True)[0]
                    #print 'shapeName='+shapeName
                    #print 'shapeList='+shapeList
                    #cmds.select('|Model|Wagon|Gandalf|Hip|Body|m3814_MINI_UPPER_PART_0|m3814_MINI_UPPER_PART_Shape0.LEGO_materialID')
                    materialID = 0
                    try:
                        IDPath = shapeList+'.LEGO_materialID'
                        #print 'IDPath='+IDPath
                        materialID = cmds.getAttr(IDPath)
                        #print 'materialID=',materialID
                    except:
                        pass
                    removeLong = meshName.split('|')[-1]
                    #print 'removeLong='+removeLong
                    nName = removeLong.split('_')[0]
                    #print 'nName='+nName
                    #filePath = libraryPath +"/" + nName +'_LOD2.ma'
                    filePath = libraryPath + nName + '/Dev/Maya/' + nName +'_Cl.ma'
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
                                shader = 'LegoS_'+str(materialID)
                                cmds.shadingNode( 'VRayMtl' , asShader=True, name=shader)
                                texturePath = '/dsPipe/Library/Asset/Bricks/LEGO_Colors/'+str(materialID)+'.png'
                                inTexture = 'color_'+str(materialID)
                                outTexture = 'place2dTexture_color_'+str(materialID)
                                cmds.shadingNode('file',name = inTexture, asTexture=True);
                                cmds.shadingNode('place2dTexture',name = outTexture, asUtility = True)
                                cmds.connectAttr(outTexture+'.outUV', inTexture+'.uvCoord', f=True)
                                cmds.connectAttr(outTexture+'.outUvFilterSize', inTexture+'.uvFilterSize', f=True)
                                cmds.connectAttr(outTexture+'.coverage', inTexture+'.coverage', f=True)
                                cmds.connectAttr(outTexture+'.translateFrame', inTexture+'.translateFrame', f=True)
                                cmds.connectAttr(outTexture+'.rotateFrame', inTexture+'.rotateFrame', f=True)
                                cmds.connectAttr(outTexture+'.mirrorU', inTexture+'.mirrorU', f=True)
                                cmds.connectAttr(outTexture+'.mirrorV', inTexture+'.mirrorV', f=True)
                                cmds.connectAttr(outTexture+'.stagger', inTexture+'.stagger', f=True)
                                cmds.connectAttr(outTexture+'.wrapU', inTexture+'.wrapU', f=True)
                                cmds.connectAttr(outTexture+'.wrapV', inTexture+'.wrapV', f=True)
                                cmds.connectAttr(outTexture+'.repeatUV', inTexture+'.repeatUV', f=True)
                                cmds.connectAttr(outTexture+'.vertexUvOne', inTexture+'.vertexUvOne', f=True)
                                cmds.connectAttr(outTexture+'.vertexUvTwo', inTexture+'.vertexUvTwo', f=True)
                                cmds.connectAttr(outTexture+'.vertexUvThree', inTexture+'.vertexUvThree', f=True)
                                cmds.connectAttr(outTexture+'.vertexCameraOne', inTexture+'.vertexCameraOne', f=True)
                                cmds.connectAttr(outTexture+'.noiseUV', inTexture+'.noiseUV', f=True)
                                cmds.connectAttr(outTexture+'.offset', inTexture+'.offset', f=True)
                                cmds.connectAttr(outTexture+'.rotateUV', inTexture+'.rotateUV', f=True)
                                cmds.setAttr(inTexture+'.fileTextureName',str(texturePath),type = "string" )
                                cmds.defaultNavigation(destination=shader, source=inTexture, connectToExisting=True)
                                cmds.setAttr(inTexture+'.filterType', 0)

                                cmds.setAttr(shader+'.brdfType', 0)
                                cmds.setAttr(shader+'.traceReflections', 0)
                                cmds.setAttr(shader+'.hilightGlossinessLock', 0)
                                cmds.setAttr(shader+'.reflectionColor',0.2, 0.2, 0.2, type="double3" )
                                cmds.setAttr(shader+'.hilightGlossiness',0.4)
                                cmds.setAttr(shader+'.reflectionsMaxDepth', 1)
                                cmds.setAttr(shader+'.refractionsMaxDepth', 1)
                            except:
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
    def Compute(self):
        self.DeleteUnUsed()
        self.Rebuild()
        pass
def Run():
    instance = legoReplace()
    instance.Compute()