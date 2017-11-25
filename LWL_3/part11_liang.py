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
            foreprob[curlabel] = (foreprob[curlabel] + k) / (priors[curlabel] + 10*k)   # w/ Laplace smoothing
            backprob[curlabel] /= priors[curlabel]   # need not smoothing
            curlabel += 1
            priors[curlabel] += 1
            foreprob[curlabel] = foreprob[curlabel] + digit.val
            backprob[curlabel] = backprob[curlabel] + (1-digit.val)
    foreprob[9] = (foreprob[9] + k) / (priors[9] + 10*k)   # w/ Laplace smoothing
    backprob[9] /= priors[9]   # need not smoothing
    # Calculate prior probability
    priors /= 5000

    #################################################################
    # Test
    confusion = np.zeros((10,10))
    i = 0
    mapprob = np.zeros((1000,10))
    probval =[[],[],[],[],[],[],[],[],[],[]]
    probimg =[[],[],[],[],[],[],[],[],[],[]]
    probidx =[[],[],[],[],[],[],[],[],[],[]]
    for digit in testset:
        # Calculate MAP probability
        for cl in range(10):
            mapprob[i,cl] = np.log(priors[cl]) + calc_log_prob(foreprob[cl],backprob[cl],digit.val)
        # Classify
        classify = np.argmax(mapprob[i,:])
        val = max(mapprob[i,:])
        probval[classify].append(val)
        probimg[classify].append(digit)
        probidx[classify].append(i)
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
    print('max prob')
    print()
    for i in range(10):
        print('Max Class: ',end='')
        print(i,end='')
        print(' Index: ',end='')
        print(probidx[i][probval[i].index(max(probval[i]))])
        for line in probimg[i][probval[i].index(max(probval[i]))].img:
            print(''.join(line))
        
   
    print('min prob')
    print()
    for i in range(10):
        print('Min Class: ',end='')
        print(i,end='')
        print(' Index: ',end='')
        print(probidx[i][probval[i].index(min(probval[i]))])
        for line in probimg[i][probval[i].index(min(probval[i]))].img:
            print(''.join(line))
    
    '''
    maxind = np.zeros(10)
    minind = np.zeros(10)
    for i in range(10):
        maxind[i] = np.argmax(mapprob[:,i])
        minind[i] = np.argmin(mapprob[:,i])
    print('The most prototypical indexes:')
    print(maxind)

    for i in maxind:
        for line in testset[int(i)].img:
            print(''.join(line))
        print()
    print('The least prototypical indexes:')
    print(minind)

    for i in minind:
        print(testset[int(i)].lab)
        for line in testset[int(i)].img:
            print(''.join(line))
        print()
    '''
    # Find Odds Ratio
    odds = np.zeros((10,10,28,28))  # class 1, class 2, i, j
    for c1 in range(10):
        for c2 in range(10):
            for i in range(28):
                for j in range(28):
                    odds[c1,c2,i,j] = np.log(foreprob[c1][i,j])-np.log(foreprob[c2][i,j])
    import matplotlib.pyplot as plt
    import numpy as np
    '''
    plt.figure()
    plt.imshow(np.log(foreprob[5]),interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(odds[5][3], interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(np.log(foreprob[3]), interpolation='nearest')
    plt.colorbar()
    
    plt.figure()
    plt.imshow(np.log(foreprob[8]),interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(odds[8][3], interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(np.log(foreprob[3]), interpolation='nearest')
    plt.colorbar()
    
    plt.figure()
    plt.imshow(np.log(foreprob[4]),interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(odds[4][9], interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(np.log(foreprob[9]), interpolation='nearest')
    plt.colorbar()
    
    plt.figure()
    plt.imshow(np.log(foreprob[7]),interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(odds[7][9], interpolation='nearest')
    plt.colorbar()
    plt.figure()
    plt.imshow(np.log(foreprob[9]), interpolation='nearest')
    plt.colorbar()
    plt.show()
    '''
