import os


class maze:
	"""docstring for maze"""
	def __init__(self, graph=[], height=0, width=0, explored=[], path=[], tree=[], goalx=[], goaly=[],startx,starty):
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
		for i in range(width):
			for j in range(height):
				if self.graph[j][i]= 'P':
					self.x=i
					self.y=j
					break
		return

	def findGoal(self):
		for i in range(width):
			for j in range(height):
				if self.graph[j][i]= 'P':
					self.goalx.append(i)
					self.goaly.append(j)
					break
		return

	def canTravel(self,x, y, dir):
		if (x < 0) or (y < 0) or (x >= _width) or (y >= _height):
			return False
		if (dir == 0 and y == 0) or (dir == 1 and y == height - 1) or (dir == 2 and x == 0) or (dir == 3 and x == width - 1):
			return False;
		if dir == 0:#up
			return (self.graph[x][y-1]!='%')
		if dir == 1 :#down
			return (self.graph[x][y+1]!='%')
		if dir == 2 :#left
			return (self.graph[x-1][y]!='%')
    	if dir == 3 :#right
    		return (self.graph[x+1][y]!='%')


a=maze()
a.readmaze('mediummaze.txt')
for i in range(a.height):
	print(a.graph[i])



		