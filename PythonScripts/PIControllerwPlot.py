#Script for PI controller (ZOH method)
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
#ADS1115 library
from adafruit_ads1x15.analog_in import AnalogIn
#Library for plot variables
import plotter as plot

SetPoint = 17.0 #Setpoint in cm
kp = 350.0 #Proportional constant
PrevError = 0.0 #Error variables
Error = 0.0 
Sensor = 0.0
PrevControl= 0.0
controlpi = 0.0
DutyCycle = 0.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490) #GPIO 13, 490Hz
pwm13.start(0)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490) #GPIO 12, 490Hz
pwm12.start(0)
i2c = busio.I2C(board.SCL, board.SDA)
ts = 0.6 #Sampling Time
ads = ADS.ADS1115(i2c) #ADS1115 configuration
chan = AnalogIn(ads, ADS.P0)
while True: 
    Sensor = round(chan.voltage,3)
    Error = round ((SetPoint*0.0482)-Sensor,3)
    controlpi = round (Error * kp - 119.4 * PrevError + PrevControl,3) #Controller equation
    if (controlpi > 1.0):
        controlpi = 1.0

    if (DutyCycle < 0.0): #(antiwind-up) for PI control
        DutyCycle = 0.0
    if (Error < 0.0):
        Error = 0.0
    if (controlpi < 0.0):
        controlpi = 0.0
    DutyCycle = round (controlpi * 100,3)
    pwm12.ChangeDutyCycle(DutyCycle) #Duty cycle in function of controller output
    time.sleep (ts)
    PrevControl= controlpi
    PrevError = Error
    plot.plot1m(str(Sensor*20.75)) #Plot tank level