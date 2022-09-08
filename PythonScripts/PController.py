#Script for proportional controller (P)
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
LevelReference = 15 #Setpoint (15 cm)
kp = 100.0 #Proportional constant
DutyCycle = 0
Error = 0.0
Sensor = 0.0
ControlP = 0.0 #Controller variable
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490) #GPIO13, PWM, f=490Hz (T1 motor pump)
pwm13.start(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490) #GPIO12, PWM, f=490Hz (T2 motor pump, fills tank T1)
pwm12.start(0)
#ADS1115 configuration
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

while True:
    Sensor = round(chan.voltage,3) #Read sensor value
    Error = round ((LevelReference*0.0482)-Sensor,3)
    ControlP = round (Error * kp,3) #Proportional control error
    ControlP = round (ControlP * 0.08333,3)
    if (ControlP>1.0):
        ControlP = 1.0
        
    if (Error<0.0): #PWM limitation (saturation)
        Error = 0.0
        
    if (ControlP<0.0):
        ControlP = 0.0
        
    DutyCycle = round (ControlP * 100.0,3)
    pwm12.ChangeDutyCycle(DutyCycle) #Duty cycle according to controller output
    time.sleep(0.6) #Sample time 0.6 secs.