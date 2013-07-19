#import maya.cmds as cmds
import os, ast
import dsAnimSG as animSG
import dsAnimUtil as animUtil
import dsCommon.dsProjectUtil as projectUtil
reload(animSG)
reload(animUtil)
reload(projectUtil)

#Ressource Files
emptyMA = 'O:\\globalMaya\\resources\\emptyScene.ma'
logPath = 'C:\\Users\\picturethis\\Desktop\\log.txt'

def handler(projInfo):
    projInfo = stringToDict(projInfo)
    #get scene/project information
    #set fps, resolution, render software

    #get sequence shots from shotgun
    shots = animSG.getSequenceShots(projInfo['sequenceName'], projInfo['projName'], projInfo['episode'])

    #create cams
    shots = animUtil.createCams(shots)

    #create cam sequences
    sequences = animUtil.createCamSequencer(shots)

    #get linked assets from shotgun
    assets = animSG.getSequenceAssets(projInfo['sequenceName'], projInfo['projName'], projInfo['episode'])
    print assets

    #ref assets
    refPath = listAssetRefPath(projInfo['projName'], assets['sg_asset_type'], assets['sg_subtype'], assets['code'])
    print refPath

def stringToDict(string=None):
    if string:
        dict = string.rsplit('}')[0].split('{')[-1]
        dict = dict.replace(" ", "")
        dict = dict.split(",")
        newDict = {}
        for entry in dict:
            entry = entry.split(":")
            newDict[entry[0]] = entry[1]
        return newDict

def savefile():
    pass
    #cmds.file( rename=path )
    #cmds.file( save=True, type='mayaAscii' )

def launch(projInfo):
    '''This Will Launch Maya Batch and Execute a Mel that runs the handler in this Module'''
##    sequences = animSG.getEspisodeSequence(projInfo['projName'], projInfo['episode'])
    #IMPORTANT: This is just a test sequence the function above does work
    sequences = [{'type': 'Sequence', 'name': 'q0010', 'id': 155}]

    if os.path.exists(emptyMA):
        for sequence in sequences:
            projInfo['sequenceName'] = sequence['name']
            projInfo['sequenceId'] = sequence['id']
            print projInfo
            melCmd = ('source animBatchSetup; cleanMaya "%s";' % (str(projInfo)))
            print melCmd
##            os.system("maya -batch -log '%s' -command '%s' -file '%s'" % (logPath, melCmd, emptyMA))
            os.system("maya -log '%s' -command '%s' -file '%s'" % (logPath, melCmd, emptyMA))


####################################################################################################
#UI SHOULD CONTAIN DATA BELOW
####################################################################################################
##projInfo = {'projName':'Lego_Friends',
##            'episode':'LEGO_Friends_EP02_147762'}
##
##launch(projInfo)