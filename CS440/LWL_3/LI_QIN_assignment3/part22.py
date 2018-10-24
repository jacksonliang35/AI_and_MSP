import os
import numpy as np

class word:
    def __init__(self,image,label):
        self.image = image
        self.label = label


def readfile(path,train):
    # path = './yesno/'
    # returns a list of words, represented by numpy matrix
    if train:
        traintest = 'training'
    else:
        traintest = 'testing'
    # Read label
    lp = open(path+traintest+'_labels.txt','r')
    labelset = []
    for line in lp:
        labelset.append(int(line[0]))
    lp.close()
    # Read data
    dp = open(path+traintest+'_data.txt','r')
    wordset = []
    count = 0
    for line in dp:
        if count == 0:
            w = np.zeros((30,13))
        if count < 30 and count >= 0:
            linelist = list(line[0:13])
            for i in range(13):
                if linelist[i] == ' ':
                    w[count,i] = 1
        elif count == 30:
            wordset.append(w)
            count = -3
        count += 1
    dp.close()
    # Group them into total set
    totalset = []
    for i in range(len(labelset)):
        totalset.append(word(wordset[i],labelset[i]))
    return totalset

def calc_log_prob(P,O):
    log_sum = 0
    for i in range(30):
        for j in range(13):
            if O[i,j] == 1:
                log_sum += np.log(P[i,j])
            else:
                log_sum += np.log(1-P[i,j])
    return log_sum

if __name__ == '__main__':
    # Import Data
    path = './data22/'
    trainset = readfile(path,True)
    testset = readfile(path,False)
    # Train
    trainset_sorted = sorted(trainset, key=lambda word: word.label)
    k = 1     # Smoothing hyperparameter
    curlabel = 0
    priors = np.zeros(5)
    prob_map = np.zeros((5,30,13))    # (class,height,width)
    for w in trainset_sorted:
        if w.label==curlabel+1:
            priors[curlabel] += 1
            prob_map[curlabel,:,:] = prob_map[curlabel,:,:] + w.image
        else:
            prob_map[curlabel,:,:] = (prob_map[curlabel,:,:] + k) / (priors[curlabel] + 5*k)   # Laplace smoothing
            curlabel += 1
            priors[curlabel] += 1
            prob_map[curlabel,:,:] = prob_map[curlabel,:,:] + w.image
    prob_map[4,:,:] = (prob_map[4,:,:] + k) / (priors[4] + 5*k)   # Laplace smoothing
    # Calculate prior probability
    priors /= len(trainset)

    #################################################################
    # Test
    confusion = np.zeros((5,5))
    i = 0
    mapprob = np.zeros((len(testset),5))
    for w in testset:
        # Calculate MAP probability
        for cl in range(5):
            mapprob[i,cl] = np.log(priors[cl]) + calc_log_prob(prob_map[cl,:,:],w.image)
        # Classify
        classify = np.argmax(mapprob[i,:])
        # Counting occurence
        confusion[w.label-1,classify] += 1
        i += 1
    # Accuraccy
    class_count = np.sum(confusion,axis=1)
    accur = np.diag(confusion)
    overall_accur = sum(accur)/len(testset)
    accur = np.divide(accur,class_count)
    for i in range(5):
        confusion[i,:] /= class_count[i]
    np.set_printoptions(precision=3)
    print('The overall accuracy is: ',end='')
    print(overall_accur)
    print('The confusion matrix is:')
    print(confusion)
