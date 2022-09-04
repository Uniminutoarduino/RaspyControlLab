#Script for PID controller
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn

LevelReference = 10.0 #Setpoint (10cm)
#Error variables for the PID controller
ErrorPrev = 0.0 #Previous error e(KT-1)
ErrorPrev2 = 0.0 #Previous-previous error e(KT-2)
Error = 0.0 #Error variable
ControlPrev = 0.0 #Previous control c(KT-1)
ControlPrev2 = 0.0 #Previous-previous control c(KT-2)
control_PID = 0.0
DutyCycle = 0.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT) #GPIO 13 for PWM (reservoir tank)
pwm13=GPIO.PWM(13,490)
pwm13.start(0)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(12,GPIO.OUT) #GPIO 12 for PWM (T1 control motor pump)
pwm12=GPIO.PWM(12,490)
pwm12.start(0)
i2c = busio.I2C(board.SCL, board.SDA)
ts = 0.6 #Sampling time (0.6 secs)
ads = ADS.ADS1115(i2c) #ADC1115 configuration
chan = AnalogIn(ads, ADS.P0)
while True:
    Sensor = round(chan.voltage,3)
    Error = round ((LevelReference*0.0482)-Sensor,3)
    #Ecuacion de control
    control_PID = round (7.754 * Error - 15.47 * ErrorPrev + 7.716 * ErrorPrev2 + ControlPrev2,3) #Control EQ
    if (control_PID > 1.0): #Controller limitation for PWM signal
        control_PID = 1.0

    if (DutyCycle < 0.0):
        DutyCycle = 0.0
    if (Error < 0.0):
        Error = 0.0
    if (control_PID < 0.0):
        control_PID = 0.0
    DutyCycle = round (control_PID * 100,3)
    pwm12.ChangeDutyCycle(DutyCycle) #Change duty cycle in function of the controller output
    time.sleep (ts) #Wait a sample time
    ControlPrev = control_PID #Assign the error variables
    ErrorPrev = Error
    ErrorPrev2 = ErrorPrev
    ControlPrev2 = ControlPrev