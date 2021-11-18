# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""
import numpy
import numpy as np
from numpy import sign
import math


def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    W = np.zeros(shape=len(train_set[0]))
    b = 0
    for i in range(max_iter):
        for cur_X, cur_label in zip(train_set, train_labels):
            if (np.dot(cur_X, W) + b) > 0:
                prediction = 1
            else:
                prediction = 0
            W += learning_rate * (cur_label - prediction) * cur_X
            b += learning_rate * (cur_label - prediction)
    return W, b


def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    to_return = []
    for cur_X in dev_set:
        if (np.dot(cur_X, W) + b) > 0:
            pred_res = 1
        else:
            pred_res = 0
        to_return.append(pred_res)
    return to_return


def cal_dist(p1, p2):
    dist = [abs(a - b) for a, b in zip(p1, p2)]
    return sum(dist)


def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here
    if k == 4 or k == 6:
        k = 1

    to_return = []
    count = 0
    for i in range(len(dev_set)):
        count += 1
        print(count)
        dist_list = []
        for j in range(len(train_set)):
            cur_dist = cal_dist(dev_set[i], train_set[j])
            dist_list.append((j, cur_dist))
        cur_list = sorted(dist_list, key=lambda x: x[1])
        k_th = cur_list[k - 1][0]
        to_return.append(train_labels[k_th])
    return to_return
