#import os, sip, re, sys, shutil, subprocess
print 'v1.0.6,', 

"""
v1.0.6
-------------------
 - Added min and max Sequence divide to the gui, and to the config.
 - And to the rrSubmitter command line.

v1.0.5
-------------------
 - Fixed self.getLastestVersion to check publish3D versions instead
 - Added self.mayaSave to self.submitRR
 - change self.getRenderScene to check for renderVersion inside
 the publish3D folder on dsPipe. 

"""

import sys
import sip
import re
import os
import shutil
import subprocess
from PyQt4 import QtGui, QtCore, uic
import dsError
reload(dsError)

try:
    import maya.cmds as cmds
    import maya.OpenMayaUI as mui
except:
    pass

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsSubmit/dsSubmit.ui'
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsSubmit/dsSubmit.ui'
 
form_class, base_class = uic.loadUiType(uiFile)

class Window(base_class, form_class):
    '''GI ONLY WORKS ON ASCII AND NOT MAYA BINARY'''
    def __init__(self, parent=getMayaWindow()):
        '''A custom window with a demo set of ui widgets'''
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        
        self.dsError = dsError.dsErrorUI()
        self.refresh()
        
        if sys.platform == "linux2":
            self.home = os.getenv("HOME")
            self.dsPipe = '/dsPipe'
            self.dsComp = '/dsComp'
            self.dsGlobal = '/dsGlobal'
            self.config_dir = '%s/.submit' % (self.home)
            self.config_path = '%s/config.ini' % (self.config_dir)
            
        elif sys.platform == 'win32':
            self.home = 'C:%s' % os.getenv("HOMEPATH")
            self.dsPipe = '//vfx-data-server/dsPipe'
            self.dsComp = '//xserv2.duckling.dk/dsComp'
            self.dsGlobal = '//vfx-data-server/dsGlobal'
            self.config_dir = '%s/.submit' % (self.home)
            self.config_path = '%s/config.ini' % (self.config_dir)
            
        self.template = '%s/dsCore/maya/dsSubmit/RR_template.xml' % (self.dsGlobal)

        self.filePath = cmds.file(q=True,l=True)[0]
        
        self.setGlobals()
        
        self.SubmitButton.clicked.connect(self.openPopup)
        self.closeButton.clicked.connect(self.closePopup)
        self.YesButton.clicked.connect(self.submitRR)
        
        self.rlRender = {}

        #self.actionGI_RL.triggered.connect(self.setupGICache)
        
        self.connect(self.actionWIKI,QtCore.SIGNAL('triggered()'), lambda item=[]: self.webBrowser())
        self.connect(self.actionExplorer,QtCore.SIGNAL('triggered()'), lambda item=[]: self.explorer())
        self.connect(self.actionrrControl,QtCore.SIGNAL('triggered()'), lambda item=[]: self.rrControl())
        
        print 'Loading config file from:', self.config_path
        self.load_config()

    def checkPath(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        
    def setupGICache(self):
        print "setupGI"
        #shotName = "%SHOTNAME%"
        RLList = cmds.ls(type="renderLayer")
        
        if "GI_RL" not in RLList:
            cmds.createRenderLayer( noRecurse=True, name='GI_RL',mc=True, g=True )
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.dontSaveImage")
            cmds.setAttr("vraySettings.dontSaveImage",1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.globopt_gi_dontRenderImage")
            cmds.setAttr("vraySettings.globopt_gi_dontRenderImage",1)
            cmds.editRenderLayerAdjustment( 'GI_RL', 'vraySettings.imap_mode')
            cmds.setAttr('vraySettings.imap_mode', 6)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.imap_dontDelete")
            cmds.setAttr("vraySettings.imap_dontDelete",1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.imap_autoSave")
            cmds.setAttr("vraySettings.imap_autoSave",1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.mode")
            cmds.setAttr("vraySettings.mode",0)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.relements_enableall")
            cmds.setAttr("vraySettings.relements_enableall",0)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.useCameraPath")
            cmds.setAttr("vraySettings.useCameraPath", 1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.imap_useCameraPath")
            cmds.setAttr("vraySettings.imap_useCameraPath", 1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.dontDelete")
            cmds.setAttr("vraySettings.dontDelete", 1)
            cmds.editRenderLayerAdjustment( 'GI_RL', "vraySettings.autoSave")
            cmds.setAttr("vraySettings.autoSave", 1)
      
            vrlmap = self.CachePath + '/' + self.dsShot + '_GICache.vrlmap'
            vrmap = self.CachePath + '/' + self.dsShot + '_GICache.vrmap'
            cmds.setAttr("vraySettings.autoSaveFile", vrlmap, type= "string")
            cmds.setAttr("vraySettings.imap_autoSaveFile", vrmap, type="string")
            self.refresh()
            
    def explorer(self):
        path = '%s/%s/film/%s/%s' % (self.dsPipe, self.project, self.episode, self.sequence)
        if os.path.isdir(path):
            if sys.platform == "linux2":
                cmd = "gnome-open " + str(path)
            if sys.platform == "win32":
                cmd = "explorer " + str(path.replace("/","\\"))
            self.process(cmd)
            
    def rrControl(self):
        if sys.platform == "linux2":
            cmd = '/mnt/rrender/lx__rrControl.sh'
        if sys.platform == "win32":
#             cmd = r"\\vfx-render-manager\royalrender\bin\win\rrControl.exe"
            cmd = r"\\vfx-render-server\royalrender\bin\win\rrControl.exe"
        self.process(cmd)
        
    def refreshRenderer(self):
        rl = str(self.rlList.currentItem().text())
        if self.rlRender.has_key(rl):
            self.renderBox.setCurrentIndex(self.rlRender[rl][0])
        
    def setGlobals(self):
        
        try:
            cmds.setAttr('dsMetaData.scriptType',2)
        except:
            pass
        
        project = '%s' % os.getenv('PROJECT')
        episode = '%s' % os.getenv('EPISODE')
        sequence = '%s' % os.getenv('SEQUENCE')
        shot = '%s' % os.getenv('SHOT')
        
        match = re.search('(?P<project>\w*)\/film\/(?P<episode>\w*)\/(?P<sequence>\w*)\/(?P<shot>\w*)', self.filePath)
        
        if match:
            match = match.groupdict()
            if project != 'None':
                self.project = project
            else:
                if match:
                    self.project = match['project']
    
            if episode != 'None':
                self.episode = episode
            else:
                if match:
                    self.episode = match['episode']
    
            if sequence != 'None':
                self.sequence = sequence
            else:
                if match: 
                    self.sequence = match['sequence']
    
            if shot != 'None':
                self.shot = shot
            else:
                if match: 
                    self.shot = match['shot']

    def refresh(self):
        self.shList.clear()
        self.rlList.clear()

        self.getShots()
        self.getRenderLayers()
        
    def getShots(self):
        list = []
        for shot in cmds.ls(type="shot"):
            if re.match("(s[0-9][0-9][0-9][0-9])",shot):
                self.shList.addItem(shot)
                list.append(shot)
            else:
                item = QtGui.QListWidgetItem(shot)
                item.setFlags(QtCore.Qt.NoItemFlags)
                self.shList.addItem(item)
                list.append(shot)
        if list:
            if not re.match("(s[0-9][0-9][0-9][0-9])",shot):
                for shot in list:
                    self.error('Shot: %s is not named correctly.' % shot)
                self.error('\nCouldnt find any shots with the correct name standard: s0000')
                self.error('Please make sure that you have named your shots correctly\n')
        
            """for i in range(self.shList.count()):
                item = self.shList.item(i)
                print str(item.flags())"""
        else:
            st = cmds.getAttr("defaultRenderGlobals.startFrame")
            et = cmds.getAttr("defaultRenderGlobals.endFrame")
            shot = cmds.shot('s0010', sst=st, set=et, cc='persp')
            self.shList.addItem('s0010')
            
    def getRenderLayers(self):
        ''' searches maya scene for all RenderLayers to update RListView'''
        for rl in cmds.ls(type='renderLayer'):
            if rl == "defaultRenderLayer":
                self.rlList.addItem("masterLayer")
            if 'RL' in rl and ':' not in rl:
                self.rlList.addItem(rl)
                
    def getSelected(self):
        shotList = self.shList.selectedItems()
        rlList = self.rlList.selectedItems()
        selDict = {}
        for shot in shotList:
            selDict[str(shot.text())] = [str(rl.text()) for rl in rlList]
        return selDict
    
    def mayaSave(self):
        try:
            save = cmds.file(save=True, force=True)
            print 'File saved: %s' % save
        except Exception as e:
            self.error('ERROR:%s' % e)
            print e.upper()
            
    def getGiSettings(self, vrlmap, vrmap, renderLayer):
        cmds.editRenderLayerGlobals( currentRenderLayer=renderLayer)
        cmds.setAttr("vraySettings.mode", 2)
        cmds.setAttr("vraySettings.imap_mode", 2)
        cmds.setAttr("vraySettings.autoSave", 0)
        cmds.setAttr("vraySettings.dontDelete", 0)
        cmds.setAttr("vraySettings.imap_dontDelete", 0)
        cmds.setAttr("vraySettings.autoSaveFile", vrlmap, type= "string")
        cmds.setAttr("vraySettings.imap_autoSaveFile", vrmap, type="string")
        cmds.setAttr("vraySettings.imap_fileName", vrlmap, type= "string")
        cmds.setAttr("vraySettings.fileName", vrmap, type="string")
        self.mayaSave()
        
    def setupGiRenderLayer(self, vrlmap, vrmap):        
        cmds.setAttr("vraySettings.autoSaveFile", vrlmap, type= "string")
        cmds.setAttr("vraySettings.imap_autoSaveFile", vrmap, type="string")
        cmds.setAttr("vraySettings.imap_fileName", vrlmap, type= "string")
        cmds.setAttr("vraySettings.fileName", vrmap, type="string")
        
        xrez = int(cmds.getAttr("defaultResolution.width"))
        yrez = int(cmds.getAttr("defaultResolution.height"))
        
        cmds.setAttr("vraySettings.width", xrez/2)
        cmds.setAttr("vraySettings.height",yrez/2)
        cmds.setAttr("defaultResolution.width", xrez/2)
        cmds.setAttr("defaultResolution.height",yrez/2)
        self.mayaSave()

        cmds.setAttr("vraySettings.width", xrez)
        cmds.setAttr("vraySettings.height",yrez)
        cmds.setAttr("defaultResolution.width", xrez)
        cmds.setAttr("defaultResolution.height",yrez)
        
    def checkVersion(self, path):
        '''
        Checks the path if there is any directories matching the pattern [vV]\d\d\d
        then adds it to a list and then it check which is the lastest and return it +1
        '''
        if os.path.exists(path):
            bool = True
            list = []
            for dir in os.listdir(path):
                match = re.search('([vV]\d\d\d)', dir)
                if match:
                    list.append(match.groups()[0].strip('v'))
            if list:
                list.sort()
                return 'v%03d' % (int(max(list)) + 1)
            else:
                return 'v001'
        else:
            return 'v001'
            
    def getLastestVersion(self, path, shot, renderLayer):
        '''Tries to match a string to the version format'''
        #path = self.getPublishPath(dir, shot, renderLayer)
        self.checkPath(path)
        
        versionList = [re.search('[v](\d+)', f).group() for f in os.listdir(path) if os.path.isdir('%s/%s' % (path, f))]
        
        if versionList:
            newVersion = 'v%03d' % (1 + int(max(versionList).strip('v')))
        else:
            newVersion = 'v001'
        return newVersion
    
    def getPublishPath(self, shot, renderLayer):
        '''
        Goes to dsPipe, right now...
        \dsComp\comDev\film\bottleShade\q0010\s0010\comp\published3D\beauty\v001
        '''
        dir = '%s/%s/film/%s/%s' % (self.dsComp, self.project, self.episode, self.sequence)
        return '%s/%s/comp/published3D/%s' % ( dir, shot, renderLayer.rstrip('_RL'))

    def getRenderScene(self, shot, renderLayer):
        publishPath = self.getPublishPath(shot, renderLayer)
        
        dir =  '%s/%s/film/%s/%s/renderFiles' % (self.dsPipe, self.project, self.episode, self.sequence)
        file = '%s_%s' % (shot, renderLayer)
        
        self.checkPath(dir)
        # get version from the publish folder
        version = self.getLastestVersion(publishPath, shot, renderLayer)
        
        extension = os.path.splitext(self.filePath)[1]
        
        return dir, file, version, extension
    
    def getImageDir(self, shot):
        dir = '%s/%s/film/%s/%s/%s/rawRender' % (self.dsPipe, self.project, self.episode, self.sequence, shot)
        return dir
    
    def getDuration(self, shot):
        return cmds.shot(shot, q=True, sst=True), cmds.shot(shot, q=True, set=True)
    
    def getRenderer(self, rl):
        #: If the user has specified any renderer for the renderlayer.
        if self.rlRender.has_key(rl):
            try:
                return self.rlRender[rl][1]
            except Exception as e:
                self.error('ERROR:%s' % e)
        #: else use the defaultRenderGlobal
        else:
            try:
                return cmds.getAttr('defaultRenderGlobals.currentRenderer')
            except Exception as e:
                self.error('ERROR:%s' % e)

    def getRenderCam(self, shot):
        camera = cmds.shot(shot, q=True,cc=True)
        if camera:
            return cmds.shot(shot, q=True,cc=True)
        else:
            self.error('No camera linked to %s' % shot)
            return 'perspShape'

    def deleteFrames(self, path):
        if self.DeleteFramesCheck.isChecked() and os.path.exists(path):
            for frame in os.listdir(path):
                print '\t', frame
                os.remove('%s/%s' % (path, frame))

    def renderOtherConfirmation(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you not want to render EXR's?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            return True
        elif reply == QtGui.QMessageBox.No:
            return False
        elif reply == QtGui.QMessageBox.Cancel:
            return False

    def extCheck(self,extension):
        if not re.search("exr",extension):
            return self.renderOtherConfirmation()
        else:
            return True

    def getExtension(self):
        renderer = cmds.getAttr("defaultRenderGlobals.ren")
        print renderer
        
        if renderer == "vray":
            extension = cmds.getAttr("vraySettings.imageFormatStr")
            if extension == "exr (multichannel)":
                extension = "exr"
        
        if renderer == "mentalRay":
            extension = cmds.getAttr("defaultRenderGlobals.imfkey")
        
        if renderer == "mayaSoftware" or renderer == "mayaHardware" or renderer == "mayaHardware2":
            extensionKey = cmds.getAttr("defaultRenderGlobals.imageFormat")
            extDict = {"6":"als","23":"avi","11":"cin","35":"dds","9":"eps","0":"gif","8":"jpg","7":"iff","10":"iff","31":"psd","36":"psd","32":"png","12":"yuv","2":"rla","5":"sgi","13":"sgi","1":"pic","19":"tga","3":"tif","4":"tif","20":"bmsp","63":"tim"}
            extension = extDict[str(extensionKey)]
            
        return extension

    def submitRR(self):
        self.closePopup()
        selection = self.getSelected()
        if self.ApproveCheck.isChecked():
            approve = "1"
        else:
            approve = "0"
        
        minSeq =str(int(self.minSeqDivInput.text()))
        maxSeq = str(int(self.maxSeqDivInput.text()))
        if self.saveFileCheck.isChecked():
            self.mayaSave()
        
        if self.UserText.text() == "":
            dsUserName = "administrator"
        else:
            dsUserName = self.UserText.text()
            
        extension = cmds.getAttr("vraySettings.imageFormatStr")        
        if self.extCheck(extension):
            for shot in selection.keys():    
                for rl in selection[shot]:
                    if len(selection.keys()) == 1:
                        startFrame = int(float(self.StartFrameInput.text()))
                        endFrame = int(float(self.EndFrameInput.text()))
                        rrFile = self.createRRFile(shot, rl, startFrame, endFrame)
                    else:
                        rrFile = self.createRRFile(shot, rl)
                    
                    if sys.platform == "linux2":
                        
                        command = '/mnt/rrender/bin/lx64/rrSubmitterconsole ' + str(rrFile) +' UserName=0~' + str(dsUserName)  + ' DefaulClientGroup=0~farm Priority=2~' + str(self.prio) + ' AutoApproveJob=1~' + approve + ' SeqDivMIN=0~' + minSeq + ' SeqDivMAX=0~' + maxSeq
                        
                        if os.path.exists(rrFile):
                            try:
                                self.process(command).communicate()[0]
                            except Exception as e:
                                self.error('ERROR:%s' % e)
                        else:
                            self.error('ERROR:%s doesnt exists...\n%s' % (rrFile, command))
                        
                    if sys.platform == "win32": 
                        command = '//vfx-render-server/royalrender/bin/win/rrSubmitterconsole.exe ' + str(rrFile) +' UserName=0~' + str(dsUserName)  + ' DefaulClientGroup=0~farm Priority=2~' + str(self.prio) + ' AutoApproveJob=1~' + approve + ' SeqDivMIN=0~' + minSeq + ' SeqDivMAX=0~' + maxSeq
                        #if os.path.exists('//vfx-render-manager/royalrender/bin/win/rrSubmitterconsole.exe'): print 'found rrSubmitterconsole'
                        if os.path.exists('//vfx-render-server/royalrender/bin/win/rrSubmitterconsole.exe'): 
                            print 'found rrSubmitterconsole'
                        else:
                            print 'couldnt find your rr submitter'
                        if os.path.exists(rrFile):
                            try:
                                self.process(command).communicate()[0]
                            except Exception as e:
                                self.error('ERROR:%s' % e)
                        else:
                            self.error('ERROR:%s doesnt exists...\n%s' % (rrFile, command))
            try:
                self.save_config()
            except Exception as e:
                self.error('ERROR:%s' % e)

    def createRRFile(self, shot, renderLayer, start=None, end=None, **kwargs):
        
        dir, file, version, fileExtension = self.getRenderScene(shot, renderLayer)
        renderScene = '%s/%s_%s%s' % (dir, file, version, fileExtension)
        renderXml = '%s/%s_%s.xml' % (dir, file, version)
        if not start and not end:
            start, end = self.getDuration(shot)
        renderer = self.getRenderer(renderLayer)
        imageDir = self.getImageDir(shot)
        renderCam = self.getRenderCam(shot)
        frameName = '%s_' % (renderLayer)

        extension = self.getExtension()

        minSeq = self.minSeqDivInput.text()
        maxSeq = self.maxSeqDivInput.text()
        
        dir = '%s/%s/film/%s/%s/%s/3D/data/GI_RL/' % (self.dsPipe, self.project, self.episode, self.sequence, shot)
        vrlmap = '%s%s_GICache.vrlmap' % (dir, shot)
        vrmap = '%s%s_GICache.vrmap' % (dir, shot)
        
        renderFolder = '%s/%s' % (imageDir, renderLayer)
        
        if renderLayer == 'GI_RL':
            self.setupGiRenderLayer(vrlmap, vrmap)
            renderer = 'vray_prepass'
            imageDir = dir
            frameName = '%s_GICache' % (shot)
            extension = "vrmap"
            renderFolder = imageDir
        else:
            if self.GICheck.isChecked():
                self.getGiSettings(vrlmap, vrmap, renderLayer)
                
        try:
            shutil.copy(self.filePath, renderScene)
        except Exception as e:
            self.error('\nERROR:%s.' % (e))
        
        template = open(self.template, 'r')
        rrFile = open(renderXml, 'w')
        
        if self.DeleteFramesCheck.isChecked() and os.path.exists(renderFolder):
            self.deleteFrames(renderFolder)
        
        for line in template:
                outline = line
                outline = outline.replace("%RENDERER%",renderer)
                outline = outline.replace("%SCENENAME%", renderScene)
                outline = outline.replace("%PROJECTNAME%", self.project)
                outline = outline.replace("%IMAGEDIR%", imageDir)
                outline = outline.replace("%RENDERCAM%", renderCam)
                outline = outline.replace("%RENDERLAYER%", renderLayer)
                outline = outline.replace("%START%", str(int(start)))
                outline = outline.replace("%END%", str(int(end)))
                outline = outline.replace("%EXTENSION%", extension)
                outline = outline.replace("%FRAMENAME%", frameName)
                outline = outline.replace("%USERNAME%", '')
                outline = outline.replace("%PRIORITY%", str(self.prio))
                outline = outline.replace("%SEQDIVMIN%", str(int(minSeq)))
                outline = outline.replace("%SEQDIVMAX%", str(int(maxSeq)))
                #outline = outline.replace("%APPROVE%", approve)
                rrFile.write(outline)
        template.close()
        rrFile.close()
        return renderXml

    def closePopup(self):
        #self.popupFrame.setGeometry(QtCore.QRect(590, 20, 171, 221))
        self.popupFrame.setGeometry(QtCore.QRect(600, 20, 171, 221))
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 591, 251))
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 250, 452, 32))    
        self.prio = self.priotyCombo.currentText()
        
    def setPopup(self):
        self.CamPopupCombo.clear()
        row = self.shList.currentRow()
        data = self.shList.item(row)
        shot = data.text()
        self.priotyCombo.setCurrentIndex(0)
        shotNew = shot.split("_")
        sName = str(shotNew[0])
        startVal = cmds.shot(sName, q=True, st=True)
        endVal = cmds.shot(sName, q=True, et=True)
        self.StartFrameInput.setText(str(startVal))
        self.EndFrameInput.setText(str(endVal))
        camShot = cmds.shot(sName,q=True,cc=True)
        self.CamPopupCombo.addItem(camShot)
        
        
        self.renderer_LE.setText(str(cmds.getAttr("defaultRenderGlobals.ren")))
        self.frameExt_LE.setText(str(self.getExtension()))

        camList = cmds.ls(type="camera")
        for cam in camList:
            if not cam == camShot and cam not in ['frontShape', 'sideShape', 'perspShape', 'topShape']:
                self.CamPopupCombo.addItem(cam)
                 
    def error(self, string):
        self.dsError.set(string)
        self.dsError.show()
        print string

    def openPopup(self):
        self.setPopup()

        shotList = self.shList.selectedItems()
        if len(shotList) >= 1:
            self.popupFrame.setGeometry(QtCore.QRect(0, 0, 241, 251))
            self.scrollArea.setGeometry(QtCore.QRect(-600, 5, 571, 241))
            self.scrollArea_2.setGeometry(QtCore.QRect(10, 300, 452, 32))
        if len(shotList) >= 2:
            self.CamPopupCombo.setEnabled(0)
            self.StartFrameInput.setEnabled(0)
            self.EndFrameInput.setEnabled(0)
        else:
            self.CamPopupCombo.setEnabled(1)
            self.StartFrameInput.setEnabled(1)
            self.EndFrameInput.setEnabled(1)
        
    def initalizeShots(self):
        for shot in self.shotNodeList:
            if re.match("(S[0-9][0-9][0-9][0-9])",shot):
                if not os.path.isdir(self.seqPath + "/" + shot): 
                    dsFolderStruct.dsCreateFs("SHOT",self.seqPath + "/",shot)

    def webBrowser(self):
        new = 2 # open in a new tab, if possible
        # open a public URL, in this case, the webbrowser docs
        url = "http://vfx.duckling.dk/?page_id=924"
        webbrowser.open(url,new=new)

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
                
            #print config
            
            if config.has_key('SHOT'):
                items = [self.shList.item(i) for i in range(self.shList.count()) if str(self.shList.item(i).text()) in config.get('SHOT')]
                
                for item in items:
                    item.setSelected(True) 
                    self.shList.setCurrentItem(item)
                
            if config.has_key('RENDERLAYER'):
                items = [self.rlList.item(i) for i in range(self.rlList.count()) if str(self.rlList.item(i).text()) in config.get('RENDERLAYER')]
                for item in items: 
                    item.setSelected(True)
                    self.rlList.setCurrentItem(item)
            
            if config.has_key('USERNAME'): self.UserText.setText(str(config.get('USERNAME')))
            if config.has_key('MINSEQDIV'): self.minSeqDivInput.setText(str(config.get('MINSEQDIV')))
            if config.has_key('MAXSEQDIV'): self.maxSeqDivInput.setText(str(config.get('MAXSEQDIV')))
            
            if config.has_key('SAVEFILE'): 
                self.saveFileCheck.setChecked(int(config.get('SAVEFILE')))
            
            if config.has_key('DELETEFRAMES'): self.DeleteFramesCheck.setChecked(int(config.get('DELETEFRAMES')))
            
            #if config.has_key('APPROVE'): self.ApproveCheck.setChecked(int(config.get('APPROVE')))

            if config.has_key('USEGI'): self.GICheck.setChecked(int(config.get('USEGI')))
            
            if config.has_key('PRIOTY'):
                index = [i for i in range(self.priotyCombo.count()) if self.priotyCombo.itemText(i) == config.get('PRIOTY')][0]
                self.priotyCombo.setCurrentIndex(index)
            
    def save_config(self):
        '''
        Save setting to the config file as a dictionary.
        '''
        shot = [str(item.text()) for item in self.shList.selectedItems()] 
        rl = [str(item.text()) for item in self.rlList.selectedItems()]
        
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        config = open( '%s' % self.config_path, 'w')
        config.write('USERNAME=%s\n'% (self.UserText.text()))
        config.write('SHOT=%s\n' % (shot))
        config.write('RENDERLAYER=%s\n' % (rl))
        config.write('SAVEFILE=%s\n' % (self.saveFileCheck.checkState()))
        config.write('DELETEFRAMES=%s\n' % (self.DeleteFramesCheck.checkState()))
        #config.write('APPROVE=%s\n' % (self.ApproveCheck.checkState()))
        config.write('USEGI=%s\n' % (self.GICheck.checkState()))
        config.write('PRIOTY=%s\n' % (str(self.priotyCombo.currentText())))
        config.write('MINSEQDIV=%s\n'% (self.minSeqDivInput.text()))
        config.write('MAXSEQDIV=%s\n'% (self.maxSeqDivInput.text()))
        config.close()
        
        self.load_config()
        return self.config_path
    
def dsSubmit():
    global myWindow
    myWindow = Window()
    myWindow.show()