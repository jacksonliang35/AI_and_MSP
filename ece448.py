import os
import math
import numpy as np
import queue
import sys
import copy

class maze:
	"""docstring for maze"""
	#We use a stracture to record the basic information of the maze which include the start, end, path, width, height
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
		self.dfscost = -1
		self.dfspath = []
		return

	#Input : Maze, txt file containing maze
	#Output: Maze list
	#Description: In this function, we read the txt file of maze line by line, 
	# and store the maze structure in a 2D list. The height and width of maze
	# are recorded too.
	def readmaze(self,filename):
		self.graph= []
		with open(filename,"r") as fp:
			for line in fp:
				self.graph.append(list(line[0:len(line)-1]))
		fp.close()
		self.height = len(self.graph)-1
		self.width = len(self.graph[0])
		return

	#Input : Maze
	#Output: None
	#Description: In this function, we travel all point of the maze list and find
	# the x, y poistion of 'P' in the maze. The position of 'P' will be recorded
	# in startx and starty
	def findStart(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]== 'P':
					self.startx=i
					self.starty=j
					break
		return

	#Input:
	#Output:
	#Description:		
	def heuristic(self, x, y, xg, yg):
		return abs(y-yg)+abs(x-xg)

	#Input : Maze
	#Output: None
	#Description: In this function, we aims to find the target point of maze.
	# After traveral the 2D maze list, we record the target point as goalx 
	# and goaly
	def findGoal(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]== '.':
					self.goalx.append(i)
					self.goaly.append(j)
					break
		return

	#Input : Maze
	#Output: x position, y poistion, direction want to travel
	#Description: This function is used to check if there is a boundary for a given
	# position we want to travel, if the direction has no block , we return True,
	# else a Flase warining is returned.
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

	#Input: 
	#Output:
	#Description:
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

	#Input:
	#Output:
	#Description:
	def Astar(self):
		counter=0
		self.path=[]
		q = queue.PriorityQueue()
		discover = dict()
		self.explored=np.zeros(self.height*self.width)
		self.explored[self.startx+(self.starty)*self.width]=1
		q.put((self.heuristic(self.startx, self.starty, self.goalx[0], self.goaly[0]),(self.startx,self.starty,0)))
		while not q.empty():
#			print("here")
			counter+=1
			temp2= q.get()[1]
			current=(temp2[0],temp2[1])
			cost=temp2[2]
			x=current[0]
			y=current[1]
#			print("Astarxy",x,y)
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

	#Input : maze
	#Output: path of maze or a false alarm
	#Description: In this function, we apply BFS algorithm to get the path of a maze
	def bfs(self):
		counter =0
		self.path=[]
		q = queue.Queue() #make a queue to help us record the point that meet first
		discover = dict() #make a dict help us to do the back tracking
		self.explored=np.zeros(self.height*self.width) # make a explored map to find if the point is visited
		self.explored[self.startx+(self.starty)*self.width]=1
		q.put((self.startx,self.starty)) # put the start point to queue
		while not q.empty():
			counter+=1
			current = q.get() #pop a point from queue
			x=current[0]
			y=current[1]
			#if the target position is found, return the path
			if current[0] == self.goalx[0] and current[1]==self.goaly[0]:
				while current != (self.startx,self.starty):
					temp = discover[current[0]+current[1]*self.width]
					current = (temp%self.width,temp//self.width)
					self.path.insert(0,current)
				return counter
				#for every point we pop from queue, check the four directions,
				#if we can travel through direction a, enque the point on direction a
				#mark the current point as visited, and recode the step before to the
				#discovery dictionary
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

	#Input : maze
	#Output: none
	#Description: In this function, we read the solution of the maze and 
	# write it to a txt file
	def drawsol(self):
		for i in range(len(self.path)):
			self.graph[self.path[i][1]][self.path[i][0]]='.'
		self.graph[self.starty][self.startx]='P'
		with open('maze_result.txt', 'w') as f:#open a file and write the solution
			sys.stdout = f
			for line in self.graph:
				print(''.join(line))
		f.close()
		return

	#Input : maze
	#Output: stack that containing the path of the maze or false alarm.
	#Description: In this function, we applied DFS algorithm to the maze
	# to get the solution
	def DFS(self):
		# Use list as stack, find single goal, change maze, return nodes expanded
		graph = copy.deepcopy(self.graph)  #make a copy to help us marked the visited point of the maze
		x = self.startx
		y = self.starty
		node = 0
		if x == -1 or y == -1:
			return -1
		stack = [(x, y, [])] # tuple = (x-cood,y-cood,path)
		while (stack != []): 
			curr = stack.pop() # pop a point from the stack and do the following:
			x = curr[0]
			y = curr[1]
			node += 1
			if graph[x][y] == '.':	# if the targe point is found, return the path 
				self.dfspath = curr[2]
				self.dfscost = len(curr[2])
				return node
			if graph[x][y] == '*': # if therer is wall at the direction we want to go, do not go
				continue
			# Add
			graph[x][y] = '*' # travelsal every direction and push it to the stack
			if self.canTravel(y, x, 0):
				stack += [(x - 1, y, curr[2].copy() + [0])]
			if self.canTravel(y, x, 1):
				stack += [(x + 1, y, curr[2].copy() + [1])]
			if self.canTravel(y, x, 2):
				stack += [(x, y - 1, curr[2].copy() + [2])]
			if self.canTravel(y, x, 3):
				stack += [(x, y + 1, curr[2].copy() + [3])]
		return -1	#if no path is found, return a negative 1 alarm

	#Input : maze
	#Output: none
	#Description: print the maze on the terminal
	def printMaze(self):
		print("printMaze")
		for line in self.graph:
			print(''.join(line))

	#Input : maze
	#Output: none
	#Description: for the path we recorded, use '.' to replace the ' '
	# in the graph
	def drawPath(self):
		path = self.dfspath.copy()
		curx = self.startx
		cury = self.starty
		for x in path:
			if x == 0:
				curx -= 1
				self.graph[curx][cury] = '.'
			elif x == 1:
				curx += 1
				self.graph[curx][cury] = '.'
			elif x == 2:
				cury -= 1
				self.graph[curx][cury] = '.'
			else:
				cury += 1
				self.graph[curx][cury] = '.'
		return

#main function
a=maze()
a.readmaze('mediummaze.txt')

#for i in range(a.height):
#	print(a.graph[i])
a.findGoal()
a.findStart()
print(a.Astar())
print(a.greedy())
print(a.bfs())

#print(a.graph[21][5])
b = a.DFS()
print(b)
a.drawPath()
a.printMaze()
a.drawsol()


		
