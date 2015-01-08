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
                    self.iRacer.Stop ()
                    self.SyncQueue.task_done ()
                    return
                
                if key.keystate == KeyEvent.key_down or key.keystate == KeyEvent.key_hold:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode:
                        self.iRacer.SetDirection (Direction.Forwards)
                    elif ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        self.iRacer.SetDirection (Direction.Backwards)
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode:
                        self.iRacer.SetDirection (Direction.Left)
                    elif ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        self.iRacer.SetDirection (Direction.Right)
                elif key.keystate == KeyEvent.key_up:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode or ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        self.iRacer.Accelerating = False
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode or ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        self.iRacer.Straighten ()




