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
		return 0   #abs(y-yg)+abs(x-xg)

	def heuristic2(self, cur, goal):	#goal is a list
		go=0
		return 0
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
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]== '.':
					self.goalx.append(i)
					self.goaly.append(j)
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


	def Astar(self):
		counter=0
		path=[]
		startx= self.startx
		starty= self.starty	
		goal = []
		goalx=self.goalx.copy()
		goaly=self.goaly.copy()
		for i in range(len(goalx)):
			goal += [(goalx[i],goaly[i])]
		goalc = 0
		discover = dict()
		explored = np.zeros(self.height*self.width)
		explored[startx+(starty)*self.width] = 1
		q = queue.PriorityQueue()

		q.put([self.heuristic2((startx, starty),goal),counter,(startx,starty,0,path.copy(),goal.copy(),discover,explored.copy(),startx,starty)])
		while not q.empty():
			counter+=1
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
			print(len(goal))
			# Goal State
			if (x,y) in goal:

				while current != (startx,starty):
					temp = discover[current[0]+current[1]*self.width]
					current = (temp%self.width,temp//self.width)
					self.path.insert(0,current)
				startx = x
				starty = y
				goal.remove((x,y))
				explored = np.zeros(self.height*self.width)
				if goal == []:
					self.path=path
					break
				#break	# Same as breaking two loops
			if self.canTravel(x, y, 0):
				if explored[x+(y-1)*self.width]==0:
					explored[x+(y-1)*self.width]=1
					discover[x+(y-1)*self.width]=x+(y)*self.width
					q.put([cost+1+self.heuristic2((x, y),goal),counter,(x,y-1,cost+1,path.copy(),goal.copy(),discover.copy(),explored.copy(),startx,starty)])

			if self.canTravel(x, y, 1):
				if explored[x+(y+1)*self.width]==0:
					explored[x+(y+1)*self.width]=1
					discover[x+(y+1)*self.width]=x+(y)*self.width
					q.put([cost+1+self.heuristic2((x, y),goal),counter,(x,y+1,cost+1,path.copy(),goal.copy(),discover.copy(),explored.copy(),startx,starty)])

			if self.canTravel(x, y, 2):
				if explored[x-1+(y)*self.width]==0:
					explored[x-1+(y)*self.width]=1
					discover[x-1+(y)*self.width]=x+(y)*self.width
					q.put([cost+1+self.heuristic2((x, y),goal),counter,(x-1,y,cost+1,path.copy(),goal.copy(),discover.copy(),explored.copy(),startx,starty)])
					
			if self.canTravel(x, y, 3):
				if explored[x+1+(y)*self.width]==0:
					explored[x+1+(y)*self.width]=1
					discover[x+1+(y)*self.width]=x+(y)*self.width
					q.put([cost+1+self.heuristic2((x, y),goal),counter,(x+1,y,cost+1,path.copy(),goal.copy(),discover.copy(),explored.copy(),startx,starty)])
					

		return counter	

	def drawsol(self):
		for i in range(10):
			self.graph[self.path[i][1]][self.path[i][0]]='~'
		self.graph[self.starty][self.startx]='P'
		with open('maze_result.txt', 'w') as f:
			sys.stdout = f
			for line in self.graph:
				print(''.join(line))
		f.close()
		return



a=maze()
a.readmaze('tinySearch.txt')

#for i in range(a.height):
#	print(a.graph[i])
a.findGoal()
a.findStart()
print(a.Astar())
print(len(a.path))
print(a.path)
a.drawsol()
#print(a.greedy())
#print(a.bfs())

#print(a.graph[21][5])
a.drawsol()


		
