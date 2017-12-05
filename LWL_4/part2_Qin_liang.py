import numpy as np
import random
import math # math.floor
from collections import Counter # Count occurence
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Pongcontstate:
    def __init__(self,x=0.5,y=0.5,vx=0.03,vy=0.01,py=0.4,rd=0,end=False,bounce=0):
        if not end:
            self.bx = x
            self.by = y #position
            self.vx = vx
            self.vy = vy #velocity
            self.py = py #paddle position
            self.rd = rd
        else:
            self.bx = -1
            self.by = -1
            self.vx = -1
            self.vy = -1
            self.py = -1
            self.rd = -1
        self.bounce = bounce
        return

    def getCurrentFrame(self):
        fig = plt.figure()
        plt.plot([self.bx],[1-self.by],'ro',[1,1],[0.8-self.py,1-self.py],linewidth=5.0)
        plt.show()
        return

    def getDiscreteState(self):
        return Pongdiscstate(self.bx,self.by,self.vx,self.vy,self.py,self.rd)

    def hasfinished(self):
        if self.rd == -1:
            return True
        return False

    def nextstate(self,action):
        # action = {-1,0,1} = {up,stay,down}
        end = False
        new_bx = self.bx + self.vx
        new_by = self.by + self.vy
        new_vx = self.vx
        new_vy = self.vy
        new_bounce = self.bounce
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
            # Check whether bouncing onto panel
            cross = self.by + (1-self.bx)*self.vy/self.vx
            if cross < self.py or cross > self.py+0.2:
                end = True
            else:
                new_bounce += 1
                new_bx = 2-new_bx
                new_vx = min(-0.03,-new_vx + 0.03*random.random()-0.015)
                new_vy = new_vy + 0.06*random.random()-0.03
        # Action
        new_py = self.py + action*(0.04)
        if new_py > 0.8:
            new_py = 0.8
        elif new_py < 0:
            new_py = 0.0
        return Pongcontstate(new_bx,new_by,new_vx,new_vy,new_py,reward,end,new_bounce)

class Pongdiscstate:
    def __init__(self,bx,by,vx,vy,py,rd):
        if rd < 0:
            # End state
            self.bx = -1
            self.by = -1
            self.vx = -1
            self.vy = -1
            self.py = -1
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
    def hasfinished(self):
        return self.py < 0

def getindex(state):
    # type(state) = Pongdiscstate
    # action = {-1,0,1}
    if state.hasfinished():
        return 12*12*2*3*12    # bx*by*vx*vy*py
    else:
        raw_ind = [state.bx,state.by,(state.vx+1)//2,(state.vy+1),state.py]
        size = [12,12,2,3,12]
        ind = raw_ind[0]
        for i in range(1,5):
            ind = ind * size[i] + raw_ind[i]
        return ind
def fexplore(q,n):
    # For exploration purposes
    # Call w/ Q[ind,:].copy()
    Ne = 5
    for i in range(3):
        if n[i] < Ne:
            q[i] = 0.1
    return q
if __name__ == '__main__':
    # Train
    C = 10
    gamma = 0.9
    num_train = 100000
    Q = np.zeros((12*12*2*3*12+1,3))    # Action-utility
    N = np.zeros((12*12*2*3*12+1,3))    # State-action frequency
    for i in range(num_train):
        # Play game
        curr = Pongcontstate()
        curd = curr.getDiscreteState()
        ind = getindex(curd)
        while not curr.hasfinished():
            a = np.argmax(fexplore(Q[ind,:].copy(),N[ind,:]))-1   # {-1,0,1}
            # Get next state
            nexts = curr.nextstate(a)
            nextd = nexts.getDiscreteState()
            nextind = getindex(nextd)
            # Get current learning rate
            alpha = C/(C+N[ind,a+1])
            # TD update
            Q[ind,a+1] = Q[ind,a+1] + alpha*(curr.rd + gamma*max(Q[nextind,:]) - Q[ind,a+1])
            N[ind,a+1] = N[ind,a+1] + 1
            # Re-assign curr
            curr = nexts
            curd = nextd
            ind = nextind
        # end TD update
        Q[ind,a+1] = Q[ind,a+1] + alpha*(curr.rd - Q[ind,a+1])
        N[ind,a+1] = N[ind,a+1] + 1
        if i % 10000 == 0:
            print('Training Process: %d%%...' % (i//1000))
    #############################################
    print('Training Completed. Start testing...')
    # Test & Display
    num_test = 1000
    num_bounce = np.zeros(num_test)
    best = -1
    for t in range(num_test):
        curr = Pongcontstate()
        play = [curr]
        while not curr.hasfinished():
            curd = curr.getDiscreteState()
            a = np.argmax(Q[getindex(curd),:])-1
            curr = curr.nextstate(a)
            play.append(curr)
        num_bounce[t] = curr.bounce
        # Save best for display
        if curr.bounce > best:
            best = curr.bounce
            bestplay = play
        if t % 100 == 0:
            print('Testing Process: %d%%...' % (t//10))
    # Print average bouncing
    print('Testing Completed.')
    print('Counts for diff. number of bounces:',end='')
    print(Counter(num_bounce))
    print('The average number of bouncing is %f' % np.mean(num_bounce))
    # Draw best solution
    fig = plt.figure()
    ims = []
    for s in bestplay:
        ims.append(plt.plot([s.bx],[1-s.by],'ro',[1,1],[0.8-s.py,1-s.py],linewidth=6.0))
    im_ani = anim.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=False)
    plt.axis([0,1,0,1])
    plt.show()
