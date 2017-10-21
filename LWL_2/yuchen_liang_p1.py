import os
import math
import numpy as np
import queue
import sys
import copy

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
		if x - 1>=0:
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
a.printgraph()
print(a.next_variable())
