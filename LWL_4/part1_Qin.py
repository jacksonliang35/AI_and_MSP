import os
import numpy as np

class digit:
    def __init__(self,image,label):
        self.img = image
        self.lab = label
        self.val = np.zeros((28,28))
        for i in range(28):
            for j in range(28):
                if image[i][j] == '+' or image[i][j] == '#':
                    self.val[i,j] = 1
        return

    def printimg(self):
        for line in self.img:
            print(''.join(line))
        return

def readfile(path,choice):
    # path = './digitdata/'
    # choice = 'training' or 'testing'
    # returns a list of digit object
    labf = open(path+choice+'labels','r')
    imgf = open(path+choice+'images','r')
    labels = []
    images = []
    image = []
    count = 0
    for line in labf:
        labels.append(int(line[0]))
    for line in imgf:
        image.append(list(line)[0:28])
        count += 1
        if count % 28 == 0:
            images.append(image)
            image = []
    labf.close()
    imgf.close()
    # Group into digits
    digitset = []
    for i in range(len(labels)):
        digitset.append(digit(images[i],labels[i]))
    return digitset

if __name__ == '__main__':
    # Import data
    trainset = readfile('./digitdata/','training')
    testset = readfile('./digitdata/','test')

    # Train
    
