#Code to empty main tank (T1)
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
Sensor = 0.0 #variable to get the sensor value
GPIO.setmode(GPIO.BCM) 
GPIO.setup(12,GPIO.OUT)
pwm12=GPIO.PWM(12,490) #GPIO 12 for PWM, f=490Hz (T2 motor pump)
pwm12.start(0)
GPIO.setup(13,GPIO.OUT)
pwm13=GPIO.PWM(13,490) #GPIO 13 for PWM, f=490Hz (T1 motor pump)
pwm13.start(0)
i2c = busio.I2C(board.SCL, board.SDA) #I2C configuration for ADS1115
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)
while True:
    Sensor = round(chan.voltage,3) #Reading sensor value
    print (str(Sensor))
    if(Sensor<=0.01): #If sensor value <0.01 stop T1 motor pump.
        pwm13.ChangeDutyCycle(0)
        pwm12.ChangeDutyCycle(0)
    else:
        pwm13.ChangeDutyCycle(100)
        pwm12.ChangeDutyCycle(0)
    time.sleep(0.5)      
