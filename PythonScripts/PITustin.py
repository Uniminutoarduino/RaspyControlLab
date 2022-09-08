#PI controller Tustin method
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
SetPoint = 20.0 #(Set point-reference)
kp = 200.0 #Proportional constant
ki = 0.01 #Integral constant
#error variables
Error = 0.0
controlpi = 0.0
DutyCycle = 0.0
ts = 0.6 #sampling time
ErrorSum = 0.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490) #GPIO 13 configuration, 490Hz
pwm13.start(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490) #GPIO 12 configuration, 490Hz
pwm12.start(0)
i2c = busio.I2C(board.SCL, board.SDA)
ts = 0.6 
ads = ADS.ADS1115(i2c) #ADS1115 configuration
chan = AnalogIn(ads, ADS.P0)
while True:
   Sensor = round(chan.voltage,3)
   Error = round ((SetPoint*0.0482)-Sensor,3)
   ErrorSum = ErrorSum + Error
   controlpi = round (Error * kp + ki * ErrorSum,3) #Control equation
   if (controlpi > 1.0): #Limitation(Antiwind-up)
       controlpi = 1.0
   if (DutyCycle < 0.0):
       DutyCycle = 0.0
   if (Error < 0.0):
       Error = 0.0
   if (controlpi < 0.0):
       controlpi = 0.0
   DutyCycle = round (controlpi * 100,3)
   pwm12.ChangeDutyCycle(DutyCycle) #Duty cycle according to controller output
   time.sleep (ts) #Wait a sampling time