import RPi.GPIO as g
from time import sleep
import time
def readEncoderA(x):
    global A,B,E1B,speeds,times
    e = g.input(E1B)
    if e:
        A+=1
    else:
        A-=1
    speeds["A"] = 1/times["A"]
    times["A"] = time.time()
    print(A,B)
def readEncoderB(x):
    global A,B,E2B,speeds,times
    e = g.input(E2B)
    if e:
        B+=1
    else:
        B-=1
    speeds["A"] = 1/times["A"]
    times["B"] = time.time()
    print(A,B)
g.setmode(g.BOARD)
A = 0
B = 0
E1A = 18
E1B = 22
E2A = 29
E2B = 31
times = {
    "A":time.time(),
    "B":time.time()
}
speeds = {
    "A":0,
    "B":0
}
g.setup(E1A,g.IN)
g.setup(E1B,g.IN)
g.setup(E2A,g.IN)
g.setup(E2B,g.IN)
g.add_event_detect(E1A,g.RISING,callback=readEncoderA)
g.add_event_detect(E2A,g.RISING,callback=readEncoderB)
try:
    while True:
        print(speeds["A"]/343,speeds["B"]/343)
except KeyboardInterrupt:
    g.cleanup()