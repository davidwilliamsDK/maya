import itertools as it
import time
import subprocess

files = range(5)
max_load = 3
sleep_interval = 0.5

pid_list = []
for combo in it.combinations(files, 2):
    print files
    # Random command that takes time'
    cmd = "ipconfig"
  
    # Launch and record this command
    print "Launching: "+ str(combo), cmd
    pid = subprocess.Popen(cmd)
    pid_list.append(pid)

    # Deal with condtion of exceeding maximum load
    while len(filter(lambda x: x.poll() is None, pid_list)) >= max_load:
        time.sleep(sleep_interval)