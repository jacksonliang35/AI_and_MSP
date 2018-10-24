import os
import scipy.sparse as sps
import queue
import sys

class flow:
    """docstring for maze"""
    def __init__(self, graph=[], height=0, width=0, path=[], goalx=[], goaly=[],startx=0,starty=0):
        self.graph=[]
        self.height=0
        self.width=0
        self.path=[]
        self.goalx=[]
        self.goaly=[]
        self.startx=-1
        self.starty=-1
        return

    def readMaze(self,filename):
         self.graph= []
         with open(filename,"r") as fp:
            for line in fp:
                self.graph.append(list(line[0:len(line)-1]))
         fp.close()
         self.graph[-1].append('%')
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
            if self.startx!=-1:
                break





