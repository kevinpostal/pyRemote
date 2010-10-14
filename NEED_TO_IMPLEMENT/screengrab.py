"""
A simple screen grabbing utility

@author Fabio Varesano - 
@date 2009-03-17
"""


from PIL import ImageGrab
import time

time.sleep(5)
ImageGrab.grab().save("screen_capture.jpg", "JPEG")
