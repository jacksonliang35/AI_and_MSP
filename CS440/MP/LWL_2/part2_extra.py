import numpy as np
import random
import copy
import time
current_pos=(0,0)

class count:
    def __init__(self):
        self.count = 0
        self.time = 0
        self.step = 0
    def inc(self):
        self.count += 1
    def tinc(self,start,end):
        self.time += (end - start)
    def sinc(self):
        self.step += 1

class Board:
    def __init__(self):
        # Parameters:config, white, black
        config = np.zeros((5,10))   # Empty = 0
        config[0:2] = 2*np.ones((2,10))  # Black = 2
        config[3:5] = np.ones((2,10))    # White = 1
        self.config = config
        self.workers = []
        white = []
        black = []
        for i in range(10):
            white.append((3,i))
            white.append((4,i))
            black.append((0,i))
            black.append((1,i))
        self.workers = [white,black]
        return

    def readboard(self,filename):
        self.config = np.zeros((5,10))
        white = []
        black = []
        temp = []
        with open(filename,"r") as fp:
            for line in fp:
                temp.append(list(line))
        fp.close()
        for i in range(5):
            for j in range(10):
                if temp[i][j] == '_':
                    self.config[(i,j)] = 0
                elif temp[i][j] == 'b':
                    self.config[(i,j)] = 2
                    black.append((i,j))
                elif temp[i][j] == 'w':
                    self.config[(i,j)] = 1
                    white.append((i,j))
        self.workers = [white,black]
        return

    def hasfinished(self):
        # Returns {0, 1, 2} = {not finished, white wins, black wins}
        if len(self.workers[0]) == 2:
            return 2
        if len(self.workers[1]) == 2:
            return 1
        counterw=0
        counterb=0
        for i in range(10):
            if self.config[0,i]==1:
                counterw+=1
            if self.config[4,i]==2:
                counterb+=1
        if counterw >=3:
            return 1
        if counterb >=3:
            return 2
        return 0

    def printboard(self):
        # Print the board
        for i in range(5):
            b = []
            for j in range(10):
                if self.config[i,j] == 0:
                    b += ['_']
                elif self.config[i,j] == 1:
                    b += ['w']
                elif self.config[i,j] == 2:
                    b += ['b']
            print(''.join(b))
        print()
        print('White workers:')
        print(self.workers[0])
        print('Black workers:')
        print(self.workers[1])
        print()
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
                    return 0
            elif dir==2 and pos[0]>0 and pos[1]<9:
                if config[(pos[0]-1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]-1,pos[1]+1)]==2:
                    return 2
        elif config[pos] == 2:
            if dir==0 and pos[0]<4 and pos[1]<9:
                if config[(pos[0]+1,pos[1]+1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]+1)]==1:
                    return 2
            elif dir==1 and pos[0]<4:
                if config[(pos[0]+1,pos[1])]==0:
                    return 1
                elif config[(pos[0]+1,pos[1])]==1:
                    return 0
            elif dir==2 and pos[0]<4 and pos[1]>0:
                if config[(pos[0]+1,pos[1]-1)]==0:
                    return 1
                elif config[(pos[0]+1,pos[1]-1)]==1:
                    return 2
        return 0

    def move(self,pos,dir):
        # NOT checking whether can move
        if self.config[pos] == 0:
            print('Nothing to Move!')
            return
        elif self.config[pos] == 1:
            if dir==0:
                if self.config[(pos[0]-1,pos[1]-1)] == 2:
                    self.workers[1].remove((pos[0]-1,pos[1]-1))
                self.config[(pos[0]-1,pos[1]-1)] = 1
                self.workers[0].append((pos[0]-1,pos[1]-1))
                #==================================
                #ret=abreast(self,self.config[(pos[0]-1,pos[1]-1)],(pos[0]-1,pos[1]-1))
                #print(ret)
                #==================================
            elif dir==1:
                self.config[(pos[0]-1,pos[1])] = 1
                self.workers[0].append((pos[0]-1,pos[1]))
                #==================================
                #ret=abreast(self,self.config[(pos[0]-1,pos[1])],(pos[0]-1,pos[1]))
                #print(ret)
                #==================================
            elif dir==2:
                if self.config[(pos[0]-1,pos[1]+1)] == 2:
                    self.workers[1].remove((pos[0]-1,pos[1]+1))
                self.workers[0].append((pos[0]-1,pos[1]+1))
                #==================================
                #ret=abreast(self,self.config[(pos[0]-1,pos[1]+1)],(pos[0]-1,pos[1]+1))
                #print(ret)
                #==================================
                self.config[(pos[0]-1,pos[1]+1)] = 1
            self.workers[0].remove(pos)
            self.config[pos] = 0

        elif self.config[pos] == 2:
            if dir==0:
                if self.config[(pos[0]+1,pos[1]+1)] == 1:
                    self.workers[0].remove((pos[0]+1,pos[1]+1))
                self.config[(pos[0]+1,pos[1]+1)] = 2
                self.workers[1].append((pos[0]+1,pos[1]+1))
                #==================================
                #ret=abreast(self,self.config[(pos[0]+1,pos[1]+1)],(pos[0]+1,pos[1]+1))
                #print(ret)
                #==================================
            elif dir==1:
                self.config[(pos[0]+1,pos[1])] = 2
                self.workers[1].append((pos[0]+1,pos[1]))
                #==================================
                #ret=abreast(self,self.config[(pos[0]+1,pos[1])],(pos[0]+1,pos[1]))
                #print(ret)
                #==================================
            elif dir==2:
                if self.config[(pos[0]+1,pos[1]-1)] == 1:
                    self.workers[0].remove((pos[0]+1,pos[1]-1))
                self.config[(pos[0]+1,pos[1]-1)] = 2
                self.workers[1].append((pos[0]+1,pos[1]-1))
                #==================================
                #ret=abreast(self,self.config[(pos[0]+1,pos[1]-1)],(pos[0]+1,pos[1]-1))
                #print(ret)
                #==================================
            self.workers[1].remove(pos)
            self.config[pos] = 0
        else:
            print('Does not move!!!')
        return

    # Heuristics
    def dh1(self,color):
        return 2*len(self.workers[color-1]) + random.random()
    def oh1(self,color):
        return 2*(30-len(self.workers[2-color])) + random.random()
    def oh2(self,color,wh,dirh):
        cur=self.laststep(color)
        ret=self.abreast(color,wh,dirh)
        cap=self.captrue(color,wh,dirh)
        dis=self.distance(color,wh)
        #print('position:',wh,' ret:',ret,' cap:',cap)
        #return 1*cap+0.1*dis**2+2*(30-len(self.workers[2-color]))
        return 3*cur+0.3*ret+3*cap+0.1*0.7*(7-dis)**2+1*(30-len(self.workers[2-color]))
    def dh2(self,color,wh,dirh):
        ret=self.abreast(color,wh,dirh)
        cap=self.captrue(color,wh,dirh)
        dis=self.distance(color,wh)
        #print('position:',wh,' ret:',ret,' cap:',cap)
        return 1*cap+0.1*dis**2+2*(len(self.workers[color-1]))
    # Helpers for Heuristics
    def laststep(self,color):
        if color==1 and current_pos[0]==1:
          return 10
        elif color==2 and current_pos[0]==8:
          return 10
        else:
          return 0
    def abreast(self,color,pos,dir):
        #print('position:',w)
        #print('color:',color)
        if color==1:
            #white
            if dir==0:#forward left
                nextpos=(pos[0]-1,pos[1]-1)
            elif dir==1:#forward
                nextpos=(pos[0]-1,pos[1])
            elif dir==2:#forward right
                nextpos=(pos[0]-1,pos[1]+1)
            else:
                print('error')
                return -1
        elif color==2:
            #black
            if dir==0:
                nextpos=(pos[0]+1,pos[1]+1)
            elif dir==1:#forward
                nextpos=(pos[0]+1,pos[1])
            elif dir==2:#forward right
                nextpos=(pos[0]+1,pos[1]-1)
            else:
                print('error')
                return -1
        else:
            print('empty position!!')
            return -1
        x=nextpos[0]
        y=nextpos[1]
        start=y
        end=y
        sflag=0
        eflag=0
        if color==1:
            #white workers:
            white=[]

            for i in range(0,len(self.workers[0])):
                if self.workers[0][i][0]==x:
                    white.append(self.workers[0][i])
                    sorted(white, key=lambda x: x[1])
            #print('row:',white)
            #get consecutive
            while sflag==0 or eflag==0:
                if (x,start-1) in white:
                    start=start-1
                else:
                    sflag=1
                if(x,end+1) in white:
                    end=end+1
                else:
                    eflag=1
        elif color==2:
            #black workers:
            black=[]
            for i in range(0,len(self.workers[1])):
                if self.workers[1][i][0]==x:
                    black.append(self.workers[1][i])
                    sorted(black, key=lambda x: x[1])
            #print('row:',black)
            #get consecutive
            while sflag==0 or eflag==0:
                if (x,start-1) in black:
                    start=start-1
                else:
                    sflag=1
                #print('end',end)
                #print((x,end+1) in black)
                if (x,end+1) in black:
                    end=end+1
                else:
                    eflag=1
            #print('start:',start,' end:',end)
        else:
            print('empty position!!')
            return -1
        return end+1-start

    #input: current position, color, board, moving direction
    def captrue(self,color,pos,dir):
            # dir = {0,1,2} = {forward left, forward, forward right}
        if color==1:
            #white
            if dir==0:#forward left
                nextpos=(pos[0]-1,pos[1]-1)
            elif dir==1:#forward
                nextpos=(pos[0]-1,pos[1])
            elif dir==2:#forward right
                nextpos=(pos[0]-1,pos[1]+1)
            else:
                print('error')
                return -1

            pos1=(nextpos[0]-1,nextpos[1]-1)
            pos2=(nextpos[0]-1,nextpos[1]+1)
            ret=0
            if pos1 in self.workers[1]:
                ret=ret+1
            if pos2 in self.workers[1]:
                ret=ret+1

        elif color==2:
            #black
            if dir==0:
                nextpos=(pos[0]+1,pos[1]+1)
            elif dir==1:#forward
                nextpos=(pos[0]+1,pos[1])
            elif dir==2:#forward right
                nextpos=(pos[0]+1,pos[1]-1)
            else:
                print('error')
                return -1
            pos1=(nextpos[0]+1,nextpos[1]+1)
            pos2=(nextpos[0]+1,nextpos[1]-1)
            ret=0
            if pos1 in self.workers[0]:
                ret=ret+1
            if pos2 in self.workers[0]:
                ret=ret+1
        else:
            print('empty position!!!')
            return -1
        return ret

    def distance(self,color,w):
        if color==1:
          ret=w[0]
            #return w[0]
        elif color==2:
          ret=9-w[0]
            #return 7-w[0]
        else:
          print('empty position!!!!')
          return -1
        if ret==8:
          return 40
        else:
          return ret



