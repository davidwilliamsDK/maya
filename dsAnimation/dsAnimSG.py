import sys, re, os, string, shutil, subprocess

if sys.platform == "linux2":
    sys.path.append('/dsGlobal/globalResources/Shotgun')
    sys.path.append('/dsGlobal/dsCore/maya/')
else:
    sys.path.append('//vfx-data-server/dsGlobal/globalResources/Shotgun')
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/maya')
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun')

from shotgun_api3 import Shotgun
import dsCommon.dsProjectUtil
import sgTools
import dsSgUtil as sgBridge
reload(sgBridge)

sgServer = "https://duckling.shotgunstudio.com"
scriptName = "assetOpenToShotgun"
scriptId = "e932e9c2864c9bcdc3f3ddf8b801cc3d565bf51f"
sg = Shotgun(sgServer, scriptName, scriptId)

try:
    import maya.cmds as cmds
    import maya.OpenMaya as api
    import maya.OpenMayaUI as apiUI
except:
    pass

def getEpisodeInfo(filmInfo):
    filters = [['code', 'is', filmInfo["episode"]], ['project.Project.name', 'is', filmInfo['projName']]]
    fields = ["sg_fps", "sg_resolution"]
    return sg.find("Scene", filters=filters, fields=fields)[0]

def setSequenceAssets(assetID, seq, episode, projName):
    '''This Def Links Assets To Sequences, Just feed it with the propper Shotgun Asset ID'''
    filters = [['code','is', seq], ['project.Project.name','is', str(projName)],['scene_sg_sequence_1_scenes.Scene.code','is', str(episode)]]
    seqID = sg.find_one("Sequence", filters=filters, fields=[])
    sg.update("Sequence",seqID['id'], {"assets":[assetID]})

def getSequenceAssets(seq,projName,episode):
    '''In combination With the reference tool, this module could be used to ref in assets that's linked to a sequence in shotgun'''
    #Find Linked Assets
    filters = [ ['code','is', seq], ['project.Project.name','is', str(projName)],['scene_sg_sequence_1_scenes.Scene.code','is', str(episode)]]
    mySeq = sg.find("Sequence", filters=filters,fields=['id','code', 'assets'])[0]
    assets = mySeq['assets']

    #Return list With Assets
    return assets

def getShotAsset(seq, shot, projName,episode):
    '''In combination With the reference tool, this module could be used to ref in assets that's linked to a shot in shotgun'''
    #Find Linked Assets
    filters = [['code','is', shot], ['project.Project.name','is', str(projName)], ['sg_scene.Scene.code','is', str(episode)], ['sg_sequence.Sequence.code','is', str(seq)]]
    shotinfo = sg.find("Shot", filters=filters,fields=['id','code', 'assets'])[0]
    assets = shotinfo['assets']

    #Return list With Assets
    return getAssetAttr(assets)

def getAssetAttr(asset):
    #Find asset paths
    filters = [['id','is', asset['id']]]
    info = sg.find("Asset", filters=filters,fields=['id','code', 'sg_asset_type', 'sg_subtype', 'sg_2d_3d'])[0]

    #Return a list with all linked Assets
    return info

def getEspisodeSequence(projName, episode):
    filters = [['code','is', episode], ['project.Project.name','is', str(projName)]]
    fields = ['id', 'code', 'sg_sequence_1']
    shotinfo = sg.find("Scene", filters=filters, fields=fields)[0]
    return shotinfo['sg_sequence_1']

def getSequenceShots(seq,projName,episode):
    filters = [['code','is', seq], ['project.Project.name','is', str(projName)],['scene_sg_sequence_1_scenes.Scene.code','is', str(episode)]]
    fields = ['id', 'code', 'shots']
    shotinfo = sg.find("Sequence", filters=filters, fields=fields)[0]

    shotData = []
    for shot in shotinfo['shots']:
        shotData.append( getShotInOut(shot))
    return shotData

def getShotInOut(shotinfo):
    filters = [['code', 'is', shotinfo['name' ]], ['id', 'is', shotinfo['id']]]
    fields = ['id', 'code', 'sg_cut_in', 'sg_cut_out', 'duration']
    shotinfo = sg.find("Shot", filters=filters, fields=fields)[0]
    return shotinfo