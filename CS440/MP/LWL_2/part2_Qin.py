import numpy as np
import random
import copy

class Board:
    def __init__(self):
        # Parameters:config, remain, white, black
        config = np.zeros((8,8))   # Empty = 0
        config[0:2] = 2*np.ones((2,8))  # Black = 2
        config[6:8] = np.ones((2,8))    # White = 1
        self.config = config
        self.remain = np.array([16,16]) # [white,black]
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
                    return 2
            elif dir==2 and pos[0]>0 and pos[1]<7:
                if config[(pos[0]-1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]-1)]==2:
                    return 2
        elif config[pos] == 2:
            if dir==0 and pos[0]<7 and pos[1]<7:
                if config[(pos[0]+1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]+1)]==1:
                    return 2
            elif dir==1 and pos[0]<7:
                if config[(pos[0]+1,pos[1])]==0:
                    return 1
                elif config[(pos[0]+1,pos[1])]==1:
                    return 2
            elif dir==2 and pos[0]<7 and pos[1]>0:
                if config[(pos[0]+1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]-1)]==1:
                    return 2
        return 0

    def move(self,pos,dir):
        # NOT check whether can move
        if self.config[pos] == 0:
            print('Nothing to Move!')
            return
        elif self.config[pos] == 1:
            if dir==0:
                if self.config[(pos[0]-1,pos[1]-1)] == 2:
                    self.remain[1] -= 1
                    self.workers[1].remove((pos[0]-1,pos[1]-1))
                self.config[(pos[0]-1,pos[1]-1)] = 1
                self.workers[0].append((pos[0]-1,pos[1]-1))
            elif dir==1:
                self.config[(pos[0]-1,pos[1])] = 1
                self.workers[0].append((pos[0]-1,pos[1]))
            elif dir==2:
                if self.config[(pos[0]-1,pos[1]+1)] == 2:
                    self.remain[1] -= 1
                    self.workers[1].remove((pos[0]-1,pos[1]+1))
                self.workers[0].append((pos[0]-1,pos[1]+1))
                self.config[(pos[0]-1,pos[1]+1)] = 1
            self.workers[0].remove(pos)

        elif self.config[pos] == 2:
            if dir==0:
                if self.config[(pos[0]+1,pos[1]+1)] == 1:
                    self.remain[0] -= 1
                    self.workers[0].remove((pos[0]+1,pos[1]+1))
                self.config[(pos[0]+1,pos[1]+1)] = 2
                self.workers[1].append((pos[0]+1,pos[1]+1))
            elif dir==1:
                self.config[(pos[0]+1,pos[1])] = 2
                self.workers[1].append((pos[0]+1,pos[1]))
            elif dir==2:
                if self.config[(pos[0]+1,pos[1]-1)] == 1:
                    self.remain[0] -= 1
                    self.workers[0].remove((pos[0]+1,pos[1]-1))
                self.config[(pos[0]+1,pos[1]-1)] 	= 2
                self.workers[1].append((pos[0]+1,pos[1]-1))
            self.workers[1].remove(pos)
        self.config[pos] = 0
        return

    # Heuristics
    def dh1(self,color):
        return 2*self.remain[color-1] + random.random()
    def oh1(self,color):
        return 2*(30-self.remain[2-color]) + random.random()

# Search Strategies
def minmax(board,depth,color,Max=True):
    if depth==0 or board.hasfinished():
        return (board.dh1(color),())
    if Max:
      strategy = ((-1,-1),-1) #White
      value = float('-inf')
      for w in board.workers[color-1]:
        for dir in range(3):
          if board.canMove(w,dir):
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax(newboard,depth-1,color,False)
            curval=temp[0]
            if value < curval:
              value = curval
              strategy = (w,dir)
    else:  # Black
      strategy = ((-1,-1),-1)
      value=float('inf')
      for w in board.workers[2-color]:
        for dir in range(3):
          if board.canMove(w,dir):
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax(newboard,depth-1,color,True)
            curval=temp[0]
            if value > curval:
              value = curval
              strategy = (w,dir)
    return (value,strategy)


# Search Strategies
def minmax2(board,depth,color,Max=True):
    if depth==0 or board.hasfinished():
        return (board.oh1(color),())
    if Max:
      strategy = ((-1,-1),-1) #White
      value = float('-inf')
      for w in board.workers[color-1]:
        for dir in range(3):
          if board.canMove(w,dir):
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax2(newboard,depth-1,color,False)
            curval=temp[0]
            
            if value < curval:
              value = curval
              strategy = (w,dir)
    else:  # Black
      strategy = ((-1,-1),-1)
      value=float('inf')
      for w in board.workers[2-color]:
        for dir in range(3):
          if board.canMove(w,dir):
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax2(newboard,depth-1,color,True)
            curval=temp[0]
            
            if value > curval:
              value = curval
              strategy = (w,dir)
    return (value,strategy)
    

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

def play(board):
    while 1:
        s=minmax(board,3,2)[1]
        board.printboard()
        board.move(s[0],s[1])
        if board.hasfinished()== 2:
            print("black wins")
            break
        s=minmax2(board,3,1)[1]
        board.printboard()
        board.move(s[0],s[1])
        if board.hasfinished()== 1:
            print("white wins")
            break
    board.printboard()











b = Board()
play(b)
print(b.dh1(1))
print(b.oh1(2))
