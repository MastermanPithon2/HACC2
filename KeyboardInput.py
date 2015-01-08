from evdev import InputDevice, KeyEvent, categorize, ecodes
import Queue
import threading

from iRacer import *

class KeyboardInput (threading.Thread):
    def __init__ (self, iracer, syncQueue, inputDeviceName):
        threading.Thread.__init__ (self)
        self.SyncQueue = syncQueue
        self.InputDeviceName = inputDeviceName
        self.iRacer = iracer

    def run (self):
        sync = self.SyncQueue.get ()
        dev = InputDevice(self.InputDeviceName)

        for event in dev.read_loop ():
            if event.type == ecodes.EV_KEY:
                key = categorize (event)

                if ecodes.KEY[ecodes.KEY_ESC] == key.keycode:
                    self.iRacer.Direction = Direction.Stop
                    self.iRacer.Speed = Speed.Stop
                    self.SyncQueue.task_done ()
                    return
                
                if key.keystate == KeyEvent.key_down or key.keystate == KeyEvent.key_hold:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode:
                        self.SetDirection (Direction.Forwards)
                    elif ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        self.SetDirection (Direction.Backwards)
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode:
                        self.SetDirection (Direction.Left)
                    elif ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        self.SetDirection (Direction.Right)
                elif key.keystate == KeyEvent.key_up:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode or ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        self.iRacer.Accelerating = False
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode or ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        self.iRacer.Straighten ()


    def SetDirection (self, newDirection):
        if newDirection == Direction.Forwards:
            if self.iRacer.IsForwards ():
                self.iRacer.Accelerating = True
            else:
                self.iRacer.Speed = 0x00
                self.iRacer.Accelerating = False
                if self.iRacer.Direction == Direction.BLeft:
                    self.iRacer.Direction = Direction.FLeft
                elif self.iRacer.Direction == Direction.BRight:
                    self.iRacer.Direction = Direction.FRight
                else:
                    self.iRacer.Direction = Direction.Forwards

        elif newDirection == Direction.Backwards:
            if self.iRacer.IsBackwards ():
                self.iRacer.IncreaseSpeed ()
                self.iRacer.Accelerating = True
            else:
                self.iRacer.Speed = 0x00
                self.iRacer.Accelerating = False
                if self.iRacer.Direction == Direction.FLeft:
                    self.iRacer.Direction = Direction.BLeft
                elif self.iRacer.Direction == Direction.FRight:
                    self.iRacer.Direction = Direction.BRight
                else:
                    self.iRacer.Direction = Direction.Backwards

        elif newDirection == Direction.Left:
            if self.iRacer.IsBackwards ():
                self.iRacer.Direction = Direction.BLeft
            elif self.iRacer.IsForwards ():
                self.iRacer.Direction = Direction.FLeft
            else:
                self.iRacer.Direction = Direction.Left

        elif newDirection == Direction.Right:
            if self.iRacer.IsBackwards ():
                self.iRacer.Direction = Direction.BRight
            elif self.iRacer.IsForwards ():
                self.iRacer.Direction = Direction.FRight
            else:
                self.iRacer.Direction = Direction.Right