# Search Strategies
def minmax(board,depth,color,wh,dirh,c,Max=True):
    c.inc()
    if depth==0 or board.hasfinished()>0:
        return (board.oh1(color),((-1,-1),-1))
    if Max:
      strategy = ((-1,-1),-1)
      value = float('-inf')
      for w in board.workers[color-1]:
          for dir in range(3):
              if board.canMove(w,dir)>0:
                  newboard = copy.deepcopy(board)
                  newboard.move(w,dir)
                  temp=minmax(newboard,depth-1,color,w,dir,c,False)
                  curval=temp[0]
                  if value < curval:
                      value = curval
                      strategy = (w,dir)
    else:
      strategy = ((-1,-1),-1)
      value=float('inf')
      for w in board.workers[2-color]:
          for dir in range(3):
              if board.canMove(w,dir)>0:
                  newboard = copy.deepcopy(board)
                  newboard.move(w,dir)
                  temp=minmax(newboard,depth-1,color,w,dir,c,True)
                  curval=temp[0]
                  if value > curval:
                      value = curval
                      strategy = (w,dir)
    return (value,strategy)

"""
# Search Strategies
def minmax2(board,depth,color,Max=True):
    if depth==0 or board.hasfinished()>0:
        return (board.oh1(color),((-1,-1),-1))
    if Max:
      strategy = ((-1,-1),-1) #White
      value = float('-inf')
      for w in board.workers[color-1]:
        for dir in range(3):
          if board.canMove(w,dir)>0:
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
          if board.canMove(w,dir)>0:
            newboard = copy.deepcopy(board)
            newboard.move(w,dir)
            temp=minmax2(newboard,depth-1,color,True)
            curval=temp[0]
            if value > curval:
              value = curval
              strategy = (w,dir)
    return (value,strategy)
"""

