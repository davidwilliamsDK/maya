import subprocess,sys,random,os,re

'''
command = '//vfx-render-manager/royalrender/bin/win/rrSubmitterconsole.exe ' + str(rrFile) +' UserName=0~' + str(self.user)  + ' DefaulClientGroup=1~' + 'All' + ' Priority=2~70 RRO_AutoApproveJob=3~False'
print self.dsProcess(command).communicate()[0]
'''

def spSG(cmd):
    "print shotgun " + cmd
    clearTmp("sgUpdate")
    
    val = random.randint(0,5000000)
    tmpPath = "C:/temp"
    if not os.path.isdir(tmpPath):os.mkdir(tmpPath)
    path =  tmpPath + "/sgUpdate_" + str(val) +  ".py"
    bFile = open(path, 'w')
    bFile.write("import sys\nsys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun')\nimport sgTools\ntry:\n\t" + str(cmd) + "\nexcept:\n\traw_input(\"Press Enter to continue...\")")
    bFile.close()
    cmd = "python "+ path
    
    subprocess.Popen(cmd, creationflags = subprocess.CREATE_NEW_CONSOLE)

def spCOPY(cmd):
    clearTmp("COPY")
    val = random.randint(0,5000000)
    if sys.platform == 'linux2':
        path =  "/tmp/COPY_" + str(val) +  ".py"
        bFile = open(path, 'w')
        bFile.write("import shutil\n" + str(cmd) + "\nraw_input(\"Press Enter to continue...\")")
    else:
        path =  "C:/temp/COPY_" + str(val) +  ".py"
        bFile = open(path, 'w')
        bFile.write("import shutil\n" + str(cmd) + "\nraw_input(\"Press Enter to continue...\")")
    bFile.close()
    cmd = "python " + path
    
    if sys.platform == "linux2":
        self.process(cmd)
    else:
        subprocess.Popen(cmd, creationflags = subprocess.CREATE_NEW_CONSOLE)


def sp(path):
    cmd = "python "+ path
    print cmd
    if sys.platform == "linux2":
        self.process(cmd)
    else:
        subprocess.Popen(cmd, creationflags = subprocess.CREATE_NEW_CONSOLE)
    

def dsProcess(  cmd_line):
    cmd = cmd_line.split(' ')
    proc = subprocess.Popen(cmd, 
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
    return proc

def clearTmp(val):
    if sys.platform == 'linux2':
        path =  "/tmp"
    else:
        path =  "C:/temp"
    tmpList = os.listdir(path)
    if val == "COPY":
        for tmp in tmpList:
            if re.search("COPY",tmp):
                print path + "/" + tmp + "##Removed"
                os.remove(path + "/" + tmp)
    if val == "sgUpdate":
        for tmp in tmpList:
            if re.search("sgUpdate",tmp):
                print path + "/" + tmp + "##Removed"
                os.remove(path + "/" + tmp)

            