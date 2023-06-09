import RPi.GPIO as g
import time as t
g.setmode(g.BCM)
def readEncoderA(x):
    global A,B,E1B,speeds,times
    e = g.input(E1B)
    if e:
        A+=1
    else:
        A-=1
    speeds["A"] = round(1/(t.time()-times["A"])*100)/100
    times["A"] = t.time()
def readEncoderB(x):
    global A,B,E2B,speeds,times
    e = g.input(E2B)
    if e:
        B+=1
    else:
        B-=1
    speeds["B"] = round(1/(t.time()-times["B"])*100)/100
    times["B"] = t.time()
def pidLoop():
    global VA,VB,IN1,IN2,IN3,IN4,setpoints,speeds,pwms,prevT,KP,KI,INTEGRAL
    for motor in ["A","B"]:
        if setpoints[motor] == 0:
            pwms[motor].ChangeDutyCycle(0)
        else:
            e = setpoints[motor]-speeds[motor]
            newtime = t.time()
            deltaTime = newtime - prevT
            prevT = newtime
            INTEGRAL = INTEGRAL + e*deltaTime
            u = KP*e + KI*INTEGRAL
            if(u<0):
                if motor == "A":
                    g.output(IN1,g.LOW)
                    g.output(IN2,g.HIGH)
                else:
                    g.output(IN3,g.LOW)
                    g.output(IN4,g.HIGH)
            else:
                if motor == "A":
                    g.output(IN2,g.LOW)
                    g.output(IN1,g.HIGH)
                else:
                    g.output(IN4,g.LOW)
                    g.output(IN3,g.HIGH)
            pwr = int(abs(u))
            if pwr > 100:
                pwr = 100
            pwms[motor].ChangeDutyCycle(pwr)
    print(speeds["A"],speeds["B"])
INTEGRAL = 0  
prevT = t.time()
A = 0
B = 0
KP = 15
KI = 4
E1A = 24#18
E1B = 25#22
E2A = 5##29
E2B = 6##31
VA = 4#7
VB = 17#11
IN1 = 18#12
IN2 = 27#13
IN3 = 22#15
IN4 =23# 16
g.setup(E1A,g.IN)
g.setup(E1B,g.IN)
g.setup(E2A,g.IN)
g.setup(E2B,g.IN)
g.setup(VA,g.OUT)
g.setup(VB,g.OUT)
g.setup(IN1,g.OUT)
g.setup(IN2,g.OUT)
g.setup(IN3,g.OUT)
g.setup(IN4,g.OUT)
g.output(IN1,g.HIGH)
g.output(IN2,g.LOW)
g.output(IN3,g.HIGH)
g.output(IN4,g.LOW)
setpoints ={
    "A":1,
    "B":1
}

times = {
    "A":t.time(),
    "B":t.time()
}
speeds = {
    "A":0,
    "B":0
}
pwms = {
    "A":g.PWM(VA,1000),
    "B":g.PWM(VB,1000)
}
pwms["A"].start(0)
pwms["B"].start(0)
g.add_event_detect(E1A,g.RISING,callback=readEncoderA)
g.add_event_detect(E2A,g.RISING,callback=readEncoderB)
t.sleep(3)
try:
    while True:
        pidLoop()
except KeyboardInterrupt:
    g.cleanup()