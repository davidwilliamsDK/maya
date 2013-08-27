import maya.cmds as cmds
import maya.mel as mel
import os, sys,threading

#sys.path.append('//vfx-data-server/dsGlobal/globalResources/Shotgun')
#from shotgun_api3 import Shotgun

print "THIS IS RUNNING A USERSETUP.PY FILE"

try:
  import vxmaya_setup
  import vxmaya_file
  import vxmaya_core
except:
  pass

mel.eval("evalDeferred dsMenu;")
#mel.eval("evalDeferred overwriteProc;")

if sys.platform == "win32":
    cmds.dirmap( en=True )
    cmds.dirmap( m=('/dsPipe/', '\\\\vfx-data-server\\dsPipe\\') )

    import dsCommon.dsCommonInit as comInit
    comInit.copyMayaPresets()
    comInit.copyVrayScripts()

else:
    cmds.dirmap( en=True )
    cmds.dirmap( m=('\\\\vfx-data-server\\dsPipe\\','/dsPipe/') )
    cmds.dirmap( m=('P:\\','/dsPipe/') )

    import dsCommon.dsCommonInit as comInit
    comInit.copyMayaPresets()
    #comInit.copyVrayScripts()
