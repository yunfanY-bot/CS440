# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
import numpy as np
import math
from tqdm import tqdm
import nltk
from collections import Counter
import reader

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

"""
  load_data calls the provided utility to load in the dataset.
  You can modify the default values for stemming and lowercase, to improve performance when
       we haven't passed in specific values for these parameters.
"""


def load_data(trainingdir, testdir, stemming=True, lowercase=True, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset(trainingdir, testdir, stemming, lowercase,
                                                                       silently)
    return train_set, train_labels, dev_set, dev_labels


# Keep this in the provided template
def print_paramter_vals(laplace, pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

"""
helper func to train.
return a dictionary of possibility
"""


def naiveBayes_train(train_set, train_labels, laplace=1.0, silently=False):
    pos_dict_count = {}  # each word count in positive reviews
    neg_dict_count = {}  # each word count in negative reviews
    pos_dict = {}  # probability table of positive reviews
    neg_dict = {}  # probability table of negative reviews
    pos_total = 0  # total word count in positive reviews
    neg_total = 0  # total word count in positive reviews
    i = 0
    for each_set in train_set:
        if train_labels[i] == 1:
            for each_word in each_set:
                pos_total += 1
                if each_word in pos_dict_count:
                    pos_dict_count[each_word] = pos_dict_count[each_word] + 1
                else:
                    pos_dict_count[each_word] = 1
        else:
            for each_word in each_set:
                neg_total += 1
                if each_word in neg_dict_count:
                    neg_dict_count[each_word] = neg_dict_count[each_word] + 1
                else:
                    neg_dict_count[each_word] = 1
        i += 1
    # do laplace
    for each_word in pos_dict_count:
        pos_dict[each_word] = (pos_dict_count[each_word] + laplace) / pos_total
    for each_word in neg_dict_count:
        neg_dict[each_word] = (neg_dict_count[each_word] + laplace) / neg_total

    # UNW adjusted by laplace smooth
    pos_dict["3e3eg3yegu"] = laplace / pos_total
    neg_dict["3e3eg3yegu"] = laplace / neg_total
    return [pos_dict, neg_dict]


def naiveBayes(train_set, train_labels, dev_set, laplace=0.01, pos_prior=0.78, silently=False):
    # Keep this in the provided template
    print_paramter_vals(laplace, pos_prior)

    yhats = []
    pair = naiveBayes_train(train_set, train_labels, laplace, silently)
    pos_dict = pair[0]
    neg_dict = pair[1]
    for doc in tqdm(dev_set, disable=silently):
        # compute pos
        pos_sum = 0
        pos_sum += math.log(pos_prior, 10)
        for each_word in doc:
            if each_word in pos_dict:
                pos_sum += math.log(pos_dict[each_word], 10)
            else:
                pos_sum += math.log(pos_dict["3e3eg3yegu"], 10)
        # compute neg
        neg_sum = 0
        neg_sum += math.log(1 - pos_prior, 10)
        for each_word in doc:
            if each_word in neg_dict:
                neg_sum += math.log(neg_dict[each_word], 10)
            else:
                neg_sum += math.log(neg_dict["3e3eg3yegu"], 10)
        if pos_sum > neg_sum:
            yhats.append(1)
        else:
            yhats.append(0)

    return yhats


# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace, bigram_laplace, bigram_lambda, pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=1.0, bigram_laplace=1.0, bigram_lambda=1.0,
                pos_prior=0.5, silently=False):
    # Keep this in the provided template
    # print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)
    #
    # yhats = []
    # for doc in tqdm(dev_set, disable=silently):
    #     yhats.append(-1)
    return
