import Queue
import threading
import pygame

from pygame.locals import *

from iRacer import *
from SonicSensor import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)

class SonicInput (threading.Thread):
    def __init__ (self, iracer, syncQueue, turnTrig, turnEcho, gasTrig, gasEcho):
        threading.Thread.__init__ (self)
        self.iRacer = iracer
        self.SyncQueue = syncQueue
        self.TurnSensor = SonicSensor ("Turn", turnTrig, turnEcho)
        self.GasSensor = SonicSensor ("Gas", gasTrig, gasEcho)
        pygame.init ()
        self.Screen = pygame.display.set_mode ((640, 480))
        try:
            self.DrawRacerState ()
        except:
            pygame.quit()


    def run (self):
        try:
            sync = self.SyncQueue.get ()

            turn = 0.0
            gas = 0.0
            while (True):
                turn0 = self.TurnSensor.PingCM ()
                gas0 = self.GasSensor.PingCM ()
                turn1 = self.TurnSensor.PingCM ()
                gas1 = self.GasSensor.PingCM ()
                
                turn = (turn + turn0 + turn1 + self.TurnSensor.PingCM ())/4
                gas = (gas + gas0 + gas1 + self.GasSensor.PingCM ())/4
                print 'GAS:' + str(gas) + '  TURN:' + str(turn)

                if turn > 30:
                    self.iRacer.Straighten ()
                elif turn < 10:
                    self.iRacer.SetDirection (Direction.Left)
                elif turn > 15:
                    self.iRacer.SetDirection (Direction.Right)
                
                if gas > 50:
                    self.iRacer.Accelerating = False
                elif gas < 20:
                    self.iRacer.SetDirection (Direction.Forwards)
                else:
                    self.iRacer.SetDirection (Direction.Backwards)

                self.DrawRacerState ()

                for event in pygame.event.get ():
                    if event.type == QUIT:
                        pygame.quit ()
                        self.iRacer.Stop ()
                        self.SyncQueue.task_done ()
                        return
        finally:
            pygame.quit ()


    def DrawRacerState (self):
        self.Screen.fill (WHITE)

        if self.iRacer.IsLeft ():
            pygame.draw.polygon (self.Screen, BLACK, [[0,240],[40,480],[40,0]])
        elif self.iRacer.IsRight ():
            pygame.draw.polygon (self.Screen, BLACK, [[600,0],[600,480],[640,240]])

        accel = RED
        if self.iRacer.Accelerating:
            accel = GREEN
            
        if self.iRacer.IsForwards ():
            pygame.draw.polygon (self.Screen, accel, [[320,0],[340,40],[300,40]])
        else:
            pygame.draw.polygon (self.Screen, accel, [[300,440],[320,480],[340,440]])

        pygame.display.flip ()
