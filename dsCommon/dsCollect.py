import os,re,sys

global rv,rvpush

if sys.platform == "linux2":
    rv = "'/usr/local/rv-Linux-x86-64-3.12.20/bin/rv'"
    rvpush = "'/usr/local/rv-Linux-x86-64-3.12.20/bin/rvpush'"
    
elif sys.platform == 'win32':
    rv = '"C:/Program Files (x86)/Tweak/RV-3.12.20-32/bin/rv.exe"'
    rvpush = '"C:/Program Files (x86)/Tweak/RV-3.12.20-32/bin/rvpush.exe"'


def getLatest(path):
    if sys.platform == 'linux2':
        verList = os.listdir(path)
        verList.sort()
        return verList[-1] 
    else:
        verList = os.listdir(path)
        verList.sort()
        return verList[-1] 

def sgGetFrameInfo(filePath):
    fileSplit = filePath.split("/")
    extSplit = filePath.split(".")
    renderlayerDir = filePath.replace("/" + fileSplit[-1],"")
    fileList = os.listdir(renderlayerDir)
    fListClean = []
    for file in fileList:
        fileSplit = file.split(".")
        if fileSplit[-1] == extSplit[-1]:
            fListClean.append(file)
    fListClean.sort()
    frame_count = len(fListClean)
    startFrame = fListClean[0]
    startObj = re.search("[0-9][0-9][0-9][0-9]\.",startFrame)
    sg_start_frame = startObj.group()[:-1]
    endFrame = fListClean[-1]
    endObj = re.search("[0-9][0-9][0-9][0-9]\.",endFrame)
    sg_end_frame = endObj.group()[:-1]
    frameInfo = {'frame_count':frame_count,'sg_start_frame':sg_start_frame,'sg_end_frame':sg_end_frame,'startFrame':startFrame,'endFrame':endFrame,'sg_file_name':startObj}
    return frameInfo

def rvPush(path):
    global rv,rvpush
    '''
    if sys.platform == "linux2":
        rv = "'/usr/local/rv-Linux-x86-64-3.12.20/bin/rv'"
        rvpush = "'/usr/local/rv-Linux-x86-64-3.12.20/bin/rvpush'"
    
    elif sys.platform == 'win32':
        rv = '"C:/Program Files (x86)/Tweak/RV-3.12.20-32/bin/rv.exe"'
        rvpush = '"C:/Program Files (x86)/Tweak/RV-3.12.20-32/bin/rvpush.exe"'
    '''
    #cmd = rvpush + ' merge %s' % (path)
    cmd = rvpush + ' -tag something merge %s' % (path)
    os.system(cmd)
    print "open framestack in RV"
    
def rvQT(input,fps,x,y,output):
    global rv,rvpush
    '''
    if sys.platform == "linux2":
        rvio = "'/usr/local/rv-Linux-x86-64-3.12.20/bin/rvio'"
    elif sys.platform == 'win32':
        rvio = '"C:/Program Files (x86)/Tweak/RV-3.12.20-32/bin/rvio.exe"'
    ''' 
    cmd = rvio + ' -vv %s -fps %s -outres %s %s -o %s' % (input,fps,x,y,output)
    print cmd
    #cmd = rvio + ' -vv %s -quality 0.75 -outres %s %s -o %s' % (input,x,y,output)
    #os.system(cmd)

def parseLatest(path,val):
    shotList = []
    fsList = []
    if val == "comp":
        print "comp"
        sl_tmp = os.listdir(path)
        for s in sl_tmp:
            if re.search("s[0-9][0-9][0-9][0-9]",s):
                shotList.append(s)
        for s in shotList:
            shot = s
            ver = getLatest(path + "/" + s + "/comp/compOut/")
            rootPath = path + "/" +  shot + "/comp/compOut/" + ver
            tl = os.listdir(rootPath)
            newName = tl[0][0:-8] + "####." + tl[0][-3:]
            filePath = rootPath + "/" + newName
            fsList.append(filePath)
        fsList.sort()
        path = ' '.join(fsList)
        rvPush(path)
    if val == "playBlast":
        print "playblast"
        path = path + "/3D/playBlast/"
        sl_tmp = os.listdir(path)
        for s in sl_tmp:
            if re.search("s[0-9][0-9][0-9][0-9]",s):
                shotList.append(s)
        for s in shotList:
            shot = s
            ver = getLatest(path + "/" + s)
            rootPath = path + "/" +  shot + "/" + ver
            tl = os.listdir(rootPath)
            for t in tl:
                if not re.search('.ma',t):
                    newName = t[0:-9] + "####." + t[-4:]
            filePath = rootPath + "/" + newName
            fsList.append(filePath)
        fsList.sort()
        path = ' '.join(fsList)
        rvPush(path)
    if val == "online":
        print "online"
        sl_tmp = os.listdir(path)
        for s in sl_tmp:
            if re.search("s[0-9][0-9][0-9][0-9]",s):
                shotList.append(s)
        for s in shotList:
            shot = s
            rootPath = path + "/" +  shot + "/published2D/compOut/DPX/"
            tl = os.listdir(rootPath)
            newName = tl[0][0:-8] + "####." + tl[0][-3:]
            filePath = rootPath + "/" + newName
            fsList.append(filePath)
        fsList.sort()
        path = ' '.join(fsList)
        rvPush(path)