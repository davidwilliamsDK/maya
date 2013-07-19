import maya.cmds as cmds
import os, shutil

mafile = cmds.file(sn=True, q=True)
textureLOD = ("%s/textures/LOD/" % mafile.rsplit("/", 3)[0])
textureAI = ("%s/textures/AI/" % mafile.rsplit("/", 3)[0])

def LODTextureReplace():
    '''This script will try and find the LOD textures in the correct '''
    textures = cmds.ls(type="file")
    
    for tex in textures:
        if cmds.objExists("%s.fileTextureName" % tex):
    
            #GETTING LOD TEXTURES
            filename = cmds.getAttr("%s.fileTextureName" % tex)
    
            if not os.path.exists("%s/%s" % (textureLOD, filename.rsplit("/", 1)[-1])):        
                if not os.path.exists(textureLOD):
                    os.makedirs(textureLOD)
                        
                try:
                    shutil.copyfile(filename, "%s/%s" % (textureLOD, filename.rsplit("/", 1)[-1]))
                except:
                    pass
                    
                try:
                    cmds.setAttr("%s.fileTextureName" % tex, "%s/%s" % (textureLOD, filename.rsplit("/", 1)[-1]), type="string")
                except:
                    pass
                
            #FINDING AI FILES
            aiName = filename.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    
            #FIND AI TEXTURE PATH
            filename = filename.rsplit("/", 1)[0]
            if aiName.startswith("d"):
                aiName = aiName[1:]
                
            aiFile = "%s/%s.ai" % (filename, aiName)
    
            if not os.path.exists(aiFile):
                aiFile = "%s/AI/%s.ai" % (filename.rsplit("/", 1)[0], aiName)
            
            if os.path.exists(aiFile):
                if not os.path.exists(textureAI):
                    os.makedirs(textureAI)
                    
                shutil.copyfile(aiFile, "%s/%s.ai" % (textureAI, aiName))