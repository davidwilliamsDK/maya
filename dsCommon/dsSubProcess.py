import subprocess

'''
command = '//vfx-render-manager/royalrender/bin/win/rrSubmitterconsole.exe ' + str(rrFile) +' UserName=0~' + str(self.user)  + ' DefaulClientGroup=1~' + 'All' + ' Priority=2~70 RRO_AutoApproveJob=3~False'
print self.dsProcess(command).communicate()[0]
'''
   
def dsProcess(  cmd_line):
    cmd = cmd_line.split(' ')
    proc = subprocess.Popen(cmd, 
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
    return proc