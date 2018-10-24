import os
import sys
import numpy as np

class digit:
    def __init__(self,image,label,n=1,m=1,disjoint=True):
        self.img = image
        self.lab = label
        self.val = np.zeros((28,28))
        self.getfeature(n,m,disjoint)
        return

    def getfeature(self,n,m,disjoint):     # n*m = height*width
        if disjoint:
            hstride = n
            wstride = m
            h = 28//n
            w = 28//m
        else:
            hstride = 1
            wstride = 1
            h = 29-n
            w = 29-m
        self.val = np.zeros((h,w))
        for i in range(h):
            for j in range(w):
                for di in range(i*hstride,i*hstride+n):
                    for dj in range(j*wstride,j*wstride+m):
                        if self.img[di][dj] == '+' or self.img[di][dj] == '#':
                            self.val[i,j] = int(2*self.val[i,j]+1)
                        else:
                            self.val[i,j] = int(2*self.val[i,j])
        return


    def printimg(self):
        for line in self.img:
            print(''.join(line))
        return

def readfile(path,choice,n=1,m=1,disjoint=True):
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
        digitset.append(digit(images[i],labels[i],n,m,disjoint))
    return digitset

def calc_log_prob(P,O):
    log_sum = 0
    height,width = P.shape[1:3]
    for i in range(height):
        for j in range(width):
            log_sum += np.log(P[int(O[i,j]),i,j])
    return log_sum

if __name__ == '__main__':
    # Patch Parameters
    n = 2
    m = 2
    disjoint = True

    # Import data
    trainset = readfile('./digitdata/','training',n,m,disjoint)
    testset = readfile('./digitdata/','test',n,m,disjoint)

    # Train
    trainset_sorted = sorted(trainset, key=lambda digit: digit.lab)
    k = 1     # Smoothing hyperparameter
    curlabel = 0
    priors = np.zeros(10)
    height, width = trainset[0].val.shape
    prob_map = np.zeros((10,int(2**(n*m)),height,width))     # (class,value,hidx,widx)
    for digit in trainset_sorted:
        if digit.lab==curlabel:
            priors[curlabel] += 1
            for i in range(height):
                for j in range(width):
                    prob_map[curlabel,int(digit.val[i,j]),i,j] += 1
        else:
            prob_map[curlabel,:,:,:] = (prob_map[curlabel,:,:,:] + k)/(priors[curlabel] + (2**(n*m))*k)
            curlabel += 1
            priors[curlabel] += 1
            for i in range(height):
                for j in range(width):
                    prob_map[curlabel,int(digit.val[i,j]),i,j] += 1
    prob_map[9,:,:,:] = (prob_map[9,:,:,:] + k)/(priors[9] + (2**(n*m))*k)

    # Calculate prior probability
    priors /= 5000

    #################################################################
    # Test
    confusion = np.zeros((10,10))
    i = 0
    mapprob = np.zeros((1000,10))
    for digit in testset:
        # Calculate MAP probability
        for cl in range(10):
            mapprob[i,cl] = np.log(priors[cl]) + calc_log_prob(prob_map[cl,:,:,:],digit.val)
        # Classify
        classify = np.argmax(mapprob[i,:])
        # Counting occurence
        confusion[digit.lab,classify] += 1
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
