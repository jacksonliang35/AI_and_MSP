import random
import math # math.floor
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Pongcontstate:
    def __init__(self,x=0.5,y=0.5,vx=0.03,vy=0.01,py=0.4,rd=0,end=False):
        if not end:
            self.bx = x
            self.by = y #position
            self.vx = vx
            self.vy = vy #velocity
            self.py = py #paddle position
            self.reward = rd
        else:
            self.bx = -1
            self.by = -1
            self.vx = -1
            self.vy = -1
            self.py = -1
            self.reward = -1
        return

    def display(self):
        plt.hold(True)
        plt.plot([self.bx],[1-self.by],'ro')
        plt.plot([1,1],[0.8-self.py,1-self.py],linewidth=8.0)
        plt.axis([0,1,0,1])
        plt.show()
        plt.hold(False)

    def getDiscreteState(self):
        return Pongdiscstate(self.bx,self.by,self.vx,self.vy,self.py,self.reward)

    def hasfinished(self):
        if self.reward == -1:
            return True
        return False

    def nextstate(self,action):
        # action = {-1,0,1}
        end = False
        new_bx = self.bx + self.vx
        new_by = self.by + self.vy
        new_vx = self.vx
        new_vy = self.vy
        reward = 0
        # Bounce
        if new_by < 0:
            new_by = -new_by
            new_vy = -new_vy
        if new_bx < 0:
            new_bx = -new_bx
            new_vx = -new_vx
            reward = 1
        if new_by > 1:
            new_by = 2-new_by
            new_vy = -new_vy
        if new_bx > 1:
            # Check whether crossing panel
            cross = self.by + (1-self.bx)*self.vy/self.vx
            if cross < self.py or cross > self.py+0.2:
                end = True
            new_bx = 2-new_bx
            new_vx = min(-0.03,-new_vx + 0.03*random.random()-0.015)
            new_vy = new_vy + 0.06*random.random()-0.03
        # Action
        new_py = self.py + action*(0.04)
        if new_py > 0.8:
            new_py = 0.8
        elif new_py < 0:
            new_py = 0.0
        return Pongcontstate(new_bx,new_by,new_vx,new_vy,new_py,reward,end)

class Pongdiscstate:
    def __init__(self,bx,by,vx,vy,py,rd):
        if rd < 0:
            # End state
            self.bx = -1
            self.by = -1
            self.vx = -1
            self.vy = -1
            self.py = -1
            self.reward = -1
        else:
            # discretize ball position
            if bx >= 1:
                self.bx = 11
            else:
                self.bx = math.floor(12*bx)
            if by >= 1:
                self.by = 11
            else:
                self.by = math.floor(12*by)
            # velocity_x
            if vx>0:
                self.vx = 1
            else:
                self.vx = -1
            # velocity_y
            if vy >= 0.015:
                self.vy = 1
            elif vy <= -0.015:
                self.vy = -1
            else:
                self.vy = 0
            # discretize pannel_y
            if py >= 0.8:
                self.py = 11
            else:
                self.py = math.floor(12 * py / 0.8)
            return
            # reward
            self.reward = rd

if __name__ == '__main__':
    test = Pongcontstate()
    test.display()
