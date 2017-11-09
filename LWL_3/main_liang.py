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

def calc_log_prob(F,B,O):
    log_sum = 0
    for i in range(28):
        for j in range(28):
            if O[i,j] == 1:
                log_sum += np.log(F[i,j])
            else:
                log_sum += np.log(B[i,j])
    return log_sum

if __name__ == '__main__':
    # Import data
    trainset = readfile('./digitdata/','training')
    testset = readfile('./digitdata/','test')

    # Train
    trainset_sorted = sorted(trainset, key=lambda digit: digit.lab)
    k = 1     # Smoothing hyperparameter
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
    foreprob[9] = (foreprob[9] + k) / (priors[9] + 2*k)   # w/ Laplace smoothing
    backprob[9] /= priors[9]   # need not smoothing
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
            mapprob[i,cl] = np.log(priors[cl]) + calc_log_prob(foreprob[cl],backprob[cl],digit.val)
            #print(mapprob[i,cl])
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
    # Find Prototypes
    maxind = np.zeros(10)
    minind = np.zeros(10)
    for i in range(10):
        maxind[i] = np.argmax(mapprob[:,i])
        minind[i] = np.argmin(mapprob[:,i])
    print('The most prototypical indexes:')
    print(maxind)
    print('The least prototypical indexes:')
    print(minind)
    # Find Odds Ratio
    odds = np.zeros((10,10,28,28))  # class 1, class 2, i, j
    for c1 in range(10):
        for c2 in range(10):
            for i in range(28):
                for j in range(28):
                    odds[c1,c2,i,j] = foreprob[c1][i,j]/foreprob[c2][i,j]
