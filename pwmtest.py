#define global variables
ENA = 12
IN1 = 11
IN2 = 13
import RPi.GPIO as g
g.setmode(g.BOARD)
g.setup(ENA,g.OUT)
g.setup(IN1,g.OUT)
g.setup(IN2,g.OUT)
pwm = g.PWM(ENA,1000)
pwm.start(25)
speed = 25
g.output(IN1,g.LOW)
g.output(IN2,g.LOW)

while True:
    command = input().split()
    if(command[0] == "o"):
        pwm.ChangeDutyCycle(int(command[1]))
        speed = 25
    elif(command[0] == "f"):
        pwm.ChangeDutyCycle(speed)
        g.output(IN1,g.HIGH)
        g.output(IN2,g.LOW)
    elif(command[0] == "b"):
        pwm.ChangeDutyCycle(speed)
        g.output(IN2,g.HIGH)
        g.output(IN1,g.LOW)
    elif(command[0] == "h"):
        pwm.ChangeDutyCycle(0)
    elif(command[0] == "e"):
        g.cleanup()
        exit()
