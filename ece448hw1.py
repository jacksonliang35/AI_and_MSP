import os


class maze:
	"""docstring for maze"""
	def __init__(self):
         self.graph=[]
         self.height=0
         self.width=0
         self.explored=[]
         self.path=[]
         self.tree=[]
         
         return
	def readmaze(self,filename):
         self.graph= []
         with open(filename,"r") as fp:
             for line in fp:
                 self.graph.append(line[0:len(line)-1])
         fp.close()
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

	def findGoals(self):
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
         return False

if __name__ == '__main__':
    a=maze()
    a.readmaze('mediummaze.txt')
    '''    
    for i in range(a.height):
        print(a.graph[i])
    '''
    


		