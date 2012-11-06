import os, re
import maya.cmds as cmds

def setGlobals():
    
    #relativePath = '%s' % os.getenv('RELATIVEPATH')
    #project = '%s' % os.getenv('PROJECT')
    #episode = '%s' % os.getenv('EPISODE')
    #sequence = '%s' % os.getenv('SEQUENCE')
    #shot = '%s' % os.getenv('SHOT')
    
    match = re.search('(?P<relative>.*)\/(?P<project>\w*)\/film\/(?P<episode>\w*)\/(?P<sequence>\w*)\/(?P<shot>\w*)', cmds.file(q=True,l=True)[0])
    
    if match:
        match = match.groupdict()
        relativePath = match['relative']
        os.environ['RELATIVEPATH'] = relativePath
        
        project = match['project']
        os.environ['PROJECT'] = project

        episode = match['episode']
        os.environ['EPISODE'] = episode

        sequence = match['sequence']
        os.environ['SEQUENCE'] = sequence

        shot = match['shot']
        os.environ['SHOT'] = shot

    else:
        pass