
import sys, sip, re, os, shutil, subprocess, stat
from PyQt4 import QtGui, QtCore, uic
import sgTools
import maya.cmds as cmds
import dsCommon.dsMetaDataTools as dsMDT
reload(dsMDT)


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsCheck/dsSceneSave.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsCheck/dsSceneSave.ui'
  
form_class, base_class = uic.loadUiType(uiFile)
class Window(base_class, form_class):

    def __init__(self, parent=None):
        base_class.__init__(self, parent)
        self.setupUi(self)

        self.taskList = ['blocking','anim','light','effect','template']

        if sys.platform == "linux2":
            self.dsPipe = "/dsPipe"
            self.emptyMA = '/dsGlobal/globalMaya/Resources/emptyScene.ma'

        elif sys.platform == 'win32':
            self.dsPipe = "//vfx-data-server/dsPipe"
            self.emptyMA = '//vfx-data-server/dsGlobal/globalMaya/Resources/emptyScene.ma'
        
        
        self.init_projects()
        
        self.projects_CB.currentIndexChanged.connect(self.init_episodes)
        self.episodes_CB.currentIndexChanged.connect(self.init_sequences)
        self.sequence_CB.currentIndexChanged.connect(self.init_tasks)
        self.task_CB.currentIndexChanged.connect(self.updateFN)
        self.nn_LE.textChanged.connect(self.updateFN)
        
        self.save_B.clicked.connect(self.saveScene)

    def init_projects(self):
        '''
        Adds projects to self.projects
        '''
        self.projects_CB.clear()
        list = []
        
        tmpList = sgTools.sgGetProjects()
        for t in tmpList:
            list.append(t['name'])
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

        if ep != "":
            if sq != "":
                self.seqRootPath = self.dsPipe + "/" + pr + "/film/" + ep + "/" + sq + "/3D/"
                tmpList = os.listdir(self.seqRootPath)     
                for t in self.taskList:
                    self.task_CB.addItem(t)
                    
        self.updateFN()

    def updateFN(self):
        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        sq = self.sequence_CB.currentText()
        tk = self.task_CB.currentText()
        nn = self.nn_LE.text()
        
        self.taskRootPath = self.seqRootPath + str(tk) + "/"
        
        if nn == "":
            self.sceneName = str(sq)+"_"+str(tk) + ".ma"
        else:
            if re.search("s[0-9][0-9][0-9][0-9]",nn):
                self.sceneName = str(sq)+"_"+str(nn)+ "_"+str(tk)+".ma"
            else:
                self.sceneName = str(sq)+"_"+str(tk)+"_"+str(nn) + ".ma"
        
        self.fn_LE.setText(self.sceneName)
        
    def saveScene(self):
        
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
            cmds.file( save=True, type='mayaAscii',force=True)
            
def dsSS():
    global myWindow
    myWindow = Window()
    myWindow.show()