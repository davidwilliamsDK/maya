
import sys, re, os, shutil, subprocess, stat, string
import maya.cmds as cmds
import dsCommon.dsMetaDataTools as dsMDT
reload(dsMDT)
import dsCommon.dsOsUtil as dsOsUtil;reload(dsOsUtil)
import dsSQLTools as dsSQL


if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsCheck/dsSceneSave.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsCheck/dsSceneSave.ui'

import maya.cmds as cmds
import maya.OpenMayaUI as mui
pyVal = dsOsUtil.getPyGUI()
  
if pyVal == "PySide":
    from PySide import QtCore,QtGui
    from shiboken import wrapInstance
    form_class, base_class = dsOsUtil.loadUiType(uiFile)
    
if pyVal == "PyQt":
    from PyQt4 import QtGui, QtCore, uic
    import sip
    form_class, base_class = uic.loadUiType(uiFile)

def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    if pyVal == "PySide":
        return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    else:
        return sip.wrapinstance(long(main_window_ptr), QtCore.QObject)

class Window(base_class, form_class):

    def __init__(self, parent=getMayaWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.taskList = ['blocking','anim','light','effect','template']
                    
        if sys.platform == "linux2":
            self.home = os.getenv("HOME")
            self.config_dir = '%s/.shotOpen' % (self.home)
            self.config_path = '%s/config.ini' % (self.config_dir)
            self.dsPipe = "/dsPipe"
            self.dsPipe = "/dsPipe"
            self.emptyMA = '/dsGlobal/globalMaya/Resources/emptyScene.ma'

        elif sys.platform == 'win32':
            self.home = 'C:%s' % os.getenv("HOMEPATH")
            self.config_dir = '%s/.shotOpen' % (self.home)
            self.config_dir = self.config_dir.replace("/","\\")
            self.config_path = '%s/config.ini' % (self.config_dir)
            self.config_path = self.config_path.replace("/","\\")
            self.dsPipe = "//vfx-data-server/dsPipe"
            self.emptyMA = '//vfx-data-server/dsGlobal/globalMaya/Resources/emptyScene.ma'
        
        
        self.init_projects()
        
        self.projects_CB.currentIndexChanged.connect(self.init_episodes)
        self.episodes_CB.currentIndexChanged.connect(self.init_sequences)
        self.sequence_CB.currentIndexChanged.connect(self.init_tasks)
        self.task_CB.currentIndexChanged.connect(self.updateFN)
        self.nn_LE.textChanged.connect(self.updateFN)
        
        self.save_B.clicked.connect(self.saveScene)

        self.load_config()

    def init_projects(self):
        '''
        Adds projects to self.projects
        Only if the project contains a /Local/config.xml
        '''
        self.projects_CB.clear()
        list = []
        
        tmpList = dsSQL.getValueDB("U:/globalProjects","Projects","Status",'Active')

        for t in tmpList:
            list.append(t[1])
        list.sort()
        for project in list:
            self.projects_CB.addItem(project)

    def init_episodes(self):
        '''
        Adds episodes to self.episodes
        '''
        self.episodes_CB.clear()
        pr = self.projects_CB.currentText()
        
        self.epiRootPath = self.dsPipe + "/" + pr + "/film/"
        tmpList = os.listdir(self.epiRootPath)

        for t in tmpList:
            if t[0] != ".":
                self.episodes_CB.addItem(t)

    def init_sequences(self):
        '''
        Adds sequences to self.sequences
        Searches after pattern is [qQ][0-9][0-9][0-9][0-9]
        '''
        self.sequence_CB.clear()
        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        
        self.seqRootPath = self.dsPipe + "/" + pr + "/film/" + ep + "/"
        tmpList = os.listdir(self.seqRootPath)

        for t in tmpList:
            if t[0] != ".":
                if re.search("q[0-9][0-9][0-9][0-9]",t):
                    self.sequence_CB.addItem(t)

    def init_tasks(self):
        '''
        Adds tasks to self.task_CB
        '''
        self.task_CB.clear()
        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        sq = self.sequence_CB.currentText()
        
        self.task_CB.addItem("data")
        if ep != "":
            if sq != "":
                self.seqRootPath = self.dsPipe + "/" + pr + "/film/" + ep + "/" + sq + "/3D/"
                tmpList = os.listdir(self.seqRootPath)     
                for t in self.taskList:
                    self.task_CB.addItem(t)
                    
        self.updateFN()

    def updateFN(self):

        #ext = item[-3:]        

        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        sq = self.sequence_CB.currentText()
        tk = self.task_CB.currentText()
        nn = self.nn_LE.text()
        self.ext = string.rsplit(cmds.file(q=True,sn=True),"/",1)[1].split(".")[-1]
        
        if tk is not "data":
            self.taskRootPath = self.seqRootPath + str(tk) + "/"
            
            if nn == "":
                self.sceneName = str(sq)+"_"+str(tk) + "." + self.ext
            else:
                if re.search("s[0-9][0-9][0-9][0-9]",nn):
                    self.sceneName = str(sq)+"_"+str(nn)+ "_"+str(tk)+"." + self.ext
                else:
                    self.sceneName = str(sq)+"_"+str(tk)+"_"+str(nn) +"." + self.ext
            
            self.fn_LE.setText(self.sceneName)
        if str(tk) == "data":
            if nn == "":
                self.sceneName = str(sq) + "_" + "." + self.ext
            else:
                if re.search("s[0-9][0-9][0-9][0-9]",nn):
                    self.sceneName = str(sq)+"_"+str(nn)+ "." + self.ext
                else:
                    self.sceneName = str(sq)+"_"+str(nn) + "." + self.ext
            
            self.fn_LE.setText(self.sceneName)
        
    def saveScene(self):
        tk = self.task_CB.currentText()

        if tk is not "data":
            destFile = str(self.taskRootPath) + str(self.sceneName)
            if os.path.isfile(destFile):
                print "file already Present overwrite or notate"
            else:
                print "saving file :" + self.sceneName
                print "here : " + self.taskRootPath
                cmds.file(rename=destFile)
                #cmds.file( save=True, type='mayaAscii',force=True)
                
                dsMDT.testMDNode()
                self.close()
                if self.ext == "ma":
                    cmds.file( save=True, type='mayaAscii',force=True)
                else:
                    cmds.file( save=True, type='mayaBinary',force=True)
                    
        if str(tk) == "data":
            path =self.seqRootPath + tk + "/export/" + self.sceneName
            print path
            
            if self.ext == "ma":
                cmds.file(path,es=True,type='mayaAscii',force=True,pr=True)
            else:
                cmds.file(path,es=True,type='mayaBinary',force=True,pr=True)

            
    def load_config(self):
        '''
        Load config which is a dictionary and applying setting.
        '''
        if os.path.exists(self.config_path):
            print 'Loading config file from:', self.config_path
            config_file = open( '%s' % self.config_path, 'r')
            list = config_file.readlines()
            config_file.close()

            config = {}
            for option in list:
                key, value = option.split('=')
                config[key] = value.strip()

            try:
                index = [i for i in range(self.projects_CB.count()) if self.projects_CB.itemText(i) == config.get('PROJECT')][0]
                self.projects_CB.setCurrentIndex(index)

                index = [i for i in range(self.episodes_CB.count()) if self.episodes_CB.itemText(i) == config.get('EPISODE')][0]
                self.episodes_CB.setCurrentIndex(index)

                index = [i for i in range(self.sequence_CB.count()) if self.sequence_CB.itemText(i) == config.get('SEQUENCE')][0]
                self.sequence_CB.setCurrentIndex(index)

                index = [i for i in range(self.task_CB.count()) if self.task_CB.itemText(i) == config.get('TASK')][0]
                self.task_CB.setCurrentIndex(index)

            except:
                print "error reseting config file"
                os.remove(self.config_path)

    #def closeEvent(self,event):
        #self.save_config()
            
def dsSS():
    global myWindow
    myWindow = Window()
    myWindow.show()