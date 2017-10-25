import numpy as np
import random
import copy

class Board:
    def __init__(self):
        # Parameters:config, workers
        config = np.zeros((8,8))   # Empty = 0
        config[0:2] = 2*np.ones((2,8))  # Black = 2
        config[6:8] = np.ones((2,8))    # White = 1
        self.config = config
        self.workers = []
        white = []
        black = []
        for i in range(8):
            white.append((6,i))
            white.append((7,i))
            black.append((0,i))
            black.append((1,i))
        self.workers = [white,black]

    def hasfinished(self):
        # Returns {0, 1, 2} = {not finished, white wins, black wins}
        if len(self.workers[0]) == 0:
            return 2
        if len(self.workers[1]) == 0:
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

    def canMove(self,pos,dir):
        return canMove(self.config,pos,dir)

    def move(self,pos,dir):
        move(self.config,self.workers,pos,dir)


    # Heuristics
    def dh1(self,color):
        return 2*len(self.workers[color-1]) + random.random()
    def oh1(self,color):
        return 2*(30-len(self.workers[2-color])) + random.random()

    # Search Strategies
    def minmax(self,config,workers,depth,color,Max):
        # workers is a deep copy of self.workers
        # config is a deep copy of self.config
    	if depth==0 or self.hasfinished():
    		return self.oh1(color)

    	if Max:
            strategy = ((-1,-1),-1)
    		value = float('-inf')
    		for w in workers[color-1]:
                for dir in range(3):
                    if self.canMove(w,dir)==1:
                        
            			curval=minmax(depth-1,newboard,color,False)
            			if value < curval:
                            value = curval
                            strategy = (w,dir)
    		return strategy
    	else:
            strategy = ((-1,-1),-1)
    		value=float('inf')
    		for w in workers[2-color]:
                for dir in range(3):
                    if board.canMove(w,dir):
                        newboard = copy.deepcopy(board)
                        newboard.move(w,dir)
            			curval=minmax(depth-1,newboard,True)
            			if value > curval:
                            value = curval
                            strategy = (w,dir)
    		return strategy

    def abpruning(self,depth,board,a,b,Max):    #a=neginf b=posinf
    	if depth==0 or board.hasfinished():
    		return board.oh1(self.color)
    	if Max:
    		for w in node.child:
    			curval=abpruning(child,depth-1,a,b,False)
    			a=max(a,curval)
    			if a >= b:
    				break
    		return a
    	else:
    		for child in node.child:
    			curval=abpruning(child,depth-1,a,b,True)
    			b=min(b,curval)
    			if a >= b:
    				break
    		return b

def canMove(config,pos,dir):
    # dir = {0,1,2} = {forward left, forward, forward right}
    # return {0,1,2} = {cannot move, can move no capture, can move with capture}
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
                return 0
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
                return 0
        elif dir==2 and pos[0]<7 and pos[1]>0:
            if config[(pos[0]+1,pos[1]-1)]==0:
                return 1
            elif config[(pos[0]+1,pos[1]-1)]==2:
                return 2
    return 0

def move(config,workers,pos,dir):
    # NOT check whether can move
    if self.config[pos] == 0:
        print('Nothing to Move!')
        return
    elif self.config[pos] == 1:
        if dir==0:
            if self.config[(pos[0]-1,pos[1]-1)] = 2:
                self.workers[1].remove((pos[0]-1,pos[1]-1))
            self.config[(pos[0]-1,pos[1]-1)] = 1
            self.workers[0].append((pos[0]-1,pos[1]-1))
        elif dir==1:
            self.config[(pos[0]-1,pos[1])] = 1
            self.workers[0].append((pos[0]-1,pos[1]))
        elif dir==2:
            if self.config[(pos[0]-1,pos[1]+1)] = 2:
                self.workers[1].remove((pos[0]-1,pos[1]+1))
            self.workers[0].append((pos[0]-1,pos[1]+1))
            self.config[(pos[0]-1,pos[1]+1)] = 1
        self.workers[0].remove(pos)

    elif self.config[pos] == 2:
        if dir==0:
            if self.config[(pos[0]+1,pos[1]+1)] = 1:
                self.workers[0].remove((pos[0]+1,pos[1]+1))
            self.config[(pos[0]+1,pos[1]+1)] = 2
            self.workers[1].append((pos[0]+1,pos[1]+1))
        elif dir==1:
            self.config[(pos[0]+1,pos[1])] = 2
            self.workers[1].append((pos[0]+1,pos[1]))
        elif dir==2:
            if self.config[(pos[0]+1,pos[1]-1)] = 1:
                self.workers[0].remove((pos[0]+1,pos[1]-1))
            self.config[(pos[0]+1,pos[1]-1)] 	= 2
            self.workers[1].append((pos[0]+1,pos[1]-1))
        self.workers[1].remove(pos)
    self.config[pos] = 0





b = Board()
print(b.dh1(1))
print(b.oh1(2))
