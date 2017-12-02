import os
import numpy as np
from collections import Counter
class digit:
    def __init__(self,image,label):
        self.img = image
        self.lab = label
        self.val = np.zeros((28,28))
        for i in range(28):
            for j in range(28):
                if image[i][j] == '+' or image[i][j] == '#':
                    self.val[i,j] = 1.0
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
def distL1(x1,x2):
    return np.sum((np.abs(x1-x2)),axis=1)

def distL2(x1,x2):
    return sum((abs(x1**2-x2**2))**0.5,axis=1)

if __name__ == '__main__':
    # Import data
    trainset = readfile('./digitdata/','training')
    testset = readfile('./digitdata/','test')
    # Train
    #################################################################
    trainset_sorted = sorted(trainset, key=lambda x: x.lab)
    dataset = np.zeros((5000,28*28))
    trainlabel = np.zeros(5000)
    for i in range(len(trainset)):
        dataset[i,:] = trainset[i].val.flatten()
        trainlabel[i] = trainset[i].lab

    #Test
    #################################################################
    k=1
    confusion = np.zeros((10,10))
    i = 0
    for testidx in testset:
        # Classify
        neighbors = np.argsort(distL1(dataset,testidx.val.flatten()))[0:k] # k's nearest neighbor
        classify = int(Counter([ trainlabel[j] for j in neighbors]).most_common()[0][0])# most common value
        # Counting occurence
        confusion[testidx.lab,classify] += 1
        i += 1
    # Accuraccy
    class_count = np.sum(confusion,axis=1)
    accur = np.diag(confusion)
    overall_accur = sum(accur)/1000
    accur = np.divide(accur,class_count)
    for i in range(10):
        confusion[i,:] /= class_count[i]
    np.set_printoptions(precision=3)
    print('The overall accuracy is: ',end='')
    print(overall_accur)
    print('The confusion matrix is:')
    print(confusion)
