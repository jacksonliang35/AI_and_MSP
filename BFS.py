import os
import sys
import numpy as np
import queue
from collections import deque
class maze:
	"""docstring for maze"""
	def __init__(self, graph=[], height=0, width=0, explored=[], path=[], tree=[], goalx=0, goaly=0,startx=0,starty=0):
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


a=maze()
a.readmaze('mediummaze.txt')
copy=a.graph
graph=np.asarray(a.graph)

width=len(graph[0])
height=len(graph)
s_row=0
s_col=0
e_row=0
e_col=0
expand=0
visited=np.zeros((height,width))
for i in range(0,len(graph)):
    for j in range(0,len(graph[0])):
        if graph[i][j] == 'P':
            print("start",i,j)
            s_row=i
            s_col=j
        if graph[i][j] == '.':
            print("end",i,j)
            e_row=i
            e_col=j
        if graph[i][j] == '%':
            visited[i][j]=1
qx = deque([])
qy = deque([])

tracex = np.zeros((height,width))
tracey = np.zeros((height,width))
print('tracex',tracex[1][5])
#BFS
#step=0
curx=s_row
cury=s_col
visited[curx][cury]=2
qx.append(curx)
qy.append(cury)
dirx=[1,0,-1,0]
diry=[0,1,0,-1]
oldx = s_row
oldy = s_col
print('width',width,'height',height)
while len(qx)!=0:
    curx=qx.popleft()
    cury=qy.popleft()
    expand+=1

    if curx == e_row and cury == e_col:
        break

    for i in range(0,4):

        tempx = curx + dirx[i]
        tempy = cury + diry[i]
        if tempx<0 or tempx>=height or tempy<0 or tempy>=width:
            continue

        if visited[tempx][tempy] == 0:
            tracex[tempx][tempy] = curx
            tracey[tempx][tempy] = cury
            visited[tempx][tempy] = 2
            qx.append(tempx)
            qy.append(tempy)


flag=0
pathx=[]
pathy=[]

pathx.append(e_row)
pathy.append(e_col)
a = tracex[e_row][e_col]
b = tracey[e_row][e_col]
ad=0
temx=a
temy=b
#print(type(temx))

chex=0
chey=0
while flag==0:
    pathx.append(temx)
    pathy.append(temy)

    chex=tracex[temx][temy]
    chey=tracey[temx][temy]

    temx=chex
    temy=chey

    #print(temx,temy)
    if temx==s_row and temy==s_col:
        #print("here")
        pathx.append(s_row)
        pathy.append(s_col)
        flag=1
        break
pathx.reverse()
pathy.reverse()

for i in range(0,len(pathx)):
    visited[pathx[i]][pathy[i]]=3
visited[s_row][s_col]=4
visited[e_row][e_col]=5

with open('maze_result.txt', 'w') as f:
    sys.stdout = f
    for i in range(0,height):
        for j in range(0,width):
            if visited[i][j]==1:
                print("%",end="")
            elif visited[i][j] == 3:
                print(".", end="")
            elif visited[i][j]== 4:
                print("P",end="")
            elif visited[i][j]==5:
                print(".",end="")
            else:
                print(" ",end="")
        print()
    print("expand",expand)
    print("path_cost",len(pathx))
f.close()
