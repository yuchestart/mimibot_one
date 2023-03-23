#Import RPi.GPIO library
import RPi.GPIO as g
from time import sleep
from timeit import timeit

ENCODER_A = 18
ENCODER_B = 22
ENA = 7
IN1 = 12
IN2 = 13
SPEED_PWM = None
POSITION = 0
def setup():
    global ENCODER_A,ENCODER_B,ENA,IN1,IN2,SPEED_PWM
    g.setmode(g.BOARD)
    g.setup(ENCODER_A,g.IN)
    g.setup(ENCODER_B,g.IN)
    g.setup(ENA,g.OUT)
    g.setup(IN1,g.OUT)
    g.setup(IN2,g.OUT)
    SPEED_PWM = g.PWM(ENA,1000)
    SPEED_PWM.start(0)
    g.output(IN1,g.LOW)
    g.output(IN2,g.LOW)
    g.add_event_detect(ENCODER_A,g.RISING,callback=readEncoder)
def setMotor(speed,direction):
    global SPEED_PWM,IN1,IN2
    SPEED_PWM.ChangeDutyCycle(speed)
    if direction == "F":
        g.output(IN1,g.HIGH)
        g.output(IN2,g.LOW)
    elif direction == "B":
        g.output(IN1,g.LOW)
        g.output(IN2,g.HIGH)
    elif direction == "S":
        g.output(IN1,g.LOW)
        g.output(IN1,g.LOW)
def readEncoder(a):
    global ENCODER_B,POSITION
    encoderBValue = g.input(ENCODER_B)
    #Tune as needed
    if encoderBValue:
        POSITION-=1
    else:
        POSITION+=1
KP = 1
KD = 0
KI = 0
e = 0
preve = 0
t = 0
prevt = 0
target = 5
LPS = 1/30 # save resources
def pid_loop():
    global KP,KD,KI,e,preve,t,prevt,target
    pass
setup()
setMotor(100,"F")
try:
    while True:
        print(g.input(ENCODER_A),g.input(ENCODER_B),POSITION)
except KeyboardInterrupt:
    g.cleanup()