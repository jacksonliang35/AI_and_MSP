import os
import numpy as np

def readfile(path,yes=True,train=True):
    # path = './yesno/'
    # returns a list of words, represented by numpy matrix
    if yes:
        yesno = 'yes'
    else:
        yesno = 'no'
    if train:
        traintest = 'train'
    else:
        traintest = 'test'
    fp = open(path+yesno+'_'+traintest+'.txt','r')
    wordset = []
    count = 0
    for line in fp:
        if count == 0:
            word = np.zeros((25,10))
        if count < 25 and count >= 0:
            linelist = list(line[0:10])
            for i in range(10):
                if linelist[i] == ' ':
                    word[count,i] = 1.0
        elif count == 25:
            wordset.append(word)
            count = -3
        count += 1
    fp.close()
    return wordset

def calc_log_prob(P,O):
    log_sum = np.zeros(2)
    for i in range(25):
        for j in range(10):
            if O[i,j] == 1:
                log_sum += np.log(np.array([P[0][i,j],P[1][i,j]]))
            else:
                log_sum += np.log(1-np.array([P[0][i,j],P[1][i,j]]))
    return log_sum

if __name__ == '__main__':
    # Import Data
    path = './yesno/'
    trainset = [readfile(path,False,True),readfile(path,True,True)]     # [no,yes]
    testset = [readfile(path,False,False),readfile(path,True,False)]    # [no,yes]

    # Train
    for k in [.1,.2,.3,.4,.5,1,2,3,5,10]:
        priors = np.array([len(trainset[0]),len(trainset[1])])
        prob_map = [np.zeros((25,10))]*2
        # training no
        for w in trainset[0]:
            prob_map[0] = prob_map[0] + w
        # training yes
        for w in trainset[1]:
            prob_map[1] = prob_map[1] + w
        # Calculate instance probability w/ Smoothing
        prob_map[0] = (prob_map[0]+k)/(priors[0]+2*k)
        prob_map[1] = (prob_map[1]+k)/(priors[1]+2*k)
        # Calculate prior probability
        priors = priors / sum(priors)

        #################################################################
        # Test
        confusion = np.zeros((2,2))
        testtotal = len(testset[0])+len(testset[1])
        i = 0
        mapprob = np.zeros((testtotal,2))
        # test no
        for word in testset[0]:
            # Calculate MAP probability
            mapprob[i,:] = np.log(priors) + calc_log_prob(prob_map,word)
            # Classify
            classify = np.argmax(mapprob[i,:])
            # Counting occurence
            confusion[0,classify] += 1
            i += 1
        # test yes
        for word in testset[1]:
            # Calculate MAP probability
            mapprob[i,:] = np.log(priors) + calc_log_prob(prob_map,word)
            # Classify
            classify = np.argmax(mapprob[i,:])
            # Counting occurence
            confusion[1,classify] += 1
            i += 1
        # Accuraccy
        class_count = np.sum(confusion,axis=1)
        overall_accur = sum(np.diag(confusion))/testtotal
        for i in range(2):
            confusion[i,:] /= len(testset[i])
        accur = np.diag(confusion)

        # Print Results
        np.set_printoptions(precision=3)
        print('The corresponding k is:',end='')
        print(k)
        print('The overall accuracy is: ',end='')
        print(overall_accur)
        print()
#        print('The confusion matrix is:')
#        print(confusion)

