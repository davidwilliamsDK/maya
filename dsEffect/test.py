import os, string, shutil
import threading, Queue
 
def dsMultiThread(inputlist):

    print "Inputlist received..."
    print inputlist
 
    print "Spawning the {0} threads.".format(THREAD_LIMIT)
    for x in xrange(THREAD_LIMIT):
        print "Thread {0} started.".format(x)
        workerbee().start()
 
    # Put stuff in queue
    print "Putting stuff in queue"
    for i in inputlist:
        try:
            jobs.put(i, block=True, timeout=5)
        except:
            singlelock.acquire()
            print "The queue is full !"
            singlelock.release()
 
    singlelock.acquire()
    print "Waiting for threads to finish."
    singlelock.release()
    jobs.join()

class workerbee(threading.Thread):
    def run(self):
        while 1:
            try:
                job = jobs.get(True,1)
                singlelock.acquire()
                print job[0]
                print job[1]
                shutil.copy(job[0],job[1])
                
                singlelock.release()
                jobs.task_done()
            except:
                break

start = r"P:\Lego_Superheroes\film\2013_Fall_SuperheroA_014598\q0010\s0010\rawRender\Mask_RL"
startDest = r"S:\Lego_SuperHeroes\film\2013_Fall_SuperheroA_014598\q0010\s0010\comp\published3D\Mask\v005"
tmpList = os.listdir(start)

masterList = []
for t in tmpList:
    newList = []
    fName = string.rsplit(t,"/",-1)[-1]
    source = start + "/" +t
    dest = startDest + "/" + fName
    newList.append(source)
    newList.append(dest)
    if newList not in masterList:
        masterList.append(newList)
        
THREAD_LIMIT = len(tmpList)
jobs = Queue.Queue(10)
singlelock = threading.Lock()
dsMultiThread(masterList)

