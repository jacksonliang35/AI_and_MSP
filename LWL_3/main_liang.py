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
    # Train
    trainset = readfile('./digitdata/','training')
    trainset_sorted = sorted(trainset, key=lambda digit: digit.lab)
    k = 0.1     # Smoothing hyperparameter
    curlabel = 0
    priors = np.zeros(10)
    foreprob = [np.zeros((28,28))]*10
    backprob = [np.zeros((28,28))]*10
    for digit in trainset_sorted:
        if digit.lab==curlabel:
            priors[curlabel] += 1
            foreprob[curlabel] = foreprob[curlabel] + digit.val
            backprob[curlabel] = backprob[curlabel] + (1-digit.val)
        else:
            foreprob[curlabel] = (foreprob[curlabel] + k) / (priors[curlabel] + 2*k)   # w/ Laplace smoothing
            backprob[curlabel] /= priors[curlabel]   # need not smoothing
            curlabel += 1
            priors[curlabel] += 1
            foreprob[curlabel] = foreprob[curlabel] + digit.val
            backprob[curlabel] = backprob[curlabel] + (1-digit.val)
    # Calculate prior probability
    priors /= 5000
    print(priors)

    # Test
    #testset = readfile('./digitdata/','test')
