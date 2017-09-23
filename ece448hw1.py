import os
import copy

class maze:
    """docstring for maze"""
    def __init__(self):
         self.graph=[]
         self.height=0
         self.width=0
         # self.tree=[] ---> What's this?
         self.startx = -1
         self.starty = -1
         self.dfscost = -1
         self.dfspath = []
         return
         
    def readMaze(self,filename):
         self.graph= []
         with open(filename,"r") as fp:
             for line in fp:
                 self.graph.append(list(line[0:len(line)-1]))
         fp.close()
         self.height = len(self.graph)
         self.width = len(self.graph[0])
         self.getStart()
         return
    
    def printMaze(self):
        for line in self.graph:
            print(''.join(line))
     
    def getStart(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.graph[i][j]== 'P':
                   self.startx=i
                   self.starty=j
                   break
        return

    def findGoals(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.graph[i][j]== '.':
                    self.goalx += [i]
                    self.goaly += [j]
        return

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
         return False
         
    def drawPath(self):
         path = self.dfspath.copy()
         curx = self.startx
         cury = self.starty
         for x in path:
             if x==0:
                 curx -= 1
                 self.graph[curx][cury] = '.'
             elif x==1:
                 curx += 1
                 self.graph[curx][cury] = '.'
             elif x==2:
                 cury -= 1
                 self.graph[curx][cury] = '.'
             else:
                 cury += 1
                 self.graph[curx][cury] = '.'
         return
         
    def DFS(self):
        # Use list as stack, find single goal, change maze, return nodes expanded
        graph = copy.deepcopy(self.graph)  # Is this a reference or a copy?
        x = self.startx
        y = self.starty
        node = 0
        if x==-1 or y==-1:
            return -1
        stack = [(x,y,[])]   # tuple = (x-cood,y-cood,path)
        while(stack!=[]):
            curr = stack.pop()
            x = curr[0]
            y = curr[1]
            node += 1
            if graph[x][y]=='.':
                self.dfspath = curr[2]
                self.dfscost = len(curr[2])
                return node
            if graph[x][y]=='*':
                continue
            # Add
            graph[x][y] = '*'
            if self.canTravel(x,y,0):
                stack += [(x-1,y,curr[2].copy()+[0])]
            if self.canTravel(x,y,1):
                stack += [(x+1,y,curr[2].copy()+[1])]
            if self.canTravel(x,y,2):
                stack += [(x,y-1,curr[2].copy()+[2])]
            if self.canTravel(x,y,3):
                stack += [(x,y+1,curr[2].copy()+[3])]
        return -1
        
if __name__=='__main__':
    a=maze()
    a.readMaze('mediummaze.txt')
    a.printMaze()
    
    b = a.DFS()
    print()
    a.drawPath()
    a.printMaze()


		