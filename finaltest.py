# FINAL REVISION BEFORE PORT TO ROS
import RPi.GPIO as g
import time as t
class Driver:
    def __init__(self,v1,v2,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
        g.setmode(g.BOARD)
        g.setup(v1,g.OUT)
        g.setup(v2,g.OUT)
        g.setup(in1,g.OUT)
        g.setup(in2,g.OUT)
        g.setup(in3,g.OUT)
        g.setup(in4,g.OUT)
        g.setup(e1a,g.IN)
        g.setup(e1b,g.IN)
        g.setup(e2a,g.IN)
        g.setup(e2b,g.IN)
        g.add_event_detect(e1a,g.RISING,callback=self.readEncoderA)
        g.add_event_detect(e2a,g.RISING,callback=self.readEncoderB)
        self.pins = {
            "v1":v1,
            "v2":v2,
            "in1":in1,
            "in2":in2,
            "in3":in3,
            "in4":in4,
            "e1a":e1a,
            "e1b":e1b,
            "e2a":e2a,
            "e2b":e2b
        }
        self.pwm = {
            "a":g.PWM(v1,1000),
            "b":g.PWM(v2,1000)
        }
        self.speed = {
            "a":0,
            "b":0
        }
        self.encoderPositions = {
            "a":0,
            "b":0
        }
        self.lastTimePerEncoder = {
            "a":t.time(),
            "b":t.time()
        }
        self.encoderSpeeds = {
            "a":0,
            "b":0
        }
        self.running = False
        self.pwm["a"].start(0)
        self.pwm["b"].start(0)
    def setMotor(self,speedA,speedB):
        requested = {
            "a":speedA,
            "b":speedB
        }
        for motor in range(self.speed):
            self.speed = requested[motor]
            self.pwm[motor].ChangeDutyCycle(abs(requested[motor]))
            if requested[motor] < 0:
                if motor == "a":
                    g.output(self.pins['in1'],g.LOW)
                    g.output(self.pins['in2'],g.HIGH)
                else:
                    g.output(self.pins['in3'],g.LOW)
                    g.output(self.pins['in4'],g.HIGH)
            else:
                if motor == "a":
                    g.output(self.pins['in2'],g.LOW)
                    g.output(self.pins['in1'],g.HIGH)
                else:
                    g.output(self.pins['in4'],g.LOW)
                    g.output(self.pins['in3'],g.HIGH)
    def readEncoderA(self,n=None):
        encoderBValue = g.input(self.pins["e1b"])
        if encoderBValue:
            self.encoderPositions["a"]+=1
        else:
            self.encoderPositions["a"]-=1
        self.encoderSpeeds["a"] = 1/self.lastTimePerEncoder["a"]
        self.lastTimePerEncoder["a"] = t.time()
    def readEncoderB(self,n=None):
        encoderBValue = g.input(self.pins["e2b"])
        if encoderBValue:
            self.encoderPositions["b"]+=1
        else:
            self.encoderPositions["b"]-=1
        self.encoderSpeeds["b"] = 1/self.lastTimePerEncoder["a"]
        self.lastTimePerEncoder["b"] = t.time()
    def pidLoop(self):
        t.sleep()
        if self.running:
            self.pidLoop() 
    
