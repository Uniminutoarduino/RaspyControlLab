#Proporcional Integral Controller (PI), ZOH (Zero Order Holder) method
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn

Reference = 25.0 #Setpoint (desired level)
kp = 350.0 #Proportional constant
ErrorPrev= 0.0 #Previous control e(KT-1)
Error = 0.0 #Error variable
Sensor = 0.0 #Sensor variable
ControlPrev = 0.0 #Previous control c(KT-1)
controlpi = 0.0
DutyCycle = 0.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490) #GPIO 13 PWM, f=490Hz
pwm13.start(0)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490) #GPIO 12 PWM, f=490Hz
i2c = busio.I2C(board.SCL, board.SDA)
ts = 0.6 #Sample time
ads = ADS.ADS1115(i2c) #Configure ADS1115
chan = AnalogIn(ads, ADS.P0)
while True: #Infinite Loop
    Sensor = round(chan.voltage,3)
    Error = round ((Reference*0.0482)-Sensor,3)
    controlpi = round (Error * kp - 119.4 * ErrorPrev+ ControlPrev,3) #control equation
    if (controlpi > 1.0):
        controlpi = 1.0

    if (DutyCycle < 0.0): #(antiwind-up) PI control
        DutyCycle = 0.0
    if (Error < 0.0):
        Error = 0.0
    if (controlpi < 0.0):
        controlpi = 0.0
    DutyCycle = round (controlpi * 100,3)
    pwm12.ChangeDutyCycle(DutyCycle) #PWM duty cycle depends on PI Controller
    time.sleep (ts)
    ControlPrev = controlpi
    ErrorPrev= Error
    