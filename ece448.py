import os
import math
import numpy as np
import queue
import sys

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
		with open(filename,"r") as fp:
			for line in fp:
				self.graph.append(list(line[0:len(line)-1]))
		fp.close()
		self.height = len(self.graph)-1
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
	def heuristic(self, x, y, xg, yg):
		return abs(y-yg)+abs(x-xg)

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
			return (self.graph[y-1][x]!='%')#up
		if dir == 1:
			return (self.graph[y+1][x]!='%')#down
		if dir == 2:
			return (self.graph[y][x-1]!='%')#left
		if dir == 3:
		  return (self.graph[y][x+1]!='%')#right
		return False

	def greedy(self):
		counter=0
		self.path=[]
		q = queue.PriorityQueue()
		discover = dict()
		self.explored=np.zeros(self.height*self.width)
		self.explored[self.startx+(self.starty)*self.width]=1
		q.put((self.heuristic(self.startx, self.starty, self.goalx[0], self.goaly[0]),(self.startx,self.starty)))
		while not q.empty():
			counter+=1
			current = q.get()[1]
			x=current[0]
			y=current[1]
			if current[0] == self.goalx[0] and current[1]==self.goaly[0]:
				while current != (self.startx,self.starty):
					temp = discover[current[0]+current[1]*self.width]
					current = (temp%self.width,temp//self.width)
					self.path.insert(0,current)
				return counter
			if self.canTravel(x, y, 0):
				if self.explored[x+(y-1)*self.width]==0:
					self.explored[x+(y-1)*self.width]=1
					q.put((self.heuristic(x, y-1, self.goalx[0], self.goaly[0]),(x,y-1)))
					discover[x+(y-1)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 1):
				if self.explored[x+(y+1)*self.width]==0:
					self.explored[x+(y+1)*self.width]=1
					q.put((self.heuristic(x, y+1, self.goalx[0], self.goaly[0]),(x,y+1)))
					discover[x+(y+1)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 2):
				if self.explored[x-1+(y)*self.width]==0:
					self.explored[x-1+(y)*self.width]=1
					q.put((self.heuristic(x-1, y, self.goalx[0], self.goaly[0]),(x-1,y)))
					discover[x-1+(y)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 3):
				if self.explored[x+1+(y)*self.width]==0:
					self.explored[x+1+(y)*self.width]=1
					q.put((self.heuristic(x+1, y, self.goalx[0], self.goaly[0]),(x+1,y)))
					discover[x+1+(y)*self.width]=x+(y)*self.width
			
		return -1

	def Astar(self):
		counter=0
		self.path=[]
		q = queue.PriorityQueue()
		discover = dict()
		self.explored=np.zeros(self.height*self.width)
		self.explored[self.startx+(self.starty)*self.width]=1
		q.put((self.heuristic(self.startx, self.starty, self.goalx[0], self.goaly[0]),(self.startx,self.starty,0)))
		while not q.empty():
			print("here")
			counter+=1
			temp2= q.get()[1]
			current=(temp2[0],temp2[1])
			cost=temp2[2]
			x=current[0]
			y=current[1]
			print("Astarxy",x,y)
			if current[0] == self.goalx[0] and current[1]==self.goaly[0]:
				while current != (self.startx,self.starty):
					temp = discover[current[0]+current[1]*self.width]
					current = (temp%self.width,temp//self.width)
					self.path.insert(0,current)
				return counter
			if self.canTravel(x, y, 0):
				if self.explored[x+(y-1)*self.width]==0:
					self.explored[x+(y-1)*self.width]=1
					q.put((cost+1+self.heuristic(x, y-1, self.goalx[0], self.goaly[0]),(x,y-1,cost+1)))
					discover[x+(y-1)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 1):
				if self.explored[x+(y+1)*self.width]==0:
					self.explored[x+(y+1)*self.width]=1
					q.put((cost+1+self.heuristic(x, y+1, self.goalx[0], self.goaly[0]),(x,y+1,cost+1)))
					discover[x+(y+1)*self.width]=x+(y)*self.width
			if self.canTravel(x, y, 2):
				if self.explored[x-1+(y)*self.width]==0:
					self.explored[x-1+(y)*self.width]=1
					q.put((cost+1+self.heuristic(x-1, y, self.goalx[0], self.goaly[0]),(x-1,y,cost+1)))
					discover[x-1+(y)*self.width]=x+(y)*self.width
			if self.canTravel(x, y, 3):
				if self.explored[x+1+(y)*self.width]==0:
					self.explored[x+1+(y)*self.width]=1
					q.put((cost+1+self.heuristic(x+1, y, self.goalx[0], self.goaly[0]),(x+1,y,cost+1)))
					discover[x+1+(y)*self.width]=x+(y)*self.width
			
		return -1	

	def bfs(self):
		counter =0
		self.path=[]
		q = queue.Queue() 
		discover = dict()
		self.explored=np.zeros(self.height*self.width)
		self.explored[self.startx+(self.starty)*self.width]=1
		q.put((self.startx,self.starty))
		while not q.empty():
			counter+=1
			current = q.get()
			x=current[0]
			y=current[1]
			if current[0] == self.goalx[0] and current[1]==self.goaly[0]:
				while current != (self.startx,self.starty):
					temp = discover[current[0]+current[1]*self.width]
					current = (temp%self.width,temp//self.width)
					self.path.insert(0,current)
				return counter
			if self.canTravel(x, y, 0):
				if self.explored[x+(y-1)*self.width]==0:
					self.explored[x+(y-1)*self.width]=1
					q.put((x,y-1))
					discover[x+(y-1)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 1):
				if self.explored[x+(y+1)*self.width]==0:
					self.explored[x+(y+1)*self.width]=1
					q.put((x,y+1))
					discover[x+(y+1)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 2):
				if self.explored[x-1+(y)*self.width]==0:
					self.explored[x-1+(y)*self.width]=1
					q.put((x-1,y))
					discover[x-1+(y)*self.width]=x+(y)*self.width

			if self.canTravel(x, y, 3):
				if self.explored[x+1+(y)*self.width]==0:
					self.explored[x+1+(y)*self.width]=1
					q.put((x+1,y))
					discover[x+1+(y)*self.width]=x+(y)*self.width

			
		return -1

	def drawsol(self):
		for i in range(len(self.path)):
			self.graph[self.path[i][1]][self.path[i][0]]='.'
		self.graph[self.starty][self.startx]='P'
		with open('maze_result.txt', 'w') as f:
			sys.stdout = f
			for line in self.graph:
				print(''.join(line))
		f.close()
		return



a=maze()
a.readmaze('mediummaze.txt')

#for i in range(a.height):
#	print(a.graph[i])
a.findGoal()
a.findStart()
print(a.Astar())
#print(a.greedy())
#print(a.bfs())

#print(a.graph[21][5])
a.drawsol()


		
