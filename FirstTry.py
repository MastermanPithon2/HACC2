from Globals import *

class UserInput (threading.Thread):
    def __init__ (self, commandQueue, syncQueue):
        threading.Thread__init__ (self)
        self.CommandQueue = commandQueue
        self.SyncQueue = syncQueue

    def run (self):
        global CommandQueue
        global CurrentDirection
        global CurrentSpeed
        global Accelerating

        sync = self.SyncQueue.get ()
        dev = InputDevice('/dev/input/event1')

        for event in dev.read_loop ():
            if event.type == ecodes.EV_KEY:
                key = categorize (event)

                newDirection = CurrentDirection
                if event.keystate == KeyEvent.key_down:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode:
                        if GoingBackwards ():
                            CurrentSpeed = 0x00
                        elif CurrentSpeed < Speed.S15:
                            CurrentSpeed += 1
                        Accelerating = True
                    elif ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        if GoingForwards ():
                            CurrentSpeed == 0x00
                        elif CurrentSpeed < Speed.S15:
                            CurrentSpeed += 1
                        Accelerating = True
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode:
                        if GoingForwards ():
                            newDirection = Direction.FLeft
                        elif GoingBackwards ():
                            newDirection = Direction.BLeft
                        else:
                            newDirection = Direction.Left
                    elif ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        if GoingForwards ():
                            newDirection = Direction.FRight
                        elif GoingBackwards ():
                            newDirection = Direction.BRight
                        else:
                            newDirection = Direction.Right
                    elif ecodes.KEY[ecodes.KEY_ESC] == key.keycode:
                        newDirection = Direction.Stop
                        CurrentSpeed = Speed.Stop
                        self.SyncQueue.task_done ()
                elif event.keystate == KeyEvent.key_hold:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode:
                        if CurrentSpeed < Speed.S15:
                            CurrentSpeed += 1
                        Accelerating = True
                    elif ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        if CurrentSpeed < Speed.S15:
                            CurrentSpeed += 1
                        Accelerating = True
                elif event.keystate == KeyEvent.key_up:
                    if ecodes.KEY[ecodes.KEY_UP] == key.keycode:
                        Accelerating = False
                    elif ecodes.KEY[ecodes.KEY_DOWN] == key.keycode:
                        Accelerating = False
                    elif ecodes.KEY[ecodes.KEY_LEFT] == key.keycode or ecodes.KEY[ecodes.KEY_RIGHT] == key.keycode:
                        if GoingForwards ():
                            newDirection = Direction.Forwards
                        elif GoingBackwards ():
                            newDirection = Direction.Backwards

                CurrentDirection = newDirection
                self.CommandQueue.put (CreateCommand (CurrentDirection, CurrentSpeed))


                    
        
def GoingForwards ():
    global CurrentDirection
    return CurrentDirection == Direction.Forwards or CurrentDirection == Direction.FLeft or CurrentDirection == Direction.FRight

def GoingBackwards ():
    global CurrentDirection
    return CurrentDirection == Direction.Backwards or CurrentDirection == Direction.BLeft or CurrentDirection == Direction.BRight

