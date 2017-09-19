import os

l = []
with open("mediumMaze.txt","r", encoding="utf-8") as fp:
    for line in fp:
        l.append(line)
fp.close()
