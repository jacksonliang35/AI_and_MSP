import os
import math
import numpy as np
import queue
import sys
import copy
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
      #self.graph[-1].append('%')
      self.height = len(self.graph)-1
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
      return
    
    def findGoal(self):
      self.goalx =[]
      self.goaly =[]
      goal=[]
      for i in range(self.height):
          for j in range(self.width):
            if self.graph[i][j]== '.':
              self.goalx += [i]
              self.goaly += [j]
      for i in range(len(self.goalx)):
        goal += [(self.goalx[i],self.goaly[i])]
      return (self.goalx==[], goal)
      
    def findGoal2(self,graph):
      self.goalx =[]
      self.goaly =[]
      goal=[]
      for i in range(self.height):
        for j in range(self.width):
          if graph[i][j]=='.':
            self.goalx += [i]
            self.goaly += [j]
      for i in range(len(self.goalx)):
        goal += [(self.goalx[i],self.goaly[i])]
      return (len(self.goalx)==0, goal)

    def canTravel(self,x, y,dir):
      if (x < 0) or (y < 0) or (x >= self.height) or (y >= self.width):
        return False
      elif (dir == 0 and x == 0) or (dir == 1 and x == self.height - 1) or (dir == 2 and y == 0) or (dir == 3 and y == self.width - 1):
        return False;
      elif (dir == 0 and x == 1) or (dir == 1 and x == self.height - 2) or (dir == 2 and y == 1) or (dir == 3 and y == self.width - 2):
        if dir == 0:#up
            return (self.graph[x-1][y]!='%' and self.graph[x-1][y]!='b' and self.graph[x-1][y]!='B' )
        elif dir == 1 :#down
            return (self.graph[x+1][y]!='%' and self.graph[x+1][y]!='b' and self.graph[x+1][y]!='B')
        elif dir == 2 :#left
            return (self.graph[x][y-1]!='%' and self.graph[x][y-1]!='b' and self.graph[x][y-1]!='B')
        elif dir == 3 :#right
            return (self.graph[x][y+1]!='%' and self.graph[x][y+1]!='b' and self.graph[x][y+1]!='B')
      elif dir == 0:#up
        return ((self.graph[x-1][y]=='B' or self.graph[x-1][y]=='b' ) and self.graph[x-2][y]==' ') or self.graph[x-1][y]==' '
      elif dir == 1 :#down
        return ((self.graph[x+1][y]=='B' or self.graph[x+1][y]=='b' ) and self.graph[x+2][y]==' ') or self.graph[x+1][y]==' '
      elif dir == 2 :#left
        return ((self.graph[x][y-1]=='B' or self.graph[x][y-1]=='b' ) and self.graph[x][y-2]==' ') or self.graph[x][y-1]==' '
      elif dir == 3 :#right
        return ((self.graph[x][y+1]=='B' or self.graph[x][y+1]=='b' ) and self.graph[x][y+2]==' ') or self.graph[x][y+1]==' '
      return False


    def Astar(self):
        counter=0
        path=[]
        start= (self.startx,self.starty)
        graph=copy.deepcopy(self.graph)
        # Create goal list
        goal = []
        for i in range(len(self.goalx)):
            goal += [(self.goalx[i],self.goaly[i])]
        # Set up goal counter
        explored = np.zeros(self.height*self.width)
        explored[start[1]+(start[0])*self.width] = 1
        q = queue.PriorityQueue()
        # push evaluation, cost (pathlength), (counter,) position, path, goalc, explored
        q.put([heuristic2(start,goal),0,counter,start,path,explored,graph])
        while not q.empty():
            counter+=1
            state = q.get()
            costc = state[1]
            pos = state[3]
            x = pos[0]
            y = pos[1]
            path = state[4]
            explored = state[5]
            graph =state[6]
            
            #print(len(goalc))
            temp=self.findGoal2(graph)
            goalc = temp[1]
            print(len(goalc))
            for line in graph:
              print(''.join(line))
            # Goal State
            if temp[0]:
                
                self.path=copy.deepcopy(path)
                return counter
                #break    # Same as breaking two loops
            if self.canTravel(x, y, 0):
                if explored[y+(x-1)*self.width]==0:
                    explored[y+(x-1)*self.width]=1
                    if graph[x-1][y]=='b':
                        if graph[x-2][y]=='.':
                            graph[x-2][y]='B'
                        else:
                            graph[x-2][y]='b'
                        graph[x-1][y]=' '
                        explored = np.zeros(self.height*self.width)
                    elif graph[x-1][y]=='B':
                        graph[x-1][y]='.'
                        if graph[x-2][y]=='.':
                            graph[x-2][y]='B'
                        else:
                            graph[x-2][y]='b'
                        explored = np.zeros(self.height*self.width)
                    q.put([costc+1+heuristic2((x-1,y),goalc),costc+1,counter,(x-1,y),path.copy()+[0],explored,graph.copy()])

            if self.canTravel(x, y, 1):
                if explored[y+(x+1)*self.width]==0:
                    explored[y+(x+1)*self.width]=1
                    if graph[x+1][y]=='b':
                        if graph[x+2][y]=='.':
                            graph[x+2][y]='B'
                        else:
                            graph[x+2][y]='b'
                        graph[x+1][y]=' '
                        explored = np.zeros(self.height*self.width)
                    elif graph[x+1][y]=='B':
                        graph[x+1][y]='.'
                        if graph[x+2][y]=='.':
                            graph[x+2][y]='B'
                        else:
                            graph[x+2][y]='b'
                        explored = np.zeros(self.height*self.width)
                    q.put([costc+1+heuristic2((x+1,y),goalc),costc+1,counter,(x+1,y),path.copy()+[1],explored,graph.copy()])

            if self.canTravel(x, y, 2):
                if explored[y-1+x*self.width]==0:
                    explored[y-1+x*self.width]=1
                    if graph[x][y-1]=='b':
                        if graph[x][y-2]=='.':
                            graph[x][y-2]='B'
                        else:
                            graph[x][y-2]='b'
                        graph[x][y-1]=' '
                        explored = np.zeros(self.height*self.width)
                    elif graph[x][y-1]=='B':
                        graph[x][y-1]='.'
                        if graph[x][y-2]=='.':
                            graph[x][y-2]='B'
                        else:
                            graph[x][y-2]='b'
                        explored = np.zeros(self.height*self.width)
                    q.put([costc+1+heuristic2((x,y-1),goalc),costc+1,counter,(x,y-1),path.copy()+[2],explored,graph.copy()])
                    
            if self.canTravel(x, y, 3):
                if explored[y+1+x*self.width]==0:
                    explored[y+1+x*self.width]=1
                    if graph[x][y+1]=='b':
                        if graph[x][y+2]=='.':
                            graph[x][y+2]='B'
                        else:
                            graph[x][y+2]='b'
                        graph[x][y+1]=' '
                        explored = np.zeros(self.height*self.width)
                    elif graph[x][y+1]=='B':
                        graph[x][y+1]='.'
                        if graph[x][y+2]=='.':
                            graph[x][y+2]='B'
                        else:
                            graph[x][y+2]='b'
                        explored = np.zeros(self.height*self.width)
                    q.put([costc+1+heuristic2((x,y+1),goalc),costc+1,counter,(x,y+1),path.copy()+[3],explored,graph.copy()])
                    

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

''' Heuristics '''              
def heuristic2(cur, goal):    #goal is a list  
    return 0
    dist = []    
    # Find the longest path
    for g in goal:
        dist = dist + [abs(cur[0]-g[0])+abs(cur[1]-g[1])]
    h1 = max(dist)
    # Find sum of smallest distances with # of len(goal)
    
    n = len(goal)       
    for i in range(n):
        j = i+1
        while j<n:    
            dist = dist + [abs(goal[i][0]-goal[j][0])+abs(goal[i][1]-goal[j][1])]
            j += 1
    dist.sort()
    h2 = sum(dist[0:n])

    return max([h1,h2])


a=maze()
a.readMaze('sokoban1.txt')
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

        
