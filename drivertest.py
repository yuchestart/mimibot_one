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
        SPEED[motor] = requested[motor]
        PWM[motor].ChangeDutyCycle(abs(requested[motor]))
        if requested[motor] < 0:
            if motor == "a":
                g.output(PINS["in1"],g.LOW)
                g.output(PINS["in2"],g.HIGH)
            else:
                g.output(PINS["in3"],g.LOW)
                g.output(PINS["in4"],g.HIGH)
        else:
            if motor == "a":
                g.output(PINS["in2"],g.LOW)
                g.output(PINS["in1"],g.HIGH)
            else:
                g.output(PINS["in4"],g.LOW)
                g.output(PINS["in3"],g.HIGH)
            
    print("Set Motor A speed to:",SPEED['a'],"Set Motor B speed to:",SPEED["b"])

setup(7,11,12,13,15,16,18,22,29,31)
setMotor(50,50)
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    g.cleanup()