class CommandSender (threading.Thread):
    def __init__(self, startQueue):
        threading.Thread.__init__ (self)
        self.StartQueue = startQueue

    def run (self):
        global current_speed
        global forwards
        global backwards
        global turnLeft
        global turnRight
        global current_direction
        global sock
        global accelerating

        while True:
            control = self.StartQueue.get ()

            dev = InputDevice('/dev/input/event1')
            prev_event_time = time.time ()

            for event in dev.read_loop ():
                if event.type == ecodes.EV_KEY:
                    current_event_time = event.timestamp ()
                    event_gap = current_event_time - prev_event_time

                    keyPressed = categorize (event)
                    newCommand = False
                    
                    if self.KeyPressed (event) and event_gap > 0.15:
                        if ecodes.KEY[ecodes.KEY_LEFT] == keyPressed.keycode:
                            print ("LEFT")
                            newCommand = True
                            turnLeft = True
                            turnRight = False
                        if ecodes.KEY[ecodes.KEY_RIGHT] == keyPressed.keycode:
                            print ("RIGHT")
                            newCommand = True
                            turnRight = True
                            turnLeft = False
                        if ecodes.KEY[ecodes.KEY_DOWN] == keyPressed.keycode:
                            print ("DOWN")
                            newCommand = True
                            if forwards:
                                current_speed = 0
                            forwards = False
                            backwards = True
                            accelerating = True
                        if ecodes.KEY[ecodes.KEY_UP] == keyPressed.keycode:
                            print ("UP")
                            newCommand = True
                            if backwards:
                                current_speed = 0
                            forwards = True
                            backwards = False
                            accelerating = True
                        if ecodes.KEY[ecodes.KEY_ESC] == keyPressed.keycode:
                            print ("ESC")
                            newCommand = True
                            forwards = False
                            backwards = False
                            turnLeft = False
                            turnRight = False
                            current_speed = 0x00
                            self.StartQueue.task_done()

                        prev_event_time = current_event_time                        

                    if not self.KeyPressed (event):
                        if ecodes.KEY[ecodes.KEY_UP] == keyPressed.keycode or ecodes.KEY[ecodes.KEY_DOWN] == keyPressed.keycode:
                            print ("UP/DOWN not pressed")
                            newCommand = True
                            accelerating = False
                        elif ecodes.KEY[ecodes.KEY_LEFT] == keyPressed.keycode or ecodes.KEY[ecodes.KEY_RIGHT] == keyPressed.keycode:
                            print ("LEFT/RIGHT not pressed")
                            newCommand = True
                            turnLeft = False
                            turnRight = False

                    if forwards:
                        if turnLeft:
                            current_direction = 0x50
                        elif turnRight:
                            current_direction = 0x60
                        else:
                            current_direction = 0x10
                    elif backwards:
                        if turnLeft:
                            current_direction = 0x70
                        elif turnRight:
                            current_direction = 0x80
                        else:
                            current_direction = 0x20
                    else:
                        if turnLeft:
                            current_direction = 0x30
                        elif turnRight:
                            current_direction = 0x40
                        else:
                            current_direction = 0x10

                    if newCommand:
                        print ("%x" % current_direction, forwards, backwards, turnLeft, turnRight)
                        sock.send(chr(current_direction | current_speed))

    def GoingForwards (self):
        global current_direction
        return (current_direction == 0x10) or (current_direction == 0x50) or (current_direction == 0x60)

    def GoingBackwards (self):
        global current_direction
        return (current_direction == 0x20) or (current_direction == 0x70) or (current_direction == 0x80)

    def OnUpPress (self):
        global current_direction
        if (current_direction == 0x70):
            current_direction = 0x50
        elif (current_direction == 0x80):
            current_direction = 0x60
        elif current_direction != 0x50 and current_direction != 0x60:
            current_direction = 0x10
        
    def OnDownPress (self):
        global current_direction
        if (current_direction == 0x50):
            current_direction = 0x70
        elif (current_direction == 0x60):
            current_direction = 0x80
        elif current_direction != 0x70 and current_direction != 0x80:
            current_direction = 0x20

    def KeyPressed (self, event):
        return event.value == 1 or event.value == 2


                            
class DecelerateCar(threading.Thread):
    """With no keys pressed, decelerate the i-racer slowly"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global current_speed
        global current_direction
        global sock
        global accelerating

        while True:

            if (accelerating == True):
                if current_speed < 0xF0:
                    current_speed += 1
                    print ("accelerating")
                time.sleep(0.15)


            else:
            # gradually slow down the car
                if (current_speed > 0):
                    print ("deccelerating")
                    current_speed -= 1
                    sock.send(chr(current_direction | current_speed))
                time.sleep(0.3)                    
                        

def main():

    global CommandQueue
    global CurrentDirection
    global CurrentSpeed
    global Accelerating

    #Set Car Speed and Direction
    CommandQueue = Queue.Queue (2)
    CurrentDirection = Direction.Stop
    CurrentSpeed = Speed.Stop
    Accelerating = False

    CommandQueue.put (CreateCommand (CurrentDirection, CurrentSpeed))
    
    btAddr = '20:13:05:30:00:30'
    port = 1
    sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
    sock.connect ((btAddr, port))

    SyncQueue = Queue.Queue ()
    inputThread = UserInput (CommandQueue, SyncQueue)
    inputThread.setDaemon (True)
    inputThread.start ()

    commandThread = CommandSender (CommandQueue)
    commandThread.setDaemon (True)
    commandThread.start ()

    SyncQueue.put ("Start")
    

    #wait on the queue until stop key pressed and then exit     
    SyncQueue.join()

    sock.close ()

def CreateCommand (currentDirection, currentSpeed):
    return currentDirection | currentSpeed

main()
