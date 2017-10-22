import os
import math
import numpy as np
import queue
import sys
import copy
from collections import deque
class flowfree:
	#We use a stracture to record the basic information of graph which include the color position, width, height
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
		self.height = len(self.graph)
		self.width = len(self.graph[0])
		self.boundary = np.zeros((self.width,self.height))
		# Assuming square graph
		for k in range(self.width):
			self.boundary[0][k] = 1
			self.boundary[k][0] = 1
			self.boundary[self.width-1][k] = 1
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

	def LBFS(self, start, goal, depth):

		height = self.height
		width  = self.width

		startx, starty = start[0], start[1]
		goalx, goaly = goal[0], goal[1]
		print('start')
		print(startx,starty)
		pathlist = []
		qx = deque([])
		qy = deque([])

		tracex = np.zeros((height, width))
		tracey = np.zeros((height, width))
		visited = np.zeros((height, width))

		for i in range(0, height):
			for j in range(0, width):
				if self.graph[i][j] != '_':
					visited[i][j] = 1

		curx = startx
		cury = starty

		qx.append(curx)
		qy.append(cury)
		visited[curx][cury] = 2

		dirx = [1, 0, -1, 0]
		diry = [0, 1, 0, -1]

		while len(qx) != 0:
			curx = qx.popleft()
			cury = qy.popleft()

			curpath = self.getPath(tracex, tracey, startx, starty, curx , cury)
			print('get one')
			print(curpath)
			if curx == goalx and cury == goaly and len(path) == depth:
				pathlist.append(curpath)
				continue
			print('113')
			if len(curpath) > depth:
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
			print('129')
		return pathlist

	def getPath(self, tracex, tracey, s_row, s_col, e_row, e_col):

		flag = 0
		pathx = []
		pathy = []
		print(tracex)
		print(tracey)
		print('138')
		if np.sum(tracex) == 0: return pathx

		pathx.append(e_row)
		pathy.append(e_col)
		a = tracex[e_row][e_col]
		b = tracey[e_row][e_col]
		ad = 0
		temx = a
		temy = b
		#print(type(temx),temx,temy,tracex[int(temx)][int(temy)])
		#return pathx
		print(s_row,s_col)
		temx = int(temx)
		temy = int(temy)
		curpath = []
		print(temx,temy)
		if temx == s_row and temy == s_col:
			curpath.append((temx,temy))
			curpath.append((s_row,s_col))
			return curpath
		while flag == 0:
			#print('151')
			temx=int(temx)
			temy=int(temy)
			#print(temx,temy)
			pathx.append(temx)
			pathy.append(temy)

			chex = tracex[temx][temy]
			chey = tracey[temx][temy]

			temx = chex
			temy = chey

			#print(temx,temy)
			if temx == s_row and temy == s_col:
				# print("here")
				pathx.append(s_row)
				pathy.append(s_col)
				flag = 1
				break
		pathx.reverse()
		pathy.reverse()

		for i in range(0, len(pathx)):
			curpath.append((pathx[i], pathy[i]))
		return curpath


	def canTravel(self, x, y, dir,color):
		if (x < 0) or (y < 0) or (x >= self.height) or (y >= self.width):
			return False
		elif (dir == 0 and x == 0) or (dir == 1 and x == self.height - 1) or (dir == 2 and y == 0) or (
				dir == 3 and y == self.width - 1):
			return False;
		elif dir == 0:  # up
			return (self.graph[x - 1][y] == '_' or self.graph[x - 1][y] == color )
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
		index=1
		if len(self.var_constrain(self.color2pos[color][0])) > len(self.var_constrain(self.color2pos[color][1])):
			index = 1
		else:
			index =0
		start = self.color2pos[color][index]
		index2=0
		if index ==1:
			index2=0
		else:
			index2=1

		goal = self.color2pos[color][index2]

		# Set up goal counter & explored
		explored = np.zeros((self.height, self.width))
		explored[start[0], start[1]] = 1
		q = queue.PriorityQueue()
		path.append(start)
		# push evaluation, length of goal , (counter,), cost (pathlength) ,position, path, goalc, explored, mstsum
		q.put((0,start,path))
		while not q.empty():
			state = q.get()
			cost = state[0]
			pos = state[1]
			x=pos[0]
			y=pos[1]
			path1 = state[2]
			temp=1
			if self.boundary[x,y] ==1:
				temp=0
			# Goal State
			if cost > depth:
				return pathlist
			if pos==goal:
				path1.append(goal)
				pathlist=pathlist+path1
				continue
				# Recalculating MST
			if self.canTravel(x, y, 0,color):
				if explored[x - 1, y] == 0:
					explored[x - 1, y] = 1
					q.put((cost+temp,(x-1,y),path1+[(x-1,y)]))

			if self.canTravel(x, y, 1,color):
				if explored[x + 1, y] == 0:
					explored[x + 1, y] = 1
					q.put((cost + temp, (x + 1, y), path1 + [(x + 1, y)]))

			if self.canTravel(x, y, 2,color):
				if explored[x, y - 1] == 0:
					explored[x, y - 1] = 1
					q.put((cost + temp, (x, y-1), path1 + [(x, y - 1)]))

			if self.canTravel(x, y, 3,color):
				if explored[x, y + 1] == 0:
					explored[x, y + 1] = 1
					q.put((cost + temp, (x , y+1), path1 + [(x, y+1)]))
		return -1

	def backtracking(self):
		if self.backtracking_h():
			for line in self.graph:
				print(''.join(line))

	def change_boundary(self,path):
		for i in path:
			x=i[0]
			y=i[1]
			if x - 1 >= 0 and y - 1 >= 0: # set surrounding area to be boundary
				if self.graph[x-1][y-1] == '_' :
					self.boundary[x-1,y] = 1
			if x - 1 >= 0:
				if self.graph[x-1][y] == '_' :
					self.boundary[x-1,y] = 1
			if x + 1 < self.height:
				if self.graph[x+1][y] == '_' :
					self.boundary[x+1,y] = 1
			if x + 1 < self.height and y - 1 >= 0:
				if self.graph[x+1][y-1] == '_' :
					self.boundary[x-1,y-1] = 1
			if y - 1 >= 0:
				if self.graph[x][y-1] == '_' :
					self.boundary[x,y-1] = 1
			if y + 1 < self.width:
				if self.graph[x][y+1] == '_' :
					self.boundary[x,y+1] = 1
			if x + 1 < self.height and y + 1 <self.width:
				if self.graph[x+1][y+1] == '_' :
					self.boundary[x+1,y+1] = 1
			if x - 1 >= 0 and y + 1 < self.width:
				if self.graph[x-1][y+1] == '_' :
					self.boundary[x-1,y+1] = 1

		for x in range(self.height):
			for y in range(self.width):
				if self.graph[x][y] != '_' :
					self.boundary[x,y] = 0 # not a boundary if a path is applied



	def change_graph(self,path,color):
		for i in path:
			self.graph[i[0]][i[1]] = color
		for line in self.graph:
			print(''.join(line))


	def backtracking_h(self):
		if self.is_complete(): # find all of the paths
			return True
		color = self.next_variable() # choose which variable to assign
		Search_result=[]
		for i in range(0,int(4*self.width)):
			temp=self.Search(color,i)
			if temp==[] or temp==-1:
				continue
			Search_result+=[temp]# search for the paths return a list according to priority
		for path in Search_result:
			#if path is consistant:
			#change graph,boundary,colors
			tempg=copy.deepcopy(self.graph)
			tempb=copy.deepcopy(self.boundary)
			tempc=copy.deepcopy(self.colors)
			self.change_boundary(path)
			self.change_graph(path,color)
			self.colors=[self.colors[i] for i in range(len(self.colors)) if self.colors[i] != color]
			result = self.backtracking_h()
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

		# Check both on boundary
		# Check openings
		op = dict()
		for c in colors:
			if c in self.colors:
				op[c] = len(self.var_constrain(colors[c][0]))*len(self.var_constrain(colors[c][1]))
		return min(op, key=op.get)
"""
	def will_fail(self):
		# Check color connectedness
		for

def next_bound(graph,pastpos,curr):
	# pastpos = {0,1,2,3} = {up,right,down,left}
	x = curr[0]
	y = curr[1]
	for i in range(1,4)+[pastpos]*4:
		if (i%4 == 0 and x>0 and graph[x-1][y]==1):
			return (x-1,y)
		if (i%4 == 1 and y<graph.width-1 and graph[x][y+1]==1):
			return (x,y+1)
		if (i%4 == 2 and x<graph.height-1 and graph[x+1][y]==1):
			return (x+1,y)
		if (i%4 == 3 and y>0 and graph[x][y-1]==1):
			return (x,y-1)
"""

a=flowfree()
a.readgraph('input77.txt')
a.findcolors()
print(a.colors)
print(a.color2pos)
a.printgraph()
#print(a.colorpos['O'][0][0])
print(a.var_constrain(a.color2pos['O'][0]))

a.backtracking()


		
