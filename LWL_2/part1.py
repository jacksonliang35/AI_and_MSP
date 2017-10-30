import os
import math
import numpy as np
import queue
import sys
import copy
import time
from collections import deque
class flowfree:
	#We use a structure to record the basic information of graph which include the color position, width, height
	def __init__(self, graph=[], height=0, width=0, colors=[], color2pos=dict(), pos2color=dict(),boundary=np.zeros((0,0))):
		self.graph=[]
		self.height=0
		self.width=0
		self.colors=[]
		self.color2pos=dict()
		self.pos2color=dict()
		self.boundary = np.zeros((0,0))
		return

	#Input : graph, txt file containing maze
	#Description: In this function, we read the txt file of graph line by line,
	# and store the maze structure in a 2D list. The height and width of maze
	# are recorded too.
	def readgraph(self,filename):
		self.graph= []
		with open(filename,"r") as fp:
			for line in fp:
				self.graph.append(list(line[0:len(line)-1]))
		fp.close()
		# Construct height & width
		self.height = len(self.graph)
		self.width = len(self.graph[0])
		# Construct Boundary
		self.boundary = np.zeros((self.width,self.height))
		for k in range(self.width):
			self.boundary[0][k] = 1	
			self.boundary[self.height-1][k] = 1
		for k in range(self.height):
			self.boundary[k][0] = 1
			self.boundary[k][self.width-1] = 1
		return

	#Input : graph
	#Output: None
	#Description: In this function, we travel all point of the graph and find colors and its corresponding position

	def findcolors(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]!= '_':
					self.pos2color[(j,i)] = self.graph[j][i]
					if self.graph[j][i] not in self.colors:
						self.colors.append(self.graph[j][i])
						self.color2pos[self.graph[j][i]]=[(j,i)]
					else:
						self.color2pos[self.graph[j][i]].append((j,i))
		return


	#Input : graph
	#Output: none
	#Description: print the graph on the terminal
	def printgraph(self):
		for line in self.graph:
			print(''.join(line))

	def var_constrain(self,pos):
		x,y=pos[0],pos[1]
		barricade=[]
		if x-1>=0:
			if self.graph[x-1][y]=='_':
				barricade.append((x - 1,y))
		if x + 1<self.height:
			if self.graph[x+1][y]=='_':
				barricade.append((x + 1, y))
		if y - 1 >= 0:
			if self.graph[x][y-1]=='_':
				barricade.append((x, y - 1))
		if y + 1 < self.width:
			if self.graph[x][y+1]=='_':
				barricade.append((x, y + 1))
		return barricade

	def isconnected(self, start, goal):

		height = self.height
		width  = self.width

		startx, starty = start[0], start[1]
		goalx, goaly = goal[0], goal[1]

		qx = deque([])
		qy = deque([])

		tracex = np.zeros((height, width))
		tracey = np.zeros((height, width))
		visited = np.zeros((height, width))

		for i in range(0, height):
			for j in range(0, width):
				if self.graph[i][j] != '_':
					visited[i][j] = 1
		#print(visited)
		visited[goalx][goaly]=0
		curx = startx
		cury = starty

		qx.append(curx)
		qy.append(cury)
		visited[curx][cury] = 2

		dirx = [1, 0, -1, 0]
		diry = [0, 1, 0, -1]
		flag=False

		while len(qx) != 0:
			#print(visited)
			curx = qx.popleft()
			cury = qy.popleft()
			#print(curx,cury)
			if curx == goalx and cury == goaly:
				flag=True
				break

			for i in range(0, 4):
				tempx = curx + dirx[i]
				tempy = cury + diry[i]

				if tempx < 0 or tempx >= height or tempy < 0 or tempy >= width:
					continue

				if visited[tempx][tempy] == 0:
					tracex[tempx][tempy] = curx
					tracey[tempx][tempy] = cury
					visited[tempx][tempy] = 2
					qx.append(tempx)
					qy.append(tempy)
		return flag



	def canTravel(self, x, y, dir,color):
		if (x < 0) or (y < 0) or (x >= self.height) or (y >= self.width):
			return False
		elif (dir == 0 and x == 0) or (dir == 1 and x == self.height - 1) or (dir == 2 and y == 0) or (
				dir == 3 and y == self.width - 1):
			return False
		elif dir == 0:  # up
			return (self.graph[x - 1][y] == '_' or self.graph[x - 1][y] == color)
		elif dir == 1:  # down
			return (self.graph[x + 1][y] == '_' or self.graph[x + 1][y] == color)
		elif dir == 2:  # left
			return (self.graph[x][y - 1] == '_' or self.graph[x][y - 1] == color)
		elif dir == 3:  # right
			return (self.graph[x][y + 1] == '_' or self.graph[x][y + 1] == color)

	def Search(self,color,depth):
		cost=0
		path = []
		pathlist=[]

		# Decide start and goal
		index=1
		if len(self.var_constrain(self.color2pos[color][0])) > len(self.var_constrain(self.color2pos[color][1])):
			index = 1
		else:
			index =0
		start = self.color2pos[color][index]	# Start at the node with more constraint
		index2=0
		if index ==1:
			index2=0
		else:
			index2=1
		goal = self.color2pos[color][index2]	# End at the node with less constraint

		# Set up explored
		explored = np.zeros((self.height, self.width))
		explored[start[0], start[1]] = 1
		q = queue.PriorityQueue()
		path.append(start)
		# push
		q.put((0,start,path,explored))
		"""
		if color=='O' and depth == 0:
			print('-------------------------------')
			print(self.boundary)
			print('-------------------------------')
		"""
		while not q.empty():
			state = q.get()
			cost = state[0]
			pos = state[1]
			x=pos[0]
			y=pos[1]
			path1 = state[2]
			explored = state[3]
			if self.has_zigzag(explored,path1,start,goal):
				continue

			nbd2bd = 1		# i.e. not (boundary to boundary)

			# Goal State
			if cost > depth:
				return pathlist
			if pos==goal:
				if cost==depth: #only return specified depth path
					pathlist=pathlist+[path1]
				continue


			if self.canTravel(x, y, 0,color):
				if explored[x - 1, y] == 0:
					exploredtemp=copy.deepcopy(explored)
					exploredtemp[x - 1, y] = 1
					nextpath = path1+[(x-1,y)]
					if self.boundary[x-1,y] == 1 and self.boundary[x,y] == 1: #if boundary to boundary cost=0
						nbd2bd = 0
					q.put((cost+nbd2bd,(x-1,y),nextpath,exploredtemp))

			if self.canTravel(x, y, 1,color):
				if explored[x + 1, y] == 0:
					exploredtemp=copy.deepcopy(explored)
					exploredtemp[x + 1, y] = 1
					nextpath = path1+[(x+1,y)]
					if self.boundary[x+1,y] == 1 and self.boundary[x,y] == 1: #if boundary to boundary cost=0
						nbd2bd = 0
					q.put((cost+nbd2bd,(x+1,y),nextpath,exploredtemp))

			if self.canTravel(x, y, 2,color):
				if explored[x, y - 1] == 0:
					exploredtemp=copy.deepcopy(explored)
					exploredtemp[x, y-1] = 1
					nextpath = path1+[(x,y-1)]
					if self.boundary[x,y-1] == 1 and self.boundary[x,y] == 1: #if boundary to boundary cost=0
						nbd2bd = 0
					q.put((cost+nbd2bd,(x,y-1),nextpath,exploredtemp))

			if self.canTravel(x, y, 3,color):
				if explored[x, y + 1] == 0:
					exploredtemp=copy.deepcopy(explored)
					exploredtemp[x, y+1] = 1
					nextpath = path1+[(x,y+1)]
					if self.boundary[x,y+1] == 1 and self.boundary[x,y] == 1: #if boundary to boundary cost=0
						nbd2bd = 0
					q.put((cost+nbd2bd,(x,y+1),nextpath,exploredtemp))
		return pathlist

	def has_zigzag(self,explored,path,start,goal):
		for p in path:
			x = p[0]
			y = p[1]
			sum = 0
			if x>0:
				sum += explored[x-1,y]
			if x<self.height-1:
				sum += explored[x+1,y]
			if y>0:
				sum += explored[x,y-1]
			if y<self.width-1:
				sum += explored[x,y+1]
			if (p==start or p==goal) and sum>1:
				return True
			if sum>2:
				return True
		return False

	def backtracking_smart(self):
		if self.backtracking_h_smart():
			for line in self.graph:
				print(''.join(line))

	def backtracking_dumb(self):
		if self.backtracking_h_dumb():
			for line in self.graph:
				print(''.join(line))

	def change_boundary(self,path):
		#print()
		for i in path:
			x=i[0]
			y=i[1]
			if x - 1 >= 0 and y - 1 >= 0: # set surrounding area to be boundary
				if self.boundary[x-1,y-1] == 0:
					self.boundary[x-1,y-1] = 1
			if x - 1 >= 0:
				if self.boundary[x-1,y] == 0:
					self.boundary[x-1,y] = 1
			if x + 1 < self.height:
				if self.boundary[x+1,y] == 0:
					self.boundary[x+1,y] = 1
			if x + 1 < self.height and y - 1 >= 0:
				if self.boundary[x+1,y] == 0:
					self.boundary[x+1,y-1] = 1
			if y - 1 >= 0:
				if self.boundary[x,y-1] == 0:
					self.boundary[x,y-1] = 1
			if y + 1 < self.width:
				if self.boundary[x,y+1] == 0:
					self.boundary[x,y+1] = 1
			if x + 1 < self.height and y + 1 <self.width:
				if self.boundary[x+1,y+1] == 0:
					self.boundary[x+1,y+1] = 1
			if x - 1 >= 0 and y + 1 < self.width:
				if self.boundary[x-1,y+1] == 0:
					self.boundary[x-1,y+1] = 1
		for i in path:
			self.boundary[i[0],i[1]] = 2
		"""
		for x in range(self.height):
			for y in range(self.width):
				if self.graph[x][y] != '_' :
					self.boundary[x,y] = 0 # not a boundary if a path is applied
		"""


	def change_graph(self,path,color):
		for i in path:
			self.graph[i[0]][i[1]] = color
		#print graph
		
		for line in self.graph:
			print(''.join(line))
		print()
		

	def backtracking_h_dumb(self):
		temp=np.arange(len(self.colors))
		np.random.shuffle(temp)
		color=self.colors[temp[0]] 
		Search_result=[]
		for i in range(4*self.width):
			Search_result=self.Search(color,i)# search for the paths with constant cost return a list according to priority
			for path in Search_result:
                #change graph,boundary,colors
				tempg=copy.deepcopy(self.graph)
				tempb=copy.deepcopy(self.boundary)
				tempc=copy.deepcopy(self.colors)
				self.change_boundary(path)
				self.change_graph(path,color)
				self.colors=[self.colors[i] for i in range(len(self.colors)) if self.colors[i] != color] #change color
				if self.is_complete():
					return True
				result = self.backtracking_h_dumb()
				if result != False:
					return result
				self.graph=tempg #restore graph,boundary,colors
				self.boundary=tempb
				self.colors=tempc
		return False



	def backtracking_h_smart(self):
		color = self.next_variable() # choose which variable to assign
		Search_result=[]
		for i in range(4*self.width):
			Search_result=self.Search(color,i)# search for the paths with constant cost return a list according to priority
			"""
			if color=='O':
				print(i)
				print(Search_result)
				print('--------------------')
			"""
			for path in Search_result:
                #change graph,boundary,colors
				tempg=copy.deepcopy(self.graph)
				tempb=copy.deepcopy(self.boundary)
				tempc=copy.deepcopy(self.colors)
				self.change_boundary(path)
				self.change_graph(path,color)
				self.colors=[self.colors[i] for i in range(len(self.colors)) if self.colors[i] != color] #change color
				if self.is_complete():
					return True
				if not self.will_fail():
					result = self.backtracking_h_smart()
					if result != False:
						return result
				self.graph=tempg #restore graph,boundary,colors
				self.boundary=tempb
				self.colors=tempc
		return False


	def is_complete(self):
		for line in self.graph:
			for c in line:
				if c == '_':
					return False
		return True

	def next_variable(self):
		colors = self.color2pos
		# Check openings
		op = dict()
		for c in colors:
			if c in self.colors:
				#op[c] = len(self.var_constrain(colors[c][0]))*len(self.var_constrain(colors[c][1]))
				a=len(self.Search(c,0))
				if a ==0:
					op[c] = len(self.var_constrain(colors[c][0]))*len(self.var_constrain(colors[c][1]))
				else:
					op[c]=a

		return min(op, key=op.get)

	def will_fail(self):
		# Check color connectedness
		for c in self.colors:
			if not self.isconnected(self.color2pos[c][0],self.color2pos[c][1]):
				return True
		# Check empty set
		boundcopy = copy.deepcopy(self.boundary)
		for i in range(self.height):
			for j in range(self.width):
				if self.has_empty_set(boundcopy,i,j):
					return True
		return False


	def has_empty_set(self,boundary,i,j):
		if boundary[i,j] > 1:
			return False
		h = self.height
		w = self.width
		no_color = True
		q = queue.Queue()
		q.put((i,j))
		while not q.empty():
			pos = q.get()
			x = pos[0]
			y = pos[1]
			# Check if it is a color position
			if self.graph[x][y] != '_':
				no_color = False
			# Change boundary map value
			boundary[x,y] = 3
			# Push neighbors into the queue
			if x>0 and boundary[x-1,y]<2:
				q.put((x-1,y))
			if x<h-1 and boundary[x+1,y]<2:
				q.put((x+1,y))
			if y>0 and boundary[x,y-1]<2:
				q.put((x,y-1))
			if y<w-1 and boundary[x,y+1]<2:
				q.put((x,y+1))
		return no_color



a=flowfree()
a.readgraph('input991.txt')
a.printgraph()
a.findcolors()
a.printgraph()
start = time.time()
a.backtracking_smart()
end = time.time()
print(end - start)
