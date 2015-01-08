class Direction:
    Stop = 0x00
    Forwards = 0x10
    Backwards = 0x20
    Left = 0x30
    Right = 0x40
    FLeft = 0x50
    FRight = 0x60
    BLeft = 0x70
    BRight = 0x80

class Speed:
    Stop = 0x00
    S01 = 0x01
    S02 = 0x02
    S03 = 0x03
    S04 = 0x04
    S05 = 0x05
    S06 = 0x06
    S07 = 0x07
    S08 = 0x08
    S09 = 0x09
    S10 = 0x0A
    S11 = 0x0B
    S12 = 0x0C
    S13 = 0x0D
    S14 = 0x0E
    S15 = 0x0F

class iRacerState:
    def __init__ (self, direction, speed, accelerating, maxSpeed):
        self.Direction = direction
        self.Speed = speed
        self.Accelerating = accelerating
        self.MaxSpeed = maxSpeed

    def GenChr (self):
        return chr(self.Direction | self.Speed)

    def Straighten (self):
        if self.IsForwards ():
            self.Direction = Direction.Forwards
        elif self.IsBackwards ():
            self.Direction = Direction.Backwards

    def Stop (self):
        self.Direction = Direction.Forwards
        self.Speed = Speed.Stop

    def IncreaseSpeed (self):
        if self.Speed < self.MaxSpeed:
            self.Speed += 1

    def DecreaseSpeed (self):
        if self.Speed > Speed.Stop:
            self.Speed -= 1

    def IsForwards (self):
        return self.Direction == Direction.Forwards or self.Direction == Direction.FLeft or self.Direction == Direction.FRight

    def IsBackwards (self):
        return self.Direction == Direction.Backwards or self.Direction == Direction.BLeft or self.Direction == Direction.BRight

    def IsLeft (self):
        return self.Direction == Direction.BLeft or self.Direction == Direction.FLeft or self.Direction == Direction.Left

    def IsRight (self):
        return self.Direction == Direction.BRight or self.Direction == Direction.FRight or self.Direction == Direction.Right

    def SetDirection (self, newDirection):
        if newDirection == Direction.Forwards:
            if self.IsForwards ():
                self.Accelerating = True
            else:
                self.Speed = 0x00
                self.Accelerating = False
                if self.Direction == Direction.BLeft:
                    self.Direction = Direction.FLeft
                elif self.Direction == Direction.BRight:
                    self.Direction = Direction.FRight
                else:
                    self.Direction = Direction.Forwards

        elif newDirection == Direction.Backwards:
            if self.IsBackwards ():
                self.IncreaseSpeed ()
                self.Accelerating = True
            else:
                self.Speed = 0x00
                self.Accelerating = False
                if self.Direction == Direction.FLeft:
                    self.Direction = Direction.BLeft
                elif self.Direction == Direction.FRight:
                    self.Direction = Direction.BRight
                else:
                    self.Direction = Direction.Backwards

        elif newDirection == Direction.Left:
            if self.IsBackwards ():
                self.Direction = Direction.BLeft
            elif self.IsForwards ():
                self.Direction = Direction.FLeft
            else:
                self.Direction = Direction.Left

        elif newDirection == Direction.Right:
            if self.IsBackwards ():
                self.Direction = Direction.BRight
            elif self.IsForwards ():
                self.Direction = Direction.FRight
            else:
                self.Direction = Direction.Right

