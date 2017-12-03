import random

class Pongcontstate:
    def __init__(self,x=0.5,y=0.5,vx=0.03,vy=0.01,py=0.4,rd=0,end=False):
        if not end:
            self.ball_x = x
            self.ball_y = y #position
            self.velocity_x = vx
            self.velocity_y = vy #velocity
            self.paddle_y = py #paddle position
            self.reward = rd
        else:
            self.ball_x = -1
            self.ball_y = -1
            self.velocity_x = -1
            self.velocity_y = -1
            self.paddle_y = -1
            self.reward = -1
        return
    '''
    def printstate(self):
    	idx = np.zeros((12,12))#12*12 grid
    	img = []
    	for i in range(idx.shape[0]):
    		img.append([])
    		for j in range(idx.shape[1]):
    			if idx[i,j]==1:
    				img[i].append("a") # if have paddle or ball print
    			else:
    				img[i].append(" ") #background
    		img[i].append("\n")
        for line in img:
            print(''.join(line))
        return
    '''
    def getDiscreteState(self):
        return Pongdiscstate(self.ball_x,self.ball_y,self.velocity_x,self.velocity_y,self.paddle_y,self.reward)

    def hasfinished(self):
        if

    def nextstate(self,action):
        # action = {-1,0,1}
        end = False
        new_ball_x = self.ball_x + self.velocity_x
        new_ball_y = self.ball_y + self.velocity_y
        new_velocity_x = self.velocity_x
        new_velocity_y = self.velocity_y
        # Bounce
        if new_ball_y < 0:
            new_ball_y = -new_ball_y
            new_velocity_y = -new_velocity_y
        if self.ball_x < 0:
            new_ball_x = -new_ball_x
            new_velocity_x = -new_velocity_x
            reward = 1
        if self.ball_y > 1:
            new_ball_y = 2-new_ball_y
            new_velocity_y = -new_velocity_y
        if self.ball_x > 1:
            # Check whether crossing panel
            if CROSS:
                end = True
            new_ball_x = 2-new_ball_x
            new_velocity_x = min(-0.03,-new_velocity_x + 0.03*random.random()-0.015)
            new_velocity_y = new_velocity_y + 0.06*random.random()-0.03
        # Action
        new_paddle_y = action*(0.04)
        return Pongcontstate(new_ball_x,new_ball_y,new_velocity_x,new_velocity_y,new_paddle_y,reward,end)
class Pongdiscstate:
    def __init__(self,bx,by,vx,vy,py,rd):
        # TODO
