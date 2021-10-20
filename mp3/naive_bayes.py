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


def load_data(trainingdir, testdir, stemming=False, lowercase=True, silently=False):
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


def naiveBayes_train(train_set, train_labels, laplace, silently=False):
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


def bigram_Bayes_train(train_set, train_labels, laplace, silently):
    pos_dict_count = {}  # each word count in positive reviews
    neg_dict_count = {}  # each word count in negative reviews
    pos_dict = {}  # probability table of positive reviews
    neg_dict = {}  # probability table of negative reviews
    pos_total = 0  # total word count in positive reviews
    neg_total = 0  # total word count in positive reviews
    i = 0
    for each_set in train_set:
        if train_labels[i] == 1:
            j = 0
            while j < len(each_set) - 1:
                bigram = (each_set[j], each_set[j + 1])
                pos_total += 1
                if bigram in pos_dict_count:
                    pos_dict_count[bigram] += 1
                else:
                    pos_dict_count[bigram] = 1
                j += 1
        else:
            j = 0
            while j < len(each_set) - 1:
                bigram = (each_set[j], each_set[j + 1])
                neg_total += 1
                if bigram in neg_dict_count:
                    neg_dict_count[bigram] += 1
                else:
                    neg_dict_count[bigram] = 1
                j += 1
        i += 1

    # laplace smooth
    for bigram in pos_dict_count:
        pos_dict[bigram] = (pos_dict_count[bigram] + laplace) / pos_total
    for bigram in neg_dict_count:
        neg_dict[bigram] = (neg_dict_count[bigram] + laplace) / neg_total

    # UNW adjusted by laplace smooth
    pos_dict["3e3eg3yegu"] = laplace / pos_total
    neg_dict["3e3eg3yegu"] = laplace / neg_total


    return [pos_dict, neg_dict]


# main function for the bigrammixture model
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.01, bigram_laplace=0.00007, bigram_lambda=0.15,
                pos_prior=0.77, silently=False):
    # Keep this in the provided template
    unigram_model = naiveBayes_train(train_set, train_labels, unigram_laplace, silently)
    bigram_model = bigram_Bayes_train(train_set, train_labels, bigram_laplace, silently)
    uni_pos_dict = unigram_model[0]
    uni_neg_dict = unigram_model[1]
    bi_pos_dict = bigram_model[0]
    bi_neg_dict = bigram_model[1]

    yhats = []



    for doc in tqdm(dev_set, disable=silently):
        # compute unigram sum
        # compute pos
        uni_pos_sum = 0
        uni_pos_sum += math.log(pos_prior, 10)
        for each_word in doc:
            if each_word in uni_pos_dict:
                uni_pos_sum += math.log(uni_pos_dict[each_word], 10)
            else:
                uni_pos_sum += math.log(uni_pos_dict["3e3eg3yegu"], 10)
        # compute neg
        uni_neg_sum = 0
        uni_neg_sum += math.log(1 - pos_prior, 10)
        for each_word in doc:
            if each_word in uni_neg_dict:
                uni_neg_sum += math.log(uni_neg_dict[each_word], 10)
            else:
                uni_neg_sum += math.log(uni_neg_dict["3e3eg3yegu"], 10)

        # compute bigram sum
        # compute pos
        bi_pos_sum = 0
        bi_pos_sum += math.log(pos_prior, 10)
        j = 0
        while j < len(doc) - 1:
            cur_pair = (doc[j], doc[j + 1])
            if cur_pair in bi_pos_dict:
                bi_pos_sum += math.log(bi_pos_dict[cur_pair], 10)
            else:
                bi_pos_sum += math.log(bi_pos_dict["3e3eg3yegu"], 10)
            j += 1

        # compute neg
        bi_neg_sum = 0
        bi_neg_sum += math.log(1 - pos_prior, 10)
        j = 0
        while j < len(doc) - 1:
            cur_pair = (doc[j], doc[j + 1])
            if cur_pair in bi_neg_dict:
                bi_neg_sum += math.log(bi_neg_dict[cur_pair], 10)
            else:
                bi_neg_sum += math.log(bi_neg_dict["3e3eg3yegu"], 10)
            j += 1

        pos_sum = (1 - bigram_lambda) * uni_pos_sum + bigram_lambda * bi_pos_sum
        neg_sum = (1 - bigram_lambda) * uni_neg_sum + bigram_lambda * bi_neg_sum

        if pos_prior < 0.3:
            pos_sum -= 7

        if pos_sum > neg_sum:
            yhats.append(1)
        else:
            yhats.append(0)

    return yhats
