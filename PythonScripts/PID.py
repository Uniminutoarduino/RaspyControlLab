#Script for PID controller
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn

SetPoint = 24.0 #Setpoint (10cm)
#Control variables for error and controller
PrevError_1 = 0.0
PrevError_2 = 0.0
Error = 0.0 
PrevControl_1 = 0.0
PrevControl_2 = 0.0
control_PID = 0.0
DutyCycle = 0.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490)
pwm13.start(0)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490)
pwm12.start(0)
i2c = busio.I2C(board.SCL, board.SDA)
ts = 0.6 #Sampling time
ads = ADS.ADS1115(i2c) #ADS1115 configuration
chan = AnalogIn(ads, ADS.P0)
while True:
    Sensor = round(chan.voltage,3)
    Error = round ((SetPoint*0.0482)-Sensor,3)
    #Ecuacion de control
    control_PID = round (7.754 * Error - 15.47 * PrevError_1 + 7.716 * PrevError_2 + PrevControl_2,3) #Controller equation
    if (control_PID > 1.0): #Output controller limit for PWM signal
        control_PID = 1.0

    if (DutyCycle < 0.0):
        DutyCycle = 0.0
    if (Error < 0.0):
        Error = 0.0
    if (control_PID < 0.0):
        control_PID = 0.0
    DutyCycle = round (control_PID * 100,3)
    pwm12.ChangeDutyCycle(DutyCycle) #Duty cycle in function of output controller
    time.sleep (ts) #Wait for a ts
    PrevControl_2 = PrevControl_1
    PrevControl_1 = control_PID
    PrevError_2 = PrevError_1
    PrevError_1 = Error