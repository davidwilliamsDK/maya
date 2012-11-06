from xml.etree import ElementTree as ET
from xml.dom import minidom
import os

def scanXML(dsPipe,dept):
    ''' creates list of all projects.. loops through to make Commercial and Lego lists'''
    dsProjectList = []
    legoXMLList = []
    legoList = []
    comXMLList = []
    comList = []
    tmpProjectList = os.listdir(dsPipe)
    for folder in tmpProjectList:
        if os.path.isfile(dsPipe + folder + "/.local/config.xml"):
            dsProjectList.append(folder)
    for proj in dsProjectList:
        XMLPath = dsPipe + proj + "/.local/config.xml"
        root = ET.parse(XMLPath).getroot()
        rootList = root.getchildren()
        for parent in root.getchildren():
            if parent.attrib['type'] == 'Department':
                if parent.attrib['name'] == "LEGO":
                    legoXMLList.append(root)
                else:
                    comXMLList.append(root)
    for elem in legoXMLList:
        for parent in elem.getchildren():
            if parent.attrib['type'] == "SHOW_LONG":
                legoList.append(parent.attrib['name'])
    for elem in comXMLList:
        for parent in elem.getchildren():
           if parent.attrib['type'] == "SHOW_LONG":
                comList.append(parent.attrib['name'])
    if dept == "LEGO":
        return legoList
    if dept == "ALL":
        return dsProjectList
    if dept == "Commercial":
        return comList