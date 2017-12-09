import os
import numpy as np
import matplotlib.pyplot as plt
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

if __name__ == '__main__':
    # Import data
    trainset = readfile('./digitdata/','training')
    testset = readfile('./digitdata/','test')
    # Train
    #################################################################
    trainset_sorted = sorted(trainset, key=lambda x: x.lab)
    
    #w = np.zeros((10,28*28))
    #b = np.zeros(10)
    w = np.random.rand(10,28*28)
    b = np.random.rand(10)
    
    epochs = 100
    accu = np.zeros(epochs)
    cm = []
    for t in range(epochs):
        alpha = 1/((t+1)**2)
        for idx in trainset:
            train_result = np.argmax(np.sign(np.dot(w,idx.val.flatten())+b))
            w[train_result,:] = w[train_result,:]-alpha*idx.val.flatten()
            b[train_result] = b[train_result] - alpha*1.0
            w[idx.lab,:] = w[idx.lab,:] + alpha*idx.val.flatten()
            b[idx.lab] = b[idx.lab] + alpha*1.0
    #Test
    #################################################################
        confusion = np.zeros((10,10))
        i = 0
        probval =[[],[],[],[],[],[],[],[],[],[]]
        probimg =[[],[],[],[],[],[],[],[],[],[]]
        probidx =[[],[],[],[],[],[],[],[],[],[]]
        for testidx in testset:
            # Classify
            classify = np.argmax(np.sign(np.dot(w,testidx.val.flatten())+b))
            val = max(np.sign(np.dot(w,testidx.val.flatten())+b))
            probval[classify].append(val)
            probimg[classify].append(testidx)
            probidx[classify].append(i)
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
        accu[t]=overall_accur
        cm.append(confusion)
        
    np.set_printoptions(precision=3)
    print('The overall accuracy is: ',end='')
    print(max(accu))
    print('The confusion matrix is:')
    print(cm[np.argmax(accu)])
    print(np.argmax(accu)+1)

    plt.figure()
    plt.plot(range(1,epochs+1),accu)
    plt.xlabel('number of epochs')
    plt.ylabel('Accuracy')
    plt.title('Training curve')
    plt.grid(True)
    plt.show()
