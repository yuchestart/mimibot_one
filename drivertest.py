import RPi.GPIO as g
from time import sleep
PINS = {}
PWM = {}
SPEED = {
    "a":0,
    "b":0,
}
def setup(ena,enb,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
    global PINS,PWM
    g.setmode(g.BOARD)
    g.setup(ena,g.OUT)
    g.setup(enb,g.OUT)
    g.setup(in1,g.OUT)
    g.setup(in2,g.OUT)
    g.setup(in3,g.OUT)
    g.setup(in4,g.OUT)
    g.setup(e1a,g.IN)
    g.setup(e1b,g.IN)
    g.setup(e2a,g.IN)
    g.setup(e2b,g.IN)
    PINS["ena"] = ena,
    PINS["ena"] = enb,
    PINS["in1"] = in1,
    PINS["in2"] = in2,
    PINS["in3"] = in3,
    PINS["in4"] = in4,
    PINS["e1a"] = e1a,
    PINS["e2a"] = e2a,
    PINS["e1b"] = e1b,
    PINS["e2b"] = e2b,
    PWM["a"] = g.PWM(ena,1000)
    PWM["b"] = g.PWM(enb,1000)
    PWM["a"].start(0)
    PWM["b"].start(0)

def setMotor(speedA,speedB):
    global SPEED,PWM,PINS
    requested = {
        "a":speedA,
        "b":speedB
    }
    pins = {
        "a":[PINS["in1"],PINS["in2"]],
        "b":[PINS["in3"],PINS["in4"]]
    }
    for motor in SPEED:
        if requested[motor] > 0 and SPEED[motor] < 0 or requested[motor] < 0 and SPEED[motor] > 0:
            PWM[motor].ChangeDutyCycle(0)
            SPEED[motor] = requested[motor]
            if requested[motor] > 0:
                g.output(pins[motor][0],g.HIGH)
                g.output(pins[motor][1],g.LOW)
            else:
                g.output(pins[motor][0],g.LOW)
                g.output(pins[motor][1],g.HIGH)
            sleep(0.05)
            PWM[motor].ChangeDutyCycle(SPEED[motor])
        elif requested[motor] == 0:
            SPEED[motor] = 0
            g.output(pins[motor][0],g.LOW)
            g.output(pins[motor][1],g.LOW)
            PWM[motor].ChangeDutyCycle(0)
        else:
            SPEED[motor] = requested[motor]
            if requested[motor] > 0:
                g.output(pins[motor][0],g.HIGH)
                g.output(pins[motor][1],g.LOW)
            else:
                g.output(pins[motor][0],g.LOW)
                g.output(pins[motor][1],g.HIGH)
            PWM[motor].ChangeDutyCycle(SPEED[motor])
    print("Set Motor A speed to:",SPEED['a'],"Set Motor B speed to:",SPEED["b"])

setup(7,11,12,13,15,16,18,22,29,31)
setMotor(50,50)
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    g.cleanup()
