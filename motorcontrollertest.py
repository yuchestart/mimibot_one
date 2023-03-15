#Import RPi.GPIO library
import RPi.GPIO as g

#Initiate Drivetrain class
class Drivetrain():
    def __init__(self,spdA,spdB,fwd1,bkd1,fwd2,bkd2):
        #Set pin references
        self.sA = spdA
        self.sB = spdB
        self.fA = fwd1
        self.bA = bkd1
        self.fB = fwd2
        self.bB = bkd2
        #Setup GPIO
        g.setmode(g.BOARD)
        g.setup(self.sA,g.OUT)
        g.setup(self.fA,g.OUT)
        g.setup(self.bA,g.OUT)
        g.setup(self.sB,g.OUT)
        g.setup(self.fB,g.OUT)
        g.setup(self.bB,g.OUT)
        #Setup PWM cycles
        self.pA = g.PWM(self.sA,1000)
        self.pB = g.PWM(self.sB,1000)
        self.pA.start(0)
        self.pB.start(0)
        #Setup directions
        g.output(self.fA,g.LOW)
        g.output(self.fB,g.LOW)
        g.output(self.bA,g.LOW)
        g.output(self.bB,g.LOW)
        #Setup user settings
        self.speed = 0 #Speed to travel at in r/s
        self.steeringAngle = 0 #Angle to steer at in d/s
        self.direction = True # True for forwards
        self.moving = False
    def stop(self):
        self.moving = False
    def start(self):
        self.moving = True
    def setSpeed(self,speed):
        if(speed<0):
            self.speed = abs(speed)
            self.direction = not self.direction
        else:
            self.speed = abs(speed)
    def steer(self,steeringAngle):
        self.steeringAngle = steeringAngle
    def update(self):
        if(self.moving):
            pass
    

def main(args=None):
    pass

if __name__ == "__main__":
    try:
        #Mainloop
        while(True):
            main()
    except KeyboardInterrupt:
        #Cleanup GPIO to prevent any unwanted problems
        g.cleanup()