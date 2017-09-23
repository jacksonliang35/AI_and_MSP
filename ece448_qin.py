import os
import math
import numpy as np
import Queue
def heuristic(self, x, y, xg, yg):
	return math.abs(y-yg)+math.abs(x-xg)

def findloop(index, array):
	a=int(index)
	while a!=-1:
		a=int(array[a])
		if index==array[a]:
			return True
	return False
class maze:
	"""docstring for maze"""
	def __init__(self, graph=[], height=0, width=0, explored=[], path=[], tree=[], goalx=[], goaly=[],startx=0,starty=0):
		self.graph=[]
		self.height=0
		self.width=0
		self.explored=[]
		self.path=[]
		self.tree=[]
		self.goalx=[]
		self.goaly=[]
		self.startx=0
		self.starty=0
		return
	def readmaze(self,filename):
		self.graph= []
		with open("mediumMaze.txt","r") as fp:
			for line in fp:
				self.graph.append(line[0:len(line)-1])
		fp.close()
		self.height = len(self.graph)
		self.width = len(self.graph[0])
		return
	def findStart(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]== 'P':
					self.startx=i
					self.starty=j
					break
		return

	def findGoal(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]== '.':
					self.goalx.append(i)
					self.goaly.append(j)
					break
		return

	def canTravel(self,x, y, dir):
		if (x < 0) or (y < 0) or (x >= self.width) or (y >= self.height):
			return False
		if (dir == 0 and y == 0) or (dir == 1 and y == self.height - 1) or (dir == 2 and x == 0) or (dir == 3 and x == self.width - 1):
			return False
		if dir == 0:
			return (self.graph[x][y-1]!='%')#up
		if dir == 1:
			return (self.graph[x][y+1]!='%')#down
		if dir == 2:
			return (self.graph[x-1][y]!='%')#left
		if dir == 3:
		  return (self.graph[x+1][y]!='%')#right
		return False


	def Astar(self):
		q = Queue.Queue() 
		s = []
		parent=np.zeros(self.height*self.width)
		self.explored=np.zeros((self.height,self.width))
		for i in range(self.width*self.height):
			parent[i]=-1

		q.put((self.startx,self.starty))
		while not q.empty():
			current = q.get()
			print(current)
			x=current[0]
			y=current[1]
			if current[0] == self.goalx[0] and current[1]==self.goaly[0]:
				while current != (self.startx,self.starty):
					path.insert(current)
					current = parent[current[0]+current[1]*self.width]
				return
			if self.canTravel(x, y, 0) and not findloop(x+(y-1)*self.width,parent):
			  q.put((x,y-1))
			  parent[x+(y-1)*self.width] = x+y*self.width
			
			if self.canTravel(x, y, 1) and not findloop(x+(y+1)*self.width,parent):
			  q.put((x,y+1))
			  parent[x+(y+1)*self.width] = x+y*self.width
			if self.canTravel(x, y, 2) and not findloop(x-1+y*self.width,parent):
			  q.put((x-1,y))
			  parent[x-1+(y)*self.width] = x+y*self.width
			if self.canTravel(x, y, 3) and not findloop(x+1+y*self.width,parent):
			  q.put((x+1,y))
			  parent[x+1+(y)*self.width] = x+y*self.width
		return

	def drawsol(self):
		for i in range(len(self.path)):
			self.graph[path[i][0]][path[i][1]]='~'
		for i in range(self.height):
			print(self.graph[i])
		return



a=maze()
a.readmaze('mediummaze.txt')
a.findGoal()
a.findStart()
for i in range(a.height):
	print(a.graph[i])
a.Astar()
print(a.path)
a.drawsol()


		
