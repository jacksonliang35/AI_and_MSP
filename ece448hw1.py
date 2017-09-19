import os


class maze:
	"""docstring for maze"""
	def __init__(self, graph=[], height=0, width=0, explored=[], path=[], tree=[]):
		return
	def readmaze(self,filename):
		self.graph= []
		with open("mediumMaze.txt","r") as fp:
			for line in fp:
				self.graph.append(line[0:len(line)-2])
		fp.close()
		self.height = len(self.graph)
		self.width = len(self.graph[0])
		return

a=maze()
a.readmaze('mediummaze.txt')
print(a.graph)

		