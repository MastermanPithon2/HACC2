import threading
import bluetooth
import time

from iRacer import *

class CommandSender (threading.Thread):
    def __init__ (self, iracer, socket):
        threading.Thread.__init__(self)
        self.LastDirection = Direction.Stop
        self.LastSpeed = Speed.Stop
        self.iRacer = iracer
        self.Socket = socket


    def run (self):
        while True:
            if self.iRacer.Accelerating:
                self.iRacer.IncreaseSpeed ()
            else:
                self.iRacer.DecreaseSpeed ()
            
            if (self.LastDirection != self.iRacer.Direction) or (self.LastSpeed != self.iRacer.Speed):
                self.Socket.send (self.iRacer.GenChr ())
                self.LastDirection = self.iRacer.Direction
                self.LastSpeed = self.iRacer.Speed

            time.sleep (0.15)
