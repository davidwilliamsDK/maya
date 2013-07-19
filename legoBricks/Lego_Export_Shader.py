#!/usr/bin/env python

from xml.etree import ElementTree as ET
from xml.dom import minidom
import re
import maya.cmds as cmds
import os
def main():
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
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(str(rough_string))
    return reparsed.toprettyxml(indent="")
    
def save(xml_file, elem=None):
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
if __name__ == "__main__":
	# Someone is launching this directly
	main()
