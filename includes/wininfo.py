
import win32pdh
import urllib
import ctypes
#PSAPI.DLL
psapi = ctypes.windll.psapi
#Kernel32.DLL
kernel = ctypes.windll.kernel32

class WinInfo():
    def get_RemoteIP(self):
        ip = urllib.urlopen('http://www.biranchi.com/ip.php').read()
        return ip.__str__()
    
    
    def get_TotalSize(self,drive):
        """ Return the TotalSize of a shared drive [GB]"""
        try:
            fso = com.Dispatch("Scripting.FileSystemObject")
            drv = fso.GetDrive(drive)
            return drv.TotalSize/2**30
        except:
            return 0
 
    def get_FreeSpace(self,drive):
        """ Return the FreeSpace of a shared drive [GB]"""
        try:
            fso = com.Dispatch("Scripting.FileSystemObject")
            drv = fso.GetDrive(drive)
            return drv.FreeSpace/2**30
        except:
            return 0

    
    def get_display_name(self):
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        NameDisplay = 3

        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(NameDisplay, None, size)

        nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(NameDisplay, nameBuffer, size)
        return nameBuffer.value
    
    def get_registry_value(self,key, subkey, value):
        import _winreg
        key = getattr(_winreg, key)
        handle = _winreg.OpenKey(key, subkey)
        (value, type) = _winreg.QueryValueEx(handle, value)
        return value
        
    def get_Cpu(self):
        try:
            cputype = self.get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
                "ProcessorNameString")
        except:
            import wmi, pythoncom
            pythoncom.CoInitialize()
            c = wmi.WMI()
            for i in c.Win32_Processor ():
                cputype = i.Name
            pythoncom.CoUninitialize()
     
        if cputype == 'AMD Athlon(tm)':
            c = wmi.WMI()
            for i in c.Win32_Processor ():
                cpuspeed = i.MaxClockSpeed
            cputype = 'AMD Athlon(tm) %.2f Ghz' % (cpuspeed / 1000.0)
        elif cputype == 'AMD Athlon(tm) Processor':
            import wmi
            c = wmi.WMI()
            for i in c.Win32_Processor ():
                cpuspeed = i.MaxClockSpeed
            cputype = 'AMD Athlon(tm) %s' % cpuspeed
        else:
            pass
        return cputype
     
    def os_version(self):
        def get(key):
            return self.get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
                key)
        os = get("ProductName")
        sp = get("CSDVersion")
        build = get("CurrentBuildNumber")
        return "%s %s (build %s)" % (os, sp, build)
    
    def systemUptime(self):
        path = win32pdh.MakeCounterPath((None, r'System', None, None, 0,"System Up Time"))
        query = win32pdh.OpenQuery()
        handle = win32pdh.AddCounter(query, path)
        win32pdh.CollectQueryData(query)
        seconds = win32pdh.GetFormattedCounterValue(handle,win32pdh.PDH_FMT_LONG | win32pdh.PDH_FMT_NOSCALE )[ 1 ]
        uptime = seconds / 3600
        return uptime
    
    def processList(self):
        ProcessList = "\n"
        arr = ctypes.c_ulong * 256
        lpidProcess= arr()
        cb = ctypes.sizeof(lpidProcess)
        cbNeeded = ctypes.c_ulong()
        hModule = ctypes.c_ulong()
        count = ctypes.c_ulong()
        modname = ctypes.c_buffer(30)
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        
        #Call Enumprocesses to get hold of process id's
        psapi.EnumProcesses(ctypes.byref(lpidProcess),
                            cb,
                            ctypes.byref(cbNeeded))
        
        #Number of processes returned
        nReturned = cbNeeded.value/ctypes.sizeof(ctypes.c_ulong())
        
        pidProcess = [i for i in lpidProcess][:nReturned]
        
        for pid in pidProcess:
            
            #Get handle to the process based on PID
            hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                                          False, pid)
            if hProcess:
                psapi.EnumProcessModules(hProcess, ctypes.byref(hModule), ctypes.sizeof(hModule), ctypes.byref(count))
                psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, ctypes.sizeof(modname))
                ProcessList +=  "".join([ i for i in modname if i != '\x00']) + "\n"
                
                #-- Clean up
                for i in range(modname._length_):
                    modname[i]='\x00'
                
                kernel.CloseHandle(hProcess)
        return ProcessList
    
    def getOpenPorts(self):
        """
            This function will return a list of ports (TCP/UDP) that the current 
            machine is listening on. It's basically a replacement for parsing 
            netstat output but also serves as a good example for using the 
            IP Helper API:
            http://msdn.microsoft.com/library/default.asp?url=/library/en-
            us/iphlp/iphlp/ip_helper_start_page.asp.
            I also used the following post as a guide myself (in case it's useful 
            to anyone):
            http://aspn.activestate.com/ASPN/Mail/Message/ctypes-users/1966295
       
         """
        portList = []
               
        DWORD = ctypes.c_ulong
        NO_ERROR = 0
        NULL = ""
        bOrder = 0
        
        # define some MIB constants used to identify the state of a TCP port
        MIB_TCP_STATE_CLOSED = 1
        MIB_TCP_STATE_LISTEN = 2
        MIB_TCP_STATE_SYN_SENT = 3
        MIB_TCP_STATE_SYN_RCVD = 4
        MIB_TCP_STATE_ESTAB = 5
        MIB_TCP_STATE_FIN_WAIT1 = 6
        MIB_TCP_STATE_FIN_WAIT2 = 7
        MIB_TCP_STATE_CLOSE_WAIT = 8
        MIB_TCP_STATE_CLOSING = 9
        MIB_TCP_STATE_LAST_ACK = 10
        MIB_TCP_STATE_TIME_WAIT = 11
        MIB_TCP_STATE_DELETE_TCB = 12
        
        ANY_SIZE = 1         
        
        # defing our MIB row structures
        class MIB_TCPROW(ctypes.Structure):
            _fields_ = [('dwState', DWORD),
                        ('dwLocalAddr', DWORD),
                        ('dwLocalPort', DWORD),
                        ('dwRemoteAddr', DWORD),
                        ('dwRemotePort', DWORD)]
        
        class MIB_UDPROW(ctypes.Structure):
            _fields_ = [('dwLocalAddr', DWORD),
                        ('dwLocalPort', DWORD)]
      
        dwSize = DWORD(0)
        
        # call once to get dwSize 
        ctypes.windll.iphlpapi.GetTcpTable(NULL, ctypes.byref(dwSize), bOrder)
        
        # ANY_SIZE is used out of convention (to be like MS docs); even setting this
        # to dwSize will likely be much larger than actually necessary but much 
        # more efficient that just declaring ANY_SIZE = 65500.
        # (in C we would use malloc to allocate memory for the *table pointer and 
        #  then have ANY_SIZE set to 1 in the structure definition)
        
        ANY_SIZE = dwSize.value
        
        class MIB_TCPTABLE(ctypes.Structure):
            _fields_ = [('dwNumEntries', DWORD),
                        ('table', MIB_TCPROW * ANY_SIZE)]
        
        tcpTable = MIB_TCPTABLE()
        tcpTable.dwNumEntries = 0 # define as 0 for our loops sake

        # now make the call to GetTcpTable to get the data
        if (ctypes.windll.iphlpapi.GetTcpTable(ctypes.byref(tcpTable), 
            ctypes.byref(dwSize), bOrder) == NO_ERROR):
          
            maxNum = tcpTable.dwNumEntries
            placeHolder = 0
            
            # loop through every connection
            while placeHolder < maxNum:
            
                item = tcpTable.table[placeHolder]
                placeHolder += 1
                
                # format the data we need (there is more data if it is useful - 
                #    see structure definition)
                lPort = item.dwLocalPort
                lPort = socket.ntohs(lPort)
                lAddr = item.dwLocalAddr
                lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
                portState = item.dwState
                        
                # only record TCP ports where we're listening on our external 
                #    (or all) connections
                if str(lAddr) != "127.0.0.1" and portState == MIB_TCP_STATE_LISTEN:
                    portList.append(str(lPort) + "/TCP")
        
        else:
            print "Error occurred when trying to get TCP Table"

        dwSize = DWORD(0)
        
        # call once to get dwSize
        ctypes.windll.iphlpapi.GetUdpTable(NULL, ctypes.byref(dwSize), bOrder)
        
        ANY_SIZE = dwSize.value # again, used out of convention 
        #                            (see notes in TCP section)
        
        class MIB_UDPTABLE(ctypes.Structure):
            _fields_ = [('dwNumEntries', DWORD),
                        ('table', MIB_UDPROW * ANY_SIZE)]  
                        
        udpTable = MIB_UDPTABLE()
        udpTable.dwNumEntries = 0 # define as 0 for our loops sake
        
        # now make the call to GetUdpTable to get the data
        if (ctypes.windll.iphlpapi.GetUdpTable(ctypes.byref(udpTable), 
            ctypes.byref(dwSize), bOrder) == NO_ERROR):
        
            maxNum = udpTable.dwNumEntries
            placeHolder = 0
            while placeHolder < maxNum:

                item = udpTable.table[placeHolder]
                placeHolder += 1
                lPort = item.dwLocalPort
        
                lPort = socket.ntohs(lPort)
                lAddr = item.dwLocalAddr
                
                lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
                
                # only record UDP ports where we're listening on our external 
                #    (or all) connections
                if str(lAddr) != "127.0.0.1":
                    portList.append(str(lPort) + "/UDP")
        else:
            print "Error occurred when trying to get UDP Table"
        
        portList.sort()  
        
        return portList