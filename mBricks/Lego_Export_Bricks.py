#-------------------------------------------------------------------------------
# Name:        LegoCleanup_Master.py
# Purpose:     Too export clean lego bricks too library and re import them later
#
# Author:      Per Sundin
#
# Created:     18/1/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        LegoCleanup.py
# Purpose:     Too export clean lego bricks too library and re import them later
#
# Author:      Per Sundin
#
# Created:     18/1/2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import os
import os.path
import maya.cmds as cmds
import shutil
class legoExport:
    def __init__(self):
        try:
            exportPath.self = '/home/administrator/Documents/Test/'
            self.list = []
            self.glist = []
            cmds.select(all=True)
            cmds.sets( e=True, forceElement= 'initialShadingGroup')
            cmds.select(cl=True)
        except:
            pass
    def DeleteUnwanted(self):
        try:
            #Delete unwanted nodes add too the list when found!!!!
            try:
                cmds.delete('STRETCH')
            except:
                pass
            try:
                cmds.delete('oppe')
            except:
                pass
            try:
                cmds.delete('nede')
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
                cmds.delete('SONT_TOUCH*')
            except:
                pass
            try:
                cmds.delete('column')
            except:
                pass
            try:
                cmds.delete('LEGO_EasyFlex*')
            except:
                pass
            try:
                cmds.delete('EasyFlexControl')
            except:
                pass
            try:
                cmds.delete('EasyFlexStart*')
            except:
                pass
            try:
                cmds.delete('*EasyFlexDeformer*')
            except:
                pass
            try:
                cmds.delete('EasyFlexControl')
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
                delNurbs = cmds.ls(type='nurbsCurve')
                cmds.delete(delNurbs)
            except:
                pass
            try:
                cmds.delete('Start')
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
    def ReOrganize(self):
        try:
            cmds.select(all=True,hi=False)
            OldGroupe = cmds.ls(selection=True)
            cmds.select('m*')
            cmds.parent(world=True)
            cmds.group(name='ReGroup')
            cmds.select(cl=True)
            cmds.delete(OldGroupe)
            print 'reorganize'
        except:
            print 'Failed on ReOrganize'
            pass
    def ListWanted(self):
        try:
            self.list = cmds.ls('m*')
        except:
            print 'Failed on ListWanted'
            pass
    def CorrectNames(self):
        value = 0
        for each in self.list:
            name=each.split('_')[0]
            if not name in self.list:
                if not cmds.objExists(name):
                    cmds.rename(each, name)
                    self.list.append(name)
                    cmds.setAttr(name + '.scale', lock=False)
                    #Move to 0 ,rotate to 0 and scale to
                    cmds.select(name, r = True)
                    cmds.parent(world=True)
                    cmds.move(0, 0, 0)
                    cmds.rotate(0, 0, 0)
                    cmds.scale(1, 1, 1)
                    cmds.select( clear=True )
                    #Groupe
                    cmds.group( name, n= name + '_Grp', world = True )
                    if value == 1:
                        cmds.parent( name + '_Grp', 'Export', relative=True )
                    else:
                        value = 1
                        cmds.group( name + '_Grp' ,n= 'Export', world=True )
    def ExportGrp(self):
        try:
            self.glist = cmds.ls('m*' + '_Grp')
        except:
            pass
    def ExportToLibrary(self):
        #Deletes ReGroup before export!
        cmds.delete('ReGroup')
        try:
            cmds.delete(all=True,constructionHistory=True)
        except:
            pass
        for each in self.glist:
            grpName = each
            meshName = each.split('_')[0]
            shapeName = 'mShape'+ meshName.split('m')[1]
            #path = "C:\Users\Per\Documents\Test/"
            #icon = "C:\Users\Per\Documents\Test\Empty.png"
            #dir = path
            #dirIcon = path
            path = '/dsPipe/Library/asset/3D/lego/mBrick/'
            icon = '/dsPipe/Library/.local/Resources/Icons/Empty.png'
            dir = path + meshName + '/dev/maya/'
            dirIcon = path + meshName + '/images/icon/'
            LOD = 0
            try:
                LOD = cmds.getAttr(meshName + ".LEGO_brickLOD")
                cmds.setAttr(meshName+".LEGO_brickLOD",lock=False)
                cmds.deleteAttr(meshName, at="LEGO_brickLOD")
            except:
                pass
            listAll = cmds.ls()
            if LOD in range(0,6):
                name = dir + meshName + '_LOD' + str(LOD) + '.ma'
            else:
                name = '_LODNone'
            if not os.path.exists(name):
                for object in listAll:
                    try:
                        try:
                            cmds.deleteAttr(object, at="LEGO_materialID")
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_brickID')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_groupID')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_objectUniqueID')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_brickRefID')
                        except:
                            pass
                        try:
                            cmds.setAttr(object+'.LEGO_modifyDate',lock=False)
                            cmds.deleteAttr(object,at='LEGO_modifyDate')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTuvset')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTmap1created')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTobjUniqueID')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTcolorID')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTname')
                        except:
                            pass
                        try:
                            cmds.deleteAttr(object,at='LEGO_DTdecoID')
                        except:
                            pass
                    except:
                        pass
            try:
                if not os.path.exists(dir):
                    cmd = 'mkdir -p ' + dir
                    os.system(cmd)
                    print dir
                if not os.path.exists(dirIcon):
                    cmd = 'mkdir -p ' + dirIcon
                    os.system(cmd)
                    shutil.copy2(icon, dirIcon + '/' + each.split('_')[0] + '.png')
                    print dirIcon
                if not os.path.exists(name):
                    cmds.sets(meshName, e = True, forceElement = 'initialShadingGroup')
                    cmds.select(grpName)
                    cmds.parent(world=True)
                    cmds.file(name, f=True, options="V=0", type="mayaAscii", es=True)
                    print name
            except:
                pass
    def Compute(self):
        #Delete unwanted nodes
        self.DeleteUnwanted()
        #ReOrganize and delete old
        self.ReOrganize()
        #ListWanted m#### modelparts
        self.ListWanted()
        #CorrectNames Remove everything from first _ in m####_etc_etc_etc
        self.CorrectNames()
        #Make List too export
        self.ExportGrp()
        #ExportToLibrary make folder structure add file etc etc
        self.ExportToLibrary()
        pass
def Run():
    instance = legoExport()
    instance.Compute()

