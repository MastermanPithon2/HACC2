import time
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM)


# Works with HC-SR04 Module
# A class for ultrasonic sensors to make it easier to work with
# Ultrasonic sensor data is very unreliable.  Results must be
# processed to improved accuracy
# Sets RPi.GPIO mode to BCM.
class SonicSensor:
    # Input name , output pin and input pin to init the sensor
    # Sensor may take up to half a second before it is ready to
    # return distance data
    def __init__ (self, sensorName, outPin, inPin):
        self.Name = sensorName
        self.OutPin = outPin
        self.InPin = inPin
        GPIO.setup (outPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup (inPin, GPIO.IN)

    # Sends a ping and returns the round trip time
    def PingTime (self):
        GPIO.output (self.OutPin, GPIO.HIGH)
        time.sleep (0.00001)
        GPIO.output (self.OutPin, GPIO.LOW)

        timeOut = time.time ()
        start = time.time ()
        while GPIO.input (self.InPin) == GPIO.LOW and (start - timeOut) < 0.01:
            start = time.time ()

        timeOut = time.time ()
        stop = time.time ()
        while GPIO.input (self.InPin) == GPIO.HIGH and (stop - timeOut) < 0.01:
            stop = time.time ()

        elapsedTime = stop - start
        return elapsedTime
        
    # Sends a ping and returns the distance measured in cm
    def PingCM (self):
        elapsedTime = self.PingTime ()
        distance = elapsedTime * 17014.5
        return distance

    # Sends a ping and returns the distance measured in inches
    def PingInch (self):
        elapsedTime = self.PingTime ()
        distance = elapsedTime * 6698.62
        return distance        
            
