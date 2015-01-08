from KeyboardInput import *
from CommandSender import *

                           
def main():

    iracer = iRacerState (Direction.Stop, Speed.Stop, False, Speed.S08)

    btAddr = '20:13:05:30:00:30'
    port = 1
    socket = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
    syncQueue = Queue.Queue ()
    try:
        socket.connect ((btAddr, port))

        inputDeviceName = '/dev/input/event1'
        inputThread = KeyboardInput (iracer, syncQueue, inputDeviceName)
        inputThread.setDaemon (True)
        inputThread.start ()

        commandThread = CommandSender (iracer, socket)
        commandThread.setDaemon (True)
        commandThread.start ()

        syncQueue.put ("Start")
        

        #wait on the queue until stop key pressed and then exit     
        syncQueue.join()
    finally:
        socket.close ()


main()