def alphabeta(board,depth,color,wh,dirh,a,b,c,canM=0,Max=True):    # initialize a=neginf b=posinf
    c.inc()
    if depth==0 or board.hasfinished()>0:
        #==================
        global current_pos
        current_pos=wh
        #==================
        return (board.oh2(color,wh,dirh)+canM,((-1,-1),-1),0)
    if Max:
      # Want larger in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[color-1]:
          for dir in range(3):
              searchlist.append((w,dir))
      random.shuffle(searchlist)
      # Regular search
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          canmove=board.canMove(w,dir)
          if canmove>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,w,dir,a,b,c,canM+canmove,False)
              curval=temp[0]
              if a < curval:
                  a = curval
                  strategy = (w,dir)
              if a >= b:
                  # Record into refutable table for future reference
                  return (a,strategy)
      return (a,strategy)
    else:
      # Want smaller in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[2-color]:
          for dir in range(3):
              searchlist.append((w,dir))
      random.shuffle(searchlist)
      # Regular
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          canmove=board.canMove(w,dir)
          if canmove>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta(newboard,depth-1,color,w,dir,a,b,c,canM-canmove,True)
              curval=temp[0]
              if b > curval:
                  b = curval
                  strategy = (w,dir)
              if a >= b:
                  return (b,strategy)
      return (b,strategy)

def alphabeta2(board,depth,color,wh,dirh,a,b,c,canM=0,Max=True):    # initialize a=neginf b=posinf
    c.inc()
    if depth==0 or board.hasfinished()>0:
        #==================
        global current_pos
        current_pos=wh
        #==================
        return (board.oh1(color),((-1,-1),-1),0)
    if Max:
      # Want larger in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[color-1]:
          for dir in range(3):
              searchlist.append((w,dir))
      random.shuffle(searchlist)
      # Regular search
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          canmove=board.canMove(w,dir)
          if canmove>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta2(newboard,depth-1,color,w,dir,a,b,c,canM+canmove,False)
              curval=temp[0]
              if a < curval:
                  a = curval
                  strategy = (w,dir)
              if a >= b:
                  # Record into refutable table for future reference
                  return (a,strategy)
      return (a,strategy)
    else:
      # Want smaller in front
      strategy = ((-1,-1),-1)
      # Construct Search table
      searchlist = []
      for w in board.workers[2-color]:
          for dir in range(3):
              searchlist.append((w,dir))
      random.shuffle(searchlist)
      # Regular
      for strat in searchlist:
          w = strat[0]
          dir = strat[1]
          canmove=board.canMove(w,dir)
          if canmove>0:
              newboard = copy.deepcopy(board)
              newboard.move(w,dir)
              temp=alphabeta2(newboard,depth-1,color,w,dir,a,b,c,canM-canmove,True)
              curval=temp[0]
              if b > curval:
                  b = curval
                  strategy = (w,dir)
              if a >= b:
                  return (b,strategy)
      return (b,strategy)

def play(board):
    whiteexp = count()
    blackexp = count()
    while True:
        start = time.time()
<<<<<<< Updated upstream
        s=alphabeta(board,4,2,(),0,float('-inf'),float('inf'),blackexp)[1]
        #s=alphabeta2(board,4,1,(),0,float('-inf'),float('inf'),whiteexp)[1]
=======
        #s=minmax(board,3,1,(),0,whiteexp)[1]
        s=alphabeta(board,4,1,(),0,float('-inf'),float('inf'),whiteexp)[1]
>>>>>>> Stashed changes
        end = time.time()
        whiteexp.tinc(start,end)
        whiteexp.sinc()
        board.printboard()
        board.move(s[0],s[1])
        if board.hasfinished() == 1:
            board.printboard()
            print("white wins")
            print()
            break

        start = time.time()
<<<<<<< Updated upstream
        s=alphabeta2(board,4,1,(),0,float('-inf'),float('inf'),whiteexp)[1]
        #s=alphabeta(board,4,2,(),0,float('-inf'),float('inf'),blackexp)[1]
=======
        s=alphabeta2(board,4,2,(),0,float('-inf'),float('inf'),blackexp)[1]
>>>>>>> Stashed changes
        end = time.time()
        blackexp.tinc(start,end)
        blackexp.sinc()
        board.printboard()
        board.move(s[0],s[1])

        if board.hasfinished()== 2:
            board.printboard()
            print("black wins")
            print()
            break
    print('White Total Nodes Expanded: ',end='')
    print(whiteexp.count)
    print('White Avg Nodes Expanded:',end='')
    print(whiteexp.count/whiteexp.step)
    print('White Total Steps:',end='')
    print(whiteexp.step)
    print('White Avg Time per Move:',end='')
    print(whiteexp.time/whiteexp.step)
    print()

    print('Black Total Nodes Expanded: ',end='')
    print(blackexp.count)
    print('Black Avg Nodes Expanded:',end='')
    print(blackexp.count/blackexp.step)
    print('Black Total Steps:',end='')
    print(blackexp.step)
    print('Black Avg Time per Move:',end='')
    print(blackexp.time/blackexp.step)
    print()


b = Board()
# b.readboard("error.txt")
play(b)
