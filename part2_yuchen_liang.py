import os
import math
import numpy as np
import queue
import sys

class maze:
    """docstring for maze"""
    def __init__(self, graph=[], height=0, width=0, explored=[], path=[], goalx=[], goaly=[],startx=0,starty=0):
        self.graph=[]
        self.height=0
        self.width=0
        self.explored=[]
        self.path=[]
        self.goalx=[]
        self.goaly=[]
        self.startx=-1
        self.starty=-1
        return
    def readMaze(self,filename):
         self.graph= []
         with open(filename,"r") as fp:
            for line in fp:
                self.graph.append(list(line[0:len(line)-1]))
         fp.close()
         self.graph[-1].append('%')
         self.height = len(self.graph)
         self.width = len(self.graph[0])
         self.getStart()
         return
    def getStart(self):
         for i in range(self.height):
            for j in range(self.width):
                if self.graph[i][j]== 'P':
                    self.startx=i
                    self.starty=j
                    break
            if self.startx!=-1:
                break
    def heuristic(self, x, y, xg, yg):
        return 0   #abs(y-yg)+abs(x-xg)

    def heuristic2(self, cur, goal):    #goal is a list
        return len(goal)
        '''
        for i in range(4):
            if self.canTravel(cur[0],cur[1],i) ==False:
                go+=1
        sum = 0
        for p in goal:
            sum += abs(cur[0]-p[0])+abs(cur[1]-p[1])
        return go*50
        '''
        
    def findGoal(self):
         for i in range(self.height):
            for j in range(self.width):
                if self.graph[i][j]== '.':
                    self.goalx += [i]
                    self.goaly += [j]

    def canTravel(self,x, y, dir):
        if (x < 0) or (y < 0) or (x >= self.height) or (y >= self.width):
            return False
        elif (dir == 0 and x == 0) or (dir == 1 and x == self.height - 1) or (dir == 2 and y == 0) or (dir == 3 and y == self.width - 1):
            return False;
        elif dir == 0:#up
            return (self.graph[x-1][y]!='%')
        elif dir == 1 :#down
            return (self.graph[x+1][y]!='%')
        elif dir == 2 :#left
            return (self.graph[x][y-1]!='%')
        elif dir == 3 :#right
            return (self.graph[x][y+1]!='%')


    def Astar(self):
        counter=0
        path=[]
        start= (self.startx,self.starty)
        # Create goal list
        goal = []
        for i in range(len(self.goalx)):
            goal += [(self.goalx[i],self.goaly[i])]
        # Set up goal counter
        explored = np.zeros(self.height*self.width)
        explored[start[1]+(start[0])*self.width] = 1
        q = queue.PriorityQueue()
        # push evaluation, cost (pathlength), (counter,) position, path, goalc, explored
        q.put([self.heuristic2(start,goal),0,counter,start,path,goal,explored])
        while not q.empty():
            counter+=1
            state = q.get()
            costc = state[1]
            pos = state[3]
            x = pos[0]
            y = pos[1]
            path = state[4]
            goalc = state[5]
            explored = state[6]
            print(len(goalc))
            '''
            temp2= q.get()[2]
            current=(temp2[0],temp2[1])
            cost=temp2[2]
            path = temp2[3]
            goal =temp2[4]
            discover = temp2[5]
            explored = temp2[6]
            startx = temp2[7]
            starty =temp2[8]
            x=temp2[0]
            y=temp2[1]
            '''

            # Goal State
            if pos in goalc:
                goalc.remove(pos)
                if goalc == []:
                    self.path=path
                    return counter
                explored = np.zeros(self.height*self.width)
                explored[y+x*self.width]=1
                #break    # Same as breaking two loops
            if self.canTravel(x, y, 0):
                if explored[y+(x-1)*self.width]==0:
                    explored[y+(x-1)*self.width]=1
                    q.put([costc+1+self.heuristic2(pos,goalc),costc+1,counter,(x-1,y),path.copy()+[0],goalc.copy(),explored])

            if self.canTravel(x, y, 1):
                if explored[y+(x+1)*self.width]==0:
                    explored[y+(x+1)*self.width]=1
                    q.put([costc+1+self.heuristic2(pos,goalc),costc+1,counter,(x+1,y),path.copy()+[1],goalc.copy(),explored])

            if self.canTravel(x, y, 2):
                if explored[y-1+x*self.width]==0:
                    explored[y-1+x*self.width]=1
                    q.put([costc+1+self.heuristic2(pos,goalc),costc+1,counter,(x,y-1),path.copy()+[2],goalc.copy(),explored])
                    
            if self.canTravel(x, y, 3):
                if explored[y+1+x*self.width]==0:
                    explored[y+1+x*self.width]=1
                    q.put([costc+1+self.heuristic2(pos,goalc),costc+1,counter,(x,y+1),path.copy()+[3],goalc.copy(),explored])
                    

        return -1    

    def drawsol(self):
        for i in range(len(self.path)):
            self.graph[self.path[i][1]][self.path[i][0]]='~'
        self.graph[self.starty][self.startx]='P'
        return

    def drawPath(self):
         path = self.path.copy()
         curx = self.startx
         cury = self.starty
         for x in path:
             if x==0:
                 curx -= 1
                 self.graph[curx][cury] = '~'
             elif x==1:
                 curx += 1
                 self.graph[curx][cury] = '~'
             elif x==2:
                 cury -= 1
                 self.graph[curx][cury] = '~'
             else:
                 cury += 1
                 self.graph[curx][cury] = '~'

    def printMaze(self):
          for line in self.graph:
              print(''.join(line))

a=maze()
a.readMaze('tinySearch.txt')
a.printMaze()
#for i in range(a.height):
#    print(a.graph[i])
a.findGoal()
a.getStart()
print(a.Astar())
print(len(a.path))
print(a.path)
a.drawPath()
a.printMaze()
#print(a.greedy())
#print(a.bfs())

#print(a.graph[21][5])
#a.drawsol()


        
