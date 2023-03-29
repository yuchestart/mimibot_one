import RPi.GPIO as g
import time as t
class Controller:
    def __init__(self,v1,v2,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
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
        self.pwm = {
            "A":g.PWM(v1,1000),
            "B":g.PWM(v2,1000)
        }
        self.encoders = {
            "position":{
                "A":0,
                "B":0,
            },
            "speed":{
                "A":0,
                "B":0
            },
            "times":{
                "A":t.time(),
                "B":t.time()
            }
        }
        self.prevT = t.time()
        self.integral = 0
        self.KP = 0.5
        self.KI = 0.3
        self.pwm["A"].start(0)
        self.pwm["B"].start(0)
        self.scan = None
        self.running = False
        g.add_event_detect(e1a,g.RISING,callback=self.readEncoderA)
        g.add_event_detect(e2a,g.RISING,callback=self.readEncoderB)
    def readEncoderA(self,x):
        e = g.input(self.pins["e1b"])
        if e:
            self.encoders["position"]["A"]+=1
        else:
            self.encoders["position"]["A"]-=1
        current = t.time()
        self.encoders["speed"]["A"] = round(1/current-self.encoders["times"]["A"]*100)/100
        self.encoders["times"]["A"] = current
    def readEncoderB(self,x):
        e = g.input(self.pins["e2b"])
        if e:
            self.encoders["position"]["B"]+=1
        else:
            self.encoders["position"]["B"]-=1
        current = t.time()
        self.encoders["speed"]["B"] = round(1/current-self.encoders["times"]["B"]*100)/100
        self.encoders["times"]["B"] = current
    def driver_loop(self):
        if self.running:
            setpoints = {
            "A":1,
            "B":1
            }
            for motor in ["A","B"]:
                if self.encoders["speed"][motor] == 0:
                    self.pwm[motor].ChangeDutyCycle(0)
                else:
                    e = setpoints[motor]-self.encoders["speed"][motor]
                    newtime = t.time()
                    deltaTime = newtime - self.prevT
                    self.prevT = newtime
                    self.integral = self.integral + e*deltaTime
                    u = self.KP*e + self.KI*self.integral
                    if(u<0):
                        if motor == "A":
                            g.output(self.pins["in1"],g.LOW)
                            g.output(self.pins["in2"],g.HIGH)
                        else:
                            g.output(self.pins["in3"],g.LOW)
                            g.output(self.pins["in4"],g.LOW)
                    else:
                        if motor == "A":
                            g.output(self.pins["in1"],g.LOW)
                            g.output(self.pins["in2"],g.HIGH)
                        else:
                            g.output(self.pins["in3"],g.LOW)
                            g.output(self.pins["in4"],g.LOW)
                    pwr = int(abs(u))
                    if pwr > 100:
                        pwr = 100
                    self.pwm[motor].ChangeDutyCycle(pwr)