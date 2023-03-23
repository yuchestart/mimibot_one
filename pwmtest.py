import RPi.GPIO as g
from time import sleep
g.setmode(g.BOARD)
g.setup(40,g.OUT)
pwm = g.PWM(40,100)
pwm.start(50)
val = 0
dir = 1
try:
    while True:
        if dir:
            val+=1
        else:
            val-=1
        if(val < 0):
            val = 0
            dir = 1
        elif val>100:
            val=100
            dir=0
        pwm.ChangeDutyCycle(val)
        sleep(0.01)
except KeyboardInterrupt:
    g.cleanup()