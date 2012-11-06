## Clean dsFolder structure version 2.0

from xml.etree import ElementTree as ET
import os, platform, shutil,sys

def mkfile(filename, body=None):
    with open(filename, 'w') as f:
        f.write(body or filename)

def testDir(tmppath):
    if not os.path.isdir(tmppath):
        os.makedirs(str(tmppath))
        return False
    else:
        return True

def changePath(path, arg):
    path = str(path)
    if arg == 'dsComp':
        if sys.platform == 'win32':
            if path[0].lower() == 'p':
                path = path.replace('%s:' % (path[0]), '//xserv2/VFXSAN/dsComp')
            else:
                path = path.replace('//vfx-data-server/dsPipe', '//xserv2/VFXSAN/dsComp')
        else:
            path = path.replace('/dsPipe', '/mounts/san/dsComp')
    
    if arg == 'dsRender':
        if sys.platform == 'win32':
            if path[0].lower() == 'p':
                path = path.replace('%s:' % (path[0]), '//framestore/pipeline/dsRender')
            else:
                path = path.replace('//vfx-data-server/dsPipe', '//framestore/pipeline/dsRender')
            
        else:
            path = path.replace('/dsPipe', '/mnt/vfxpipe/dsRender')

    if not os.path.exists(path):
        if sys.platform == 'win32':
            path = path.replace('/', '\\')
            if path.endswith('.nk'):
                mkfile(path)
            else:
                try:
                    os.makedirs(path)
                    print 'win making:', path
                except Exception as e:
                    print 'ERROR: %s' % e
        else:
            if path.endswith('.nk'):
                mkfile(path)
            else:
                try:
                    os.makedirs(path)
                    print 'making:', path
                except Exception as e:
                    print 'ERROR: %s' % e
    if path:
        return path
    else:
        return None

def mkSymlink(path):
    print 'mkSymlink'
    symlink = path.replace("/dsPipe",'/mounts/san/dsComp')
    #symlink = '%s%s' % ( '/mounts/san/dsComp', path)
    if sys.platform == 'linux2':
        if not os.path.exists(symlink):
            os.makedirs(symlink)
            os.symlink( symlink, path)
            return False
        else:
            if not os.path.exists(symlink):
                shutil.move(path, symlink)
                os.symlink( symlink, path)
            return True
    else:
        print sys.platform
    
def testType(val,tmppath):
    if val == "file":
        if not os.path.isfile(tmpPath):
            tmppath = changePath(tmppath, 'dsComp') 
            mkfile(tmppath)
    if val == "folder":
        testDir(tmppath)
    if val == "symlink":
        mkSymlink(tmppath)
    if val == "dsComp" or val == "dsRender":
        changePath(tmppath, val)
        
def dsCreateFs(TYPE,path,name):
    if platform.system() == "Linux":
        if TYPE == "COMP":
            XMLPath ='/dsGlobal/dsCore/tools/dsProjectCreate/compWorkflow.xml'
        if TYPE == "3D":
            XMLPath ='/dsGlobal/dsCore/tools/dsProjectCreate/3DWorkflow.xml'
        if TYPE == "PROJECT":
            XMLPath ='/dsGlobal/dsCore/tools/dsProjectCreate/project.xml'
            resources = '/dsGlobal/globalTools/ressources/.local'
        if TYPE == "EPISODE":
            XMLPath ='/dsGlobal/dsCore/tools/dsProjectCreate/episode.xml'
            
    if platform.system() == "Windows":
        if TYPE == "COMP":
            XMLPath = '//vfx-data-server/dsGlobal/dsCore/tools/dsProjectCreate/compWorkflow.xml'
        if TYPE == "3D":
            XMLPath ='//vfx-data-server/dsGlobal/dsCore/tools/dsProjectCreate/3DWorkflow.xml'
        if TYPE == "PROJECT":
            XMLPath ='//vfx-data-server/dsGlobal/dsCore/tools/dsProjectCreate/project.xml'
            resources ='//vfx-data-server/dsGlobal/globalTools/ressources/.local'
        if TYPE == "EPISODE":
            XMLPath ='//vfx-data-server/dsGlobal/dsCore/tools/dsProjectCreate/episode.xml'

    ''' Creates folder structure from XML'''
    root = ET.parse(XMLPath).getroot()
    
    if TYPE == "PROJECT" or TYPE == "EPISODE":
        pathNew = path + name + "/"
        if testDir(pathNew) == False:
            for parent in root.getchildren():
                testType(parent.attrib['type'],pathNew + parent.attrib['name'])
                for child in parent.getchildren():
                    testType(child.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'])
                    for subchild in child.getchildren():
                        testType(subchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] +"/"+ subchild.attrib['name'])
                        for subsubchild in subchild.getchildren():
                            testType(subsubchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] + "/"+ subchild.attrib['name']+ "/"+ subsubchild.attrib['name'])                  
            print "created Folder structure for " + name
        else:
            print "Project or Episode folder structure for " + pathNew + " already exits!!"


    if TYPE == "3D":
        pathTest = path + name + "/3D/"
        if testDir(pathTest) == False:
            pathNew = path + name + "/"
            for parent in root.getchildren():
                testType(parent.attrib['type'],pathNew + parent.attrib['name'])
                for child in parent.getchildren():
                    testType(child.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'])
                    for subchild in child.getchildren():
                        testType(subchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] +"/"+ subchild.attrib['name'])
                        for subsubchild in subchild.getchildren():
                            testType(subsubchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] + "/"+ subchild.attrib['name']+ "/"+ subsubchild.attrib['name'])                  
            print "created Folder structure for " + name
        else:
            print "3D folder structure for " + pathNew + " already exits!!"
    
    
    if TYPE == "COMP":
        pathTest = path + name + "/comp/"
        if testDir(pathTest) == False:
            pathNew = path + name + "/"
            for parent in root.getchildren():
                testType(parent.attrib['type'],pathNew + parent.attrib['name'])
                for child in parent.getchildren():
                    testType(child.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'])
                    for subchild in child.getchildren():
                        testType(subchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] +"/"+ subchild.attrib['name'])
                        for subsubchild in subchild.getchildren():
                            testType(subsubchild.attrib['type'],pathNew + parent.attrib['name'] +"/"+ child.attrib['name'] + "/"+ subchild.attrib['name']+ "/"+ subsubchild.attrib['name'])                  
            print "created Folder structure for " + name
        else:
            print "comp folder structure for " + pathNew + " already exits!!"
            
    print str(pathNew)  + ".local"
    if not os.path.isdir(str(pathNew) + ".local"):
        if TYPE == 'PROJECT':
            shutil.copytree(str(resources),str(pathNew + "/.local"))
        