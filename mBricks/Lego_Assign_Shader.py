import maya.cmds as cmds
import re
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os
def main(materialID):
    #materialID = "297"
    #print materialID
    root = readLegoSXML()
    RGB = searchRGBLegoSXML(root,materialID)
    sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl = searchAttrLegoSXML(root,materialID)
    shader = CreateLegoShader(RGB,materialID,sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl)
    return shader
    
def readLegoSXML():
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
    
def searchRGBLegoSXML(root,materialID):
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
    
def searchAttrLegoSXML(root,materialID):
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
    
def CreateLegoShader(RGB,materialID,sTransparent,sChrome,sGlitter,sGlow,sMetallic,sNeon,sPearl):
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
if __name__ == "__main__":
    # Someone is launching this directly
    pass