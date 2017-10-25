import numpy as np
import random

class Board:
    def __init__(self):
        # Parameters: height, width, config, remain
        self.height = 8
        self.width = 8
        config = np.zeros((8,8))   # Empty = 0
        config[0:2] = 2*np.ones((2,8))  # Black = 2
        config[6:8] = np.ones((2,8))    # White = 1
        self.config = config
        self.remain = np.array([16,16]) # [white,black]

    def hasfinished(self):
        # Returns {0, 1, 2} = {not finished, white wins, black wins}
        if self.remain[0] == 0:
            return 2
        if self.remain[1] == 0:
            return 1
        for i in range(8):
            if self.config[0,i]==1:
                return 1
            if self.config[7,i]==2:
                return 2
        return 0

    def printboard(self):
        # Print the board
        for i in range(8):
            b = []
            for j in range(8):
                if self.config[i,j] == 0:
                    b += ['_']
                elif self.config[i,j] == 1:
                    b += ['w']
                elif self.config[i,j] == 2:
                    b += ['b']
            print(''.join(b))
        print()

    def move(self,i,j,dir):
        return


    def canMove(self,pos,dir):
        # dir = {0,1,2} = {forward left, forward, forward right}
        # return {0,1,2} = {cannot move, can move no capture, can move with capture}
        config = self.config
        if config[pos] == 0:
            print('Position is empty!')
            return 0
        if config[pos] == 1:
            if dir==0 and pos[0]>0 and pos[1]>0:
                if config[(pos[0]-1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]-1)]==2:
                    return 2
            elif dir==1 and pos[0]>0:
                if config[(pos[0]-1,pos[1])]==0:
                    return 1
                elif config[(pos[0]-1,pos[1])]==2:
                    return -1
            elif dir==2 and pos[0]>0 and pos[1]<7:
                if config[(pos[0]-1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]-1)]==2:
                    return 2
        elif config[pos] == 2:
            if dir==0 and pos[0]<7 and pos[1]<7:
                if config[(pos[0]+1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]+1)]==2:
                    return 2
            elif dir==1 and pos[0]<7:
                if config[(pos[0]+1,pos[1])]==0:
                    return 1
                elif config[(pos[0]+1,pos[1])]==2:
                    return -1
            elif dir==2 and pos[0]<7 and pos[1]>0:
                if config[(pos[0]+1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]-1)]==2:
                    return 2
        return 0

    def move(self,pos,dir):
        # NOT check whether can move
        if self.config[pos] == 0:
            print('Nothing to Move!')
            return
        elif self.config[pos] == 1:
            if dir==0:
                self.config[(pos[0]-1,pos[1]-1)] = 1
            elif dir==1:
                self.config[(pos[0]-1,pos[1])] = 1
            elif dir==2:
                self.config[(pos[0]-1,pos[1]+1)] = 1
        elif self.config[pos] == 2:
            if dir==0:
                self.config[(pos[0]+1,pos[1]+1)] = 2
            elif dir==1:
                self.config[(pos[0]+1,pos[1])] = 2
            elif dir==2:
                self.config[(pos[0]+1,pos[1]-1)] = 2
        self.config[pos] = 0

    def dh1(self,color):
        return 2*self.remain[color-1] + random.random()

    def oh1(self,color):
        return 2*(30-self.remain[2-color]) + random.random()

class Player:
    def __init__(self,color):
        # Parameters: color = {1,2} = {white, black}, workers
        self.color = color
        self.workers = []
        if color == 1:
            for i in range(8):
                self.workers.append((6,i))
                self.workers.append((7,i))
        elif color == 2:
            for i in range(8):
                self.workers.append((0,i))
                self.workers.append((1,i))

    def dh1(self,board):
        return board.dh1(color)
    def oh1(self,board):
        return board.oh1(color)

b = Board()
print(b.dh1(1))
print(b.oh1(2))
