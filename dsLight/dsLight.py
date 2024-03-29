import maya.cmds as cmds
import maya.mel as mel

#find all lights in scene, supports vray light types
#print cmds.ls(lt=True) + cmds.ls(type='VRayLightRectShape') + cmds.ls(type='VRayLightDomeShape') + cmds.ls(type='VRayLightIESShape') + cmds.ls(type='VRayLightSphereShape')

#print cmds.nodeType(cmds.ls(selection=True))

#rElement = cmds.ls(type='VRayRenderElement')
#reList = cmds.ls(type='VRayRenderElementSet')

#for re in reList:
    #print cmds.getAttr(re+".vrayClassType")
    
def dsCreateLight(name,type):
    # name of the light and what type of light to create
    
    if len(cmds.ls(str(name))) >= 1:
        print "Light alread named in scene ... please rename confilicting lights..."
    else:
        if type == "vraySphere":
            light = cmds.shadingNode ('VRayLightSphereShape', asLight=True)
            cmds.rename(str(light),str(name))
        if type == "vrayDome":
            light = cmds.shadingNode ('VRayLightDomeShape', asLight=True)
            cmds.rename(str(light),str(name))
        if type == "vrayRect":
            light = cmds.shadingNode ('VRayLightRectShape', asLight=True)
            cmds.rename(str(light),str(name))
        if type == "vrayIES":
            light = cmds.shadingNode ('VRayLightIESShape', asLight=True)
            cmds.rename(str(light),str(name))
        if type == "ambient":
            light = mel.eval('string $light = `ambientLight -n ' + name + '`;')
        if type == "directional":
            light = mel.eval('string $light = `directionalLight -n ' + name + '`;')
        if type == "point":
            light = mel.eval('string $light = `pointLight -n ' + name + '`;')
        if type == "spot":
            light = mel.eval('string $light = `spotLight -n ' + name + '`;')
        if type == "area":
            light = cmds.shadingNode ('areaLight', asLight=True)
            cmds.rename(str(light),str(name))
        if type == "volume":
            light = cmds.shadingNode ('volumeLight', asLight=True)
            cmds.rename(str(light),str(name))
    
        if not cmds.ls("light_Grp"):cmds.group( em=True, name='light_Grp' )
        cmds.parent(str(name),"light_Grp")
        return name
    
def createLS(preFix,light):

    if not cmds.ls(str(preFix + '_LS')):
        renderElement = mel.eval('vrayAddRenderElement LightSelectElement;')
        renderElement = cmds.rename(str(renderElement), str(preFix + '_LS') ) 
        cmds.sets(str(light), edit=True, forceElement=str(preFix + '_LS'))
        cmds.setAttr(str(renderElement) + ".vray_name_lightselect",str(preFix + '_LS'),type='string')
    else:
        #cmds.setAttr(str(preFix + '_LS') + ".vray_name_lightselect",str(preFix + '_LS'),type='string')
        cmds.sets(str(light), edit=True, forceElement=str(preFix + '_LS'))


