import sys, re, os, shutil, subprocess, stat, webbrowser

if sys.platform == 'linux2':
    sys.path.append('/dsGlobal/globalMaya/Python/PyQt_Linx64')
    sys.path.append('/dsGlobal/dsCore/shotgun')
    sys.path.append('/dsGlobal/dsCore/maya/dsCommon')
    sys.path.append('/dsGlobal/dsCore/maya/dsCheck')
    uiFile = '/dsGlobal/dsCore/maya/dsShotOpen/dsShotOpenUI.ui'

else:
    sys.path.append(r'\\vfx-data-server\dsGlobal\globalMaya\Python\PyQt_Win64')
    sys.path.append(r'\\vfx-data-server\dsGlobal\dsCore\shotgun')
    sys.path.append(r'\\vfx-data-server\dsGlobal\dsCore\maya')
    sys.path.append(r'\\vfx-data-server\dsGlobal\dsCore\maya\dsCheck')
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsShotOpen/dsShotOpenUI.ui'
    
import dsCommon.dsMetaDataTools as dsMDT
import dsSQLTools as dsSQL
import sgTools
import dsVersionUp   
import dsCommon.dsOsUtil as dsOsUtil;reload(dsOsUtil)
import dsSaveScene;reload(dsSaveScene)

if dsOsUtil.mayaRunning() == True:
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
        
        self.setObjectName( 'dsShotOpener' )
        self.taskList = ['blocking','anim','light','effect','template']
        
        self.home = 'C:%s' % os.getenv("HOMEPATH")
        self.config_dir = '%s/.shotOpen' % (self.home)
        self.config_dir = self.config_dir.replace("/","\\")
        self.config_path = '%s/config.ini' % (self.config_dir)
        self.config_path = self.config_path.replace("/","\\")
        self.dsPipe = "//vfx-data-server/dsPipe"
        self.emptyMA = '//vfx-data-server/dsGlobal/globalMaya/Resources/emptyScene.ma'

        self.taskRootPath = ""
        self.init_GUI()
        self.init_user()
        self.init_projects()

        self.projects_CB.currentIndexChanged.connect(self.init_episodes)
        self.episodes_CB.currentIndexChanged.connect(self.init_sequences)
        self.sequence_CB.currentIndexChanged.connect(self.init_tasks)
        self.sequence_CB.currentIndexChanged.connect(self.init_shots)
        self.task_CB.currentIndexChanged.connect(self.init_scene)

        self.createEmpty_B.clicked.connect(self.createEmpty)
        self.saveAs_B.clicked.connect(self.saveAs)
        self.ref_B.clicked.connect(self.refScene)
        self.import_B.clicked.connect(self.importScene)
        self.retire_B.clicked.connect(self.retireScene)
        self.versionUp_B.clicked.connect(self.versionAction)
        self.notate_B.clicked.connect(self.notateScene)
        self.explorer_B.clicked.connect(self.explorerOpen)
        self.sg_B.clicked.connect(self.sgWeb)
        
        self.scene_LW.itemDoubleClicked.connect(self.openScene)
        self.hero_RB.clicked.connect(self.init_scene)
        self.version_RB.clicked.connect(self.init_scene)
        
        self.scene_LW.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.scene_LW.customContextMenuRequested.connect(self.openMenu)
        
        self.connect(self.actionVfx_wiki_dk,QtCore.SIGNAL('triggered()'), lambda item=[]: self.webBrowser())

        self.load_config()

    def saveAs(self):
        print "save file as"
        dsSaveScene.dsSS()

    def init_GUI(self):
        self.hero_RB.setEnabled(False)
        self.version_RB.setEnabled(False)
    
    def init_user(self):

        self.myPeople = dsSQL.getValueDB("//vfx-data-server/dsGlobal/globalusers","Users","Status","act")
        
        ##Test and return if Episode exists
        self.user_CB.clear()
        self.userDict = {}

        for user in sorted(self.myPeople):
            userName = str(user[1])
            self.user_CB.addItem(userName)
            self.userDict['id'] = user[0]
            self.userDict['sg_initials'] = user[2]
        
        '''
        #Connecting Through Shotgun Web
        self.group = {'type': 'Group', 'id': 5}
        self.myPeople = sgTools.sgGetPeople()
        for user in sorted(self.myPeople):
            if str(user['sg_status_list']) == "act":
                userName = str(user['name'])
                self.user_CB.addItem(userName)
                self.userDict['id'] = user['id']
                self.userDict['sg_initials'] = user['sg_initials']
        '''
            
    def init_projects(self):
        '''
        Adds projects to self.projects
        Only if the project contains a /Local/config.xml
        '''
        self.projects_CB.clear()
        list = []
        
        tmpList = dsSQL.getValueDB("U:/globalProjects","Projects","Status",'Active')
        
        #ShotGun Connection
        #tmpList = sgTools.sgGetProjects()
        
        for t in tmpList:
            list.append(t[1])
        list.sort()
        for project in list:
            self.projects_CB.addItem(project)
        
    def init_episodes(self):
        '''
        Adds episodes to self.episodes
        '''
        #self.keepTask()
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
        #self.keepTask()
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
                self.taskRootPath = self.dsPipe + "/" + pr + "/film/" + ep + "/" + sq + "/3D/"
        
                tmpList = os.listdir(self.taskRootPath)
                self.task_CB.addItem("all")        
                for t in self.taskList:
                    self.task_CB.addItem(t)
                    
        self.loadTaskconfig()
            
    def init_scene(self):
        #self.loadTaskconfig()
        self.hero_RB.setEnabled(True)
        self.version_RB.setEnabled(True)
            
        if self.hero_RB.isChecked():
            view = "hero"
            self.sceneView(view)
        if self.version_RB.isChecked():
            view = "version"
            self.sceneView(view)
        
    def init_shots(self):
        self.init_vars()
        self.shots_LW.clear()
        
        
        
        #sg = sgTools.getSG()
        #['sg_scene.Scene.code','is', str(epiName)]"
        #sgShots = sg.find("Shot",[['project.Project.name','is',str(self.pr)],['sg_scene.Scene.code','is',str(self.ep)],['sg_sequence.Sequence.code','is',str(self.sq)]],['code','id','sg_cut_in','sg_cut_out','sg_mayain','sg_mayaout'])
        
        #for shot in sgShots:
            #self.shots_LW.addItem(str(shot['code']))

    def init_vars(self):
        self.pr = self.projects_CB.currentText()
        self.ep = self.episodes_CB.currentText()
        self.sq = self.sequence_CB.currentText()
        self.tk = self.task_CB.currentText()

    def sceneView(self,view):
        '''
        Adds tasks to self.task_CB
        '''
        
        self.scene_LW.clear()
        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        sq = self.sequence_CB.currentText()
        tk = self.task_CB.currentText()
        
        if tk != "all":
            if view == "hero":
                self.sceneRootPath = self.taskRootPath + tk
                tmpList = os.listdir(self.sceneRootPath)

                tmpList = self.getMA(tmpList)
                if len(tmpList) != 0:
                    for t in tmpList:
                        self.scene_LW.addItem(t)
                
            if view == "version":
                self.sceneRootPath = self.taskRootPath + tk + "/version"
                if os.path.isdir(self.sceneRootPath):
                    tmpList = os.listdir(self.sceneRootPath)
                    
                    for t in tmpList:
                        if t[0] != ".":
                            vList = os.listdir(self.sceneRootPath + "/" + t)
                            for v in vList:
                                if re.search(".ma",v) or re.search(".mb",v):
                                    self.scene_LW.addItem(v)
        if tk == "all":
            if view == "hero":
                for tk in self.taskList:
                    try:
                        self.sceneRootPath = self.taskRootPath + tk
                        tmpList = os.listdir(self.sceneRootPath)
                        
                        tmpList = self.getMA(tmpList)
                        if len(tmpList) != 0:
                            self.scene_LW.addItem("------"+str(tk)+"------")
                            for t in tmpList:
                                self.scene_LW.addItem(t)
                    except:
                        pass
                    
            if view == "version":
                for tk in self.taskList:
                    self.sceneRootPath = self.taskRootPath + tk + "/version"
                    if os.path.isdir(self.sceneRootPath):
                        tmpList = os.listdir(self.sceneRootPath)
                        
                        tmpList = self.getMA(tmpList)
                        
                        if len(tmpList) != 0:
                            self.scene_LW.addItem("------"+str(tk)+"------")
                            for t in tmpList:
                                if t[0] != ".":
                                    vList = os.listdir(self.sceneRootPath + "/" + t)
                                    for v in vList:
                                        if re.search(".ma",v) or re.search(".mb",v):
                                            self.scene_LW.addItem(v)

    def checkScene(self,path):
        sceneList = []
        tmpList = os.listdir(path)
        for t in tmpList:
            if str(t) != ".mayaSwatches":
                if re.search(".ma",t) or re.search(".mb",t):
                    sceneList.append(t)

        return sceneList

    def getMA(self,tmpList):
        newList = []
        for t in tmpList:
            if t[0] != ".":
                if re.search(".ma",t) or re.search(".mb",t):
                    newList.append(t)
        return newList

    def createEmptyFrom(self,menu,item):

        tk = self.task_CB.currentText()
        sq = self.sequence_CB.currentText()
        selectedItem = self.scene_LW.currentItem()

        ext = item[-3:]
        #ext = selectedItem.text()[-3:]
        
        destFile = self.taskRootPath + tk + "/" + sq + "_" + tk + ext
        templateFile = self.taskRootPath +menu.title() + "/" + item
            
        if selectedItem != None:
            ext = selectedItem.text()[-3:]
            fileName = selectedItem.text().replace(ext,"")
        else:
            ext = item[-3:]
            fileName = item.replace(ext,"")
        
        if not os.path.isfile(destFile):
            shutil.copy(templateFile,destFile)
        else:
            print "hero file exists please notate"
            nn = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Add notation for Maya Scene File:')

            if str(nn[0]) != "":
                preName = sq + "_" + str(tk)
        
                if re.search("s[0-9][0-9][0-9][0-9]",fileName):
                    sName = re.search("s[0-9][0-9][0-9][0-9]",fileName)
                    sName = sName.group()
                    
                    if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                        nsName = re.search("s[0-9][0-9][0-9][0-9]",str(nn[0]))
                        nsName = nsName.group()
                        preName = fileName.replace(sName,nsName)
                    
                    else:
                        preName = sq + "_" + sName + "_" + str(tk)
                
                """ notate shot to name of workfile"""
                if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                    preName = sq + "_" + str(nn[0]) + "_" + tk
                    notatedName = preName
                else:
                    notatedName = preName + "_" + str(nn[0])
        
                if self.testNotation(notatedName):
                    destFile = destFile.replace(fileName,notatedName)
                    print "create " + destFile
                    shutil.copy(templateFile,destFile)         

        self.init_scene()

    def sgWeb(self):
        pr = str(self.projects_CB.currentText())
        ep = str(self.episodes_CB.currentText())
        sq = str(self.sequence_CB.currentText())
        tk = str(self.task_CB.currentText())
        val = "sq"
        
        url = sgTools.sgGetPage(pr,ep,sq,val)
        new = 2 # open in a new tab, if possible
        webbrowser.open(url,new=new)
    
    def openScene(self):
        self.init_vars()
        selectedItem = self.scene_LW.currentItem()
        print selectedItem.text()
        if selectedItem.text()[0] != "-":
            if self.tk == "all":
                for task in self.taskList:
                    if re.search(task,selectedItem.text()):
                        self.tk = task
                        break
    
            if self.hero_RB.isChecked():
                mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
                
            if self.version_RB.isChecked():
                tmpSplit = selectedItem.text().split("_")
                ext = selectedItem.text()[-3:]
                heroScene = tmpSplit[0] + "_" + tmpSplit[1] + ext
                mayaScene = self.taskRootPath + self.tk + "/version/" + heroScene +"/"+ selectedItem.text()
    
            if dsOsUtil.mayaRunning() == True:
                if cmds.file(q=True, anyModified=True) == True:
                    self.saveConfirmDialog(mayaScene)
                else:
                    cmds.file( str(mayaScene), o=True )
            else:
                os.environ['PYTHONPATH']="//vfx-data-server/dsGlobal/dsCore\maya;//vfx-data-server/dsGlobal/globalMaya/Resources/PyQt_Win64;//vfx-data-server/dsGlobal/globalResources/Shotgun;//vfx-data-server/dsGlobal/dsCore/shotgun"
                os.environ['MAYA_SCRIPT_PATH'] = "//vfx-data-server/dsGlobal/globalMaya/Mel"
                os.environ['MAYA_ICON_PATH'] = "//vfx-data-server/dsGlobal/globalMaya/Icons"
                os.environ['MAYA_SHELF_PATH'] = "//vfx-data-server/dsGlobal/globalMaya/shelves"
                os.environ['MAYA_MODULE_PATH'] = "//vfx-data-server/dsGlobal/globalMaya/modules/windows/2013/"
                os.environ['YETI_INTERACTIVE_LICENSE'] = "1"
                os.environ['RLM_LICENSE '] = "49534@xserv2.duckling.dk"
                
                print "open new Maya with Scene " + mayaScene
                cmd = '"C:/Program Files/Autodesk/Maya2013/bin/maya.exe\" -file ' + str(mayaScene)
                if sys.platform == "linux2":
                    self.process(cmd)
                else:
                    proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,)
        
        try:
            dsMDT.testMDNode()
            dsMDT.sceneCheck()
        except:
            pass
            
    def importScene(self):
        self.init_vars()
        
        selectedItem = self.scene_LW.currentItem()
        
        if self.tk == "all":
            for task in self.taskList:
                if re.search(task,selectedItem.text()):
                    self.tk = task
                    break


        mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
        if dsOsUtil.mayaRunning() == True:
            print "import " +  mayaScene
            cmds.file(str(mayaScene), i=True)
        
    def retireScene(self):
        self.init_vars()

        selectedItem = self.scene_LW.currentItem()
        
        if self.tk == "all":
            for task in self.taskList:
                if re.search(task,selectedItem.text()):
                    self.tk = task
                    break

        historyPath = self.taskRootPath + self.tk + "/_history"
        if not os.path.isdir(historyPath):os.mkdir(historyPath)
        
        mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
        self.versionAction()
        
        shutil.copy(mayaScene,historyPath + "/" + selectedItem.text())
        os.remove(str(mayaScene))
        print "retired " + mayaScene
            
        self.init_scene()

    def explorerOpen(self):
        self.init_vars()
        
        selectedItem = self.scene_LW.currentItem()
            
        if selectedItem is not "":
            path = self.taskRootPath + self.tk + "/"
        else:
            path = self.taskRootPath
            
        if self.tk == "all":
            path = self.taskRootPath
            
        dsOsUtil.openInBrowser(path)
    
    def refScene(self):
        self.init_vars()

        selectedItem = self.scene_LW.currentItem()
        
        if self.tk == "all":
            for task in self.taskList:
                if re.search(task,selectedItem.text()):
                    self.tk = task
                    break
                
        ext = selectedItem.text()[-3:]
        nsName = selectedItem.text().replace(ext,"")
        mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
        if dsOsUtil.mayaRunning() == True:
            print "Ref " +mayaScene
            cmds.file(str(mayaScene), r=True, namespace=str(nsName), options="v=0", shd="shadingNetworks")

    def versionAction(self):
        self.init_vars()
        
        selectedItem = self.scene_LW.currentItem()
        
        if selectedItem is not None:
            
            mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
    
            if self.hero_RB.isChecked():
                mayaScene = self.taskRootPath + self.tk + "/" + selectedItem.text()
                
            if self.version_RB.isChecked():
                tmpSplit = selectedItem.text().split("_")
                ext = selectedItem.text()[-3:]
                heroScene = tmpSplit[0] + "_" + tmpSplit[1] + ext
                mayaScene = self.taskRootPath + self.tk + "/version/" + heroScene +"/"+ selectedItem.text()
    
    
            if dsOsUtil.mayaRunning() == True:
                if str(mayaScene) ==str(cmds.file(q=True,sn=True)):
                    dsVersionUp.dsVersionUp()
                else:
                    nn = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Add Descrition:')
                    description = str(nn[0])
    
                    if description != "":
                        """ dsVersionUp """
                        filePath = str(mayaScene)
                        sgTask = self.tk
                
                        self.pathDict = sgTools.sgShotPathParce(filePath)
                        self.check = self.checkLocalVersion(filePath,self.pathDict)
                        
                        thumbPath = sgTools.sgThumbnail(filePath,self.check,False)
                        
                        sg = sgTools.getSG()
                        """ test if task is connected to seq or shot """
                        
                        taskOBJ = sg.find_one('Task',[['project.Project.name','is',str(self.pr)],['entity.Sequence.code','is',str(self.sq)],['step.Step.code','is',str(self.tk)]],['content','id','entity'])
                        val = "seq"
                        if taskOBJ == None:
                            if re.search("s[0-9][0-9][0-9][0-9]",selectedItem.text()):
                                sName = re.search("s[0-9][0-9][0-9][0-9]",selectedItem.text())
                                sName = sName.group()    
                            else:
                                sgShots = sg.find("Shot",[['project.Project.name','is',str(self.pr)],['sg_sequence.Sequence.code','is',str(self.sq)]],['code','id'])
                                sName = sgShots[1]['code']

                            val = "shot"
                            taskOBJ = sg.find_one('Task',[['project.Project.name','is',str(self.pr)],['entity.Shot.sg_sequence.Sequence.code','is',str(self.sq)],['entity.Shot.code','is',str(sName)],['step.Step.code','is',str(self.tk)]],['content','id','entity'])
                        
                        try:
                            self.sgTaskID = taskOBJ['id']
                        except:
                            print "no task for this shot or sequence"
                            self.sgTaskID = "none"
                             
                        self.versionUp(filePath,self.check,False)
                                
                        self.versionUp(filePath,self.check,True)
                        self.path_version_file = self.path_version_file.replace(self.pathDict['dsRelative'] + "/","")
                            
                        heroName = self.pathDict['fileName']
                            
                        self.proj = sgTools.sgGetProject(str(self.pr),[])
                        self.epiObj = sgTools.sgGetEpisode(str(self.ep),str(self.pr),[])
                        self.seqObj = sgTools.sgGetSequence(str(self.sq),str(self.pr),str(self.ep),[])
                        self.taskObj = sgTools.sgGetObjbyID("Task",int(self.sgTaskID),[])
                             
                        if val == "seq":
                            data = {'code':self.version_file_name,'project':self.proj,'user':self.currentUser,'sg_task':self.taskObj,'sg_file_name':heroName,'sg_path':self.path_version_file,'description':description,'sg_version_file_name':self.version_file_name,'entity':self.seqObj}
                           
                        if val == "shot":
                            self.shotObj = sgTools.sgGetShot(sg,str(sName),str(self.sq),str(self.pr),str(self.ep),[])
                            data = {'code':self.version_file_name,'project':self.proj,'user':self.currentUser,'sg_task':self.taskObj,'sg_file_name':heroName,'sg_path':self.path_version_file,'description':description,'sg_version_file_name':self.version_file_name,'entity':self.shotObj}
                       
                        result = sgTools.sgCreateObj('Version',data)
                        print "created " + self.version_file_name + " in shotGun"
                
                        self.init_scene()
                    else:
                        print "please select maya scene too versionUP"
            
    def versionUp(self,filePath,version,val):
        
        if not re.search("/version/",filePath):
            filePathList = filePath.split("/")
            versionPath = filePath.replace(filePathList[-1],"version")
            versionPath = versionPath + "/" + filePathList[-1]
            if not os.path.isdir(versionPath):
                os.makedirs(versionPath)
                
            self.myPeople = sgTools.sgGetPeople()
                
            duckUser = self.user_CB.currentText()
            for user in self.myPeople:           
                if str(duckUser) == user['name']:
                    self.currentUser = user
                    self.duckInitials = user['sg_initials']
                    break
                
            self.version_file_name = filePathList[-1].replace(".ma","_" + version + "_" + self.duckInitials +  ".ma")
            self.path_version_file = versionPath + "/" + self.version_file_name
            
            if val == True:
                shutil.copy(filePath,versionPath + "/" + self.version_file_name)
                print "versioned UP"
                self.filePermissions(versionPath + "/" + self.version_file_name)
         
    def VersionToHero(self):
        print "versionToHero"
        self.init_vars()
        selectedItem = self.scene_LW.currentItem()
        ext = selectedItem.text()[-3:]
        
        fileSplit = selectedItem.text().split("_")
        ver_user = "_" +fileSplit[-2] +  "_" + fileSplit[-1] 
        
        versionFilePath = str(self.taskRootPath+self.tk + "/version/"+selectedItem.text())
        
        heroFileName = selectedItem.text().replace(ver_user,"")
        heroFilePath = str(self.taskRootPath + self.tk + "/" + heroFileName + ext)
        mayaScene = heroFilePath
        
        if dsOsUtil.mayaRunning() == True:
            if str(mayaScene) ==str(cmds.file(q=True,sn=True)):
                dsVersionUp.dsVersionUp()
            else:
                nn = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Add Descrition:')
                description = str(nn[0])

                if description != "":
                    """ dsVersionUp """
                    filePath = str(mayaScene)
                    sgTask = self.tk
            
                    self.pathDict = sgTools.sgShotPathParce(filePath)
                    self.check = self.checkLocalVersion(filePath,self.pathDict)
                    
                    thumbPath = sgTools.sgThumbnail(filePath,self.check,False)
                    
                    sg = sgTools.getSG()
                    """ test if task is connected to seq or shot """
                    
                    taskOBJ = sg.find_one('Task',[['project.Project.name','is',str(self.pr)],['entity.Sequence.code','is',str(self.sq)],['step.Step.code','is',str(self.tk)]],['content','id','entity'])
                    val = "seq"
                    if taskOBJ == None:
                        if re.search("s[0-9][0-9][0-9][0-9]",selectedItem.text()):
                            sName = re.search("s[0-9][0-9][0-9][0-9]",selectedItem.text())
                            sName = sName.group()    
                        else:
                            sName = "s0010"
                            
                        val = "shot"
                        taskOBJ = sg.find_one('Task',[['project.Project.name','is',str(self.pr)],['entity.Shot.sg_sequence.Sequence.code','is',str(self.sq)],['entity.Shot.code','is',str(sName)],['step.Step.code','is',str(self.tk)]],['content','id','entity'])
    
                    self.sgTaskID = taskOBJ['id']
                    self.versionUp(filePath,self.check,False)
                            
                    self.versionUp(filePath,self.check,True)
                    self.path_version_file = self.path_version_file.replace(self.pathDict['dsRelative'] + "/","")
                        
                    heroName = self.pathDict['fileName']
                        
                    self.proj = sgTools.sgGetProject(str(self.pr),[])
                    self.epiObj = sgTools.sgGetEpisode(str(self.ep),str(self.pr),[])
                    self.seqObj = sgTools.sgGetSequence(str(self.sq),str(self.pr),str(self.ep),[])
                    self.taskObj = sgTools.sgGetObjbyID("Task",int(self.sgTaskID),[])
                         
                    if val == "seq":
                        data = {'code':self.version_file_name,'project':self.proj,'user':self.currentUser,'sg_task':self.taskObj,'sg_file_name':heroName,'sg_path':self.path_version_file,'description':description,'sg_version_file_name':self.version_file_name,'entity':self.seqObj}
                       
                    if val == "shot":
                        self.shotObj = sgTools.sgGetShot(sg,str(sName),str(self.sq),str(self.pr),str(self.ep),[])
                        data = {'code':self.version_file_name,'project':self.proj,'user':self.currentUser,'sg_task':self.taskObj,'sg_file_name':heroName,'sg_path':self.path_version_file,'description':description,'sg_version_file_name':self.version_file_name,'entity':self.shotObj}
                   
                    result = sgTools.sgCreateObj('Version',data)
                    print "created " + self.version_file_name + " in shotGun"
            
                    self.init_scene()
        
            shutil.copy(versionFilePath,heroFilePath)
            self.filePermissions(heroFilePath)
         
    def checkLocalVersion(self,filePath,pathDict):
        tmpList = []
        if re.search(".ma",filePath):
            dirPath = filePath.replace(self.pathDict['fileName'] + '.ma',"")
            self.fn = self.pathDict['fileName'] + '.ma'
        if re.search(".mb",filePath):
            dirPath = filePath.replace(self.pathDict['fileName'] + '.mb',"")
            self.fn = self.pathDict['fileName'] + '.mb'
        local = os.listdir(dirPath)
        
        if "version" in local:
            verPath = dirPath + "version/" + self.fn + "/"
            if os.path.isdir(verPath):
                verList = os.listdir(verPath)
                for ver in verList:
                    if re.search(str(pathDict['fileName']),ver):
                        tmpList.append(ver)
                nV = len(tmpList)  + 1
                ver = "v%03d" %nV
                return ver
            else:
                return "v001"
        else:
            return "v001"

    def testNotation(self,notatedName):
        val = True

        testSplit = notatedName.split("_")
        if len(testSplit) > 4:
            print "too long"
            val = False

        testSplit = notatedName.split(" ")
        if len(testSplit) > 1:
            print " has spaces"
            val = False

        return val

    def createEmpty(self):
        self.init_vars()

        heroFileName = str(self.sq+"_"+self.tk+".ma")
        heroFilePath = str(self.taskRootPath + self.tk + "/" + heroFileName)
        
        if self.tk != "all":
            if os.path.isfile(heroFilePath):
                print "hero file exists please notate"
                nn = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Add notation for Maya Scene File:')
                ext = ".ma"
                if str(nn[0]) != "":
                    preName = self.sq + "_" + str(self.tk)
            
                    if re.search("s[0-9][0-9][0-9][0-9]",heroFileName):
                        sName = re.search("s[0-9][0-9][0-9][0-9]",heroFileName)
                        sName = sName.group()
                        
                        if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                            nsName = re.search("s[0-9][0-9][0-9][0-9]",str(nn[0]))
                            nsName = nsName.group()
                            preName = heroFileName.replace(sName,nsName)
                        
                        else:
                            preName = self.sq + "_" + sName + "_" + str(self.tk)
                    
                    """ notate shot to name of workfile"""
                    if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                        preName = self.sq + "_" + str(nn[0]) + "_" + self.tk
                        notatedName = preName + ext
                    else:
            
                        notatedName = preName + "_" + str(nn[0]) + ext
            
                    if self.testNotation(notatedName):
                        destFile = heroFilePath.replace(heroFileName,notatedName)
                        print "create " + destFile
                        shutil.copy(self.emptyMA,destFile)
                        self.init_scene()
            else:
                print "creating new Hero file"
                shutil.copy(self.emptyMA,heroFilePath)
        else:
            print ""
        self.init_scene()

    def notateScene(self):
        self.init_vars()

        if self.tk != "all":
            
            nn = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Add notation for Maya Scene File:')
    
            if str(nn[0]) != "":

                selectedItem = self.scene_LW.currentItem()
    
                templateFile = str(self.taskRootPath + self.tk + "/" + selectedItem.text())
                ext = templateFile[-3:]
    
                fileName = selectedItem.text().replace(ext,"")
                
                preName = self.sq + "_" + str(self.tk)
                
                """ update new notation from one s0010 to s0020 and keep the current notation"""
                if re.search("s[0-9][0-9][0-9][0-9]",fileName):
                    sName = re.search("s[0-9][0-9][0-9][0-9]",fileName)
                    sName = sName.group()
                    
                    if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                        nsName = re.search("s[0-9][0-9][0-9][0-9]",str(nn[0]))
                        nsName = nsName.group()
                        preName = fileName.replace(sName,nsName)
                    
                    else:
                        preName = self.sq + "_" + sName + "_" + str(self.tk)
                
                
                """ notate shot to name of workfile"""
                if re.search("s[0-9][0-9][0-9][0-9]",str(nn[0])):
                    preName = self.sq + "_" + str(nn[0]) + "_" + self.tk
                    notatedName = preName + ext
                else:
    
                    notatedName = preName + "_" + str(nn[0]) + ext
    
                if self.testNotation(notatedName):
                    destFile = templateFile.replace(selectedItem.text(),notatedName)
                    print "Notated " + destFile
                    shutil.copy(templateFile,destFile)
                    self.init_scene()

    def saveConfirmDialog(self, item):
        reply = QtGui.QMessageBox.question(self, 'Message', "Want to to Save, before closing?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        
        #print str(item)
        if reply == QtGui.QMessageBox.Yes:
            cmds.file(save=True, type='mayaAscii' )
            cmds.file(str(item), o=True, f=True)
        elif reply == QtGui.QMessageBox.No:
            cmds.file(str(item), o=True, f=True)

    def filePermissions(self,myFile):
        fileAtt = os.stat(myFile)[0]
        if (not fileAtt & stat.S_IWRITE):
           # File is read-only, so make it writeable
           os.chmod(myFile, stat.S_IWRITE)
        else:
           # File is writeable, so make it read-only
           os.chmod(myFile, stat.S_IREAD)

    def webBrowser(self):
        new = 2 # open in a new tab, if possible
        # open a public URL, in this case, the webbrowser docs
        url = "http://vfx.duckling.dk/?page_id=1471"
        webbrowser.open(url,new=new)

    def openMenu(self, position):
        self.save_config()

        tk = self.task_CB.currentText()
        selectedItem = self.scene_LW.currentItem()

        menu = QtGui.QMenu()
        createMenu = QtGui.QMenu("CreateFromTask")
        mainMenu = QtGui.QMenu("main")

        """ task Menu's"""
        blockingMenu = QtGui.QMenu("blocking")
        animMenu = QtGui.QMenu("anim")
        lightMenu = QtGui.QMenu("light")
        effectMenu = QtGui.QMenu("effect")
        templateMenu = QtGui.QMenu("template")

        """ Menu creation"""
        menu.addMenu(mainMenu)

        if self.hero_RB.isChecked():
            if not selectedItem is None:
                openTask = mainMenu.addAction("open")
                self.connect(openTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.openScene())
    
                importTask = mainMenu.addAction("import")
                self.connect(importTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.importScene())
    
                refTask = mainMenu.addAction("reference")
                self.connect(refTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.refScene())
    
                retireTask = mainMenu.addAction("retire")
                self.connect(retireTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.retireScene())
    
                versionTask = mainMenu.addAction("versionUp")
                self.connect(versionTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.versionAction())
    
                notateTask = mainMenu.addAction("notateScene")
                self.connect(notateTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.notateScene())
    
            else:
                menu.addMenu(createMenu)
                createTask = mainMenu.addAction("create empty scene")
                self.connect(createTask,QtCore.SIGNAL('triggered()'), lambda item=[]: self.createEmpty())
                
                        
                if len(self.checkScene(self.taskRootPath + "blocking")) != 0:
                    createMenu.addMenu(blockingMenu)
                    for item in self.checkScene(self.taskRootPath + "blocking"):
                        sceneName = blockingMenu.addAction(item)
                        self.connect(sceneName,QtCore.SIGNAL('triggered()'), lambda item=item: self.createEmptyFrom(blockingMenu,item))
    
                if len(self.checkScene(self.taskRootPath + "anim")) != 0:
                    createMenu.addMenu(animMenu)
                    for item in self.checkScene(self.taskRootPath + "anim"):
                        sceneName = animMenu.addAction(item)
                        self.connect(sceneName,QtCore.SIGNAL('triggered()'), lambda item=item: self.createEmptyFrom(animMenu,item))
    
                if len(self.checkScene(self.taskRootPath + "light")) != 0:
                    createMenu.addMenu(lightMenu)
                    for item in self.checkScene(self.taskRootPath + "light"):
                        sceneName = lightMenu.addAction(item)
                        self.connect(sceneName,QtCore.SIGNAL('triggered()'), lambda item=item: self.createEmptyFrom(lightMenu,item))
    
                if len(self.checkScene(self.taskRootPath + "effect")) != 0:
                    createMenu.addMenu(effectMenu)
                    for item in self.checkScene(self.taskRootPath + "effect"):
                        sceneName = effectMenu.addAction(item)
                        self.connect(sceneName,QtCore.SIGNAL('triggered()'), lambda item=item: self.createEmptyFrom(effectMenu,item))
    
                if len(self.checkScene(self.taskRootPath + "template")) != 0:
                    createMenu.addMenu(templateMenu)
                    for item in self.checkScene(self.taskRootPath + "template"):
                        sceneName = templateMenu.addAction(item)
                        self.connect(sceneName,QtCore.SIGNAL('triggered()'), lambda item=item: self.createEmptyFrom(templateMenu,item))
                        
            menu.exec_(QtGui.QCursor.pos())
            #action = menu.exec_(self.scene_LW.mapToGlobal(position))

        if self.version_RB.isChecked():

            createTask = mainMenu.addAction("Version up to Hero")
            self.connect(createTask,QtCore.SIGNAL('triggered()'), lambda item=selectedItem: self.VersionToHero())
                
            menu.exec_(QtGui.QCursor.pos())

    def closeEvent(self,event):
        self.save_config()

    def loadTaskconfig(self):
        '''
        Load config which is a dictionary and applying setting.
        '''
        if os.path.exists(self.config_path):
            config_file = open( '%s' % self.config_path, 'r')
            list = config_file.readlines()
            config_file.close()

            config = {}
            for option in list:
                key, value = option.split('=')
                config[key] = value.strip()
            
            for i in range(self.task_CB.count()):
                if str(self.task_CB.itemText(i)) == str(config.get('TASK')):
                    self.task_CB.setCurrentIndex(i)
                
    def load_config(self):
        '''
        Load config which is a dictionary and applying setting.
        '''
        if os.path.exists(self.config_path):
            config_file = open( '%s' % self.config_path, 'r')
            list = config_file.readlines()
            config_file.close()

            config = {}
            for option in list:
                key, value = option.split('=')
                config[key] = value.strip()

            try:
                index = [i for i in range(self.user_CB.count()) if self.user_CB.itemText(i) == config.get('USER')][0]
                self.user_CB.setCurrentIndex(index)

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

    def save_config(self):
        '''
        Save setting to the config file as a dictionary.
        '''

        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        us = self.user_CB.currentText()
        pr = self.projects_CB.currentText()
        ep = self.episodes_CB.currentText()
        sq = self.sequence_CB.currentText()
        tk = self.task_CB.currentText()

        config = open( '%s' % self.config_path, 'w')
        config.write('USER=%s\n' % (us))
        config.write('PROJECT=%s\n' % (pr))
        config.write('EPISODE=%s\n' % (ep))
        config.write('SEQUENCE=%s\n' % (sq))
        config.write('TASK=%s\n' % (tk))
        config.close()

        return self.config_path

    def process( self, cmd_line):
        '''
        Subprocessing, Returning the process.
        '''
        cmd = cmd_line.split(' ')
        proc = subprocess.Popen(cmd,
                            shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
        return proc


        
def dsShotOpen():
    global myWindow
    myWindow = Window()
    myWindow.show()