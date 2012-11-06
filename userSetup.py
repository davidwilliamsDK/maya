import maya.cmds as cmds
import maya.mel as mel
import os, sys

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
else:
    cmds.dirmap( en=True )
    cmds.dirmap( m=('\\\\vfx-data-server\\dsPipe\\','/dsPipe/') )
    cmds.dirmap( m=('P:\\','/dsPipe/') )
