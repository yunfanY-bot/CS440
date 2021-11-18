"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

import math

"""
This function will return 3 parameters:
1. emission probabilities: {tag:{word:P}}
2. transition probabilities: {tag:{tag:P}}
3. initial probabilities: {tag:P}
"""


def train_v1(train):
    """
    @ To do:
        parameters to tune later
    """
    # laplace smoothing parameter for emission probability
    e_laplace = 0.0002
    # laplace smoothing parameter for transitional probability
    t_laplace = 0.0005

    tag_list = []

    # # build initial probabilities: {tag:P}
    # initial_count = {}
    # initial_prob = {}
    # start_tag_count = 0
    # for sentence in train:
    #     start = sentence[1]
    #     start_tag = start[1]
    #     start_tag_count += 1
    #     if start_tag in initial_count:
    #         initial_count[start_tag] += 1
    #     else:
    #         initial_count[start_tag] = 1
    # for tag in initial_count:
    #     initial_prob[tag] = initial_count[tag] / start_tag_count

    # build transitional probability
    trans_count = {}
    trans_prob = {}
    for sentence in train:
        # n is number of words in the sentence
        n = len(sentence)
        for i in range(n - 1):
            cur_tag = sentence[i][1]
            next_tag = sentence[i + 1][1]
            if cur_tag not in tag_list and cur_tag != "START":
                tag_list.append(cur_tag)
            # ignore END tag
            if next_tag == "END":
                continue
            if cur_tag in trans_count:
                cur_dict = trans_count[cur_tag]
                if next_tag in cur_dict:
                    cur_dict[next_tag] += 1
                else:
                    cur_dict[next_tag] = 1
            else:
                trans_count[cur_tag] = {next_tag: 1}

    hapx_count_tag = {}
    total_count_tag = 0
    for tag in trans_count:
        cur_dict = trans_count[tag]
        for tag in cur_dict:
            if cur_dict[tag] <= 2:
                total_count_tag += 1
                if tag in hapx_count_tag:
                    hapx_count_tag[tag] += 1
                else:
                    hapx_count_tag[tag] = 1

    # calculate probability with smoothing
    for tag in trans_count:
        cur_laplace = 0
        v = len(trans_count[tag])
        if tag in hapx_count_tag:
            cur_laplace = t_laplace * pow(2 * hapx_count_tag[tag], 2)
        else:
            cur_laplace = t_laplace
        cur_laplace = cur_laplace / total_count_tag
        trans_prob[tag] = {}
        cur_dict = trans_count[tag]
        cur_total = 0
        for next_tag in cur_dict:
            cur_total += cur_dict[next_tag]
        for next_tag in cur_dict:
            trans_prob[tag][next_tag] = (cur_dict[next_tag] + cur_laplace) / (cur_total + cur_laplace * (v + 1))
            trans_prob[tag]["UNKNOWN"] = cur_laplace / (cur_total + cur_laplace * (v + 1))


    # build emission probability
    emis_count = {}
    emis_prob = {}
    for sentence in train:
        for pair in sentence:
            word = pair[0]
            tag = pair[1]
            if tag in emis_count:
                cur_dict = emis_count[tag]
                if word in cur_dict:
                    cur_dict[word] += 1
                else:
                    cur_dict[word] = 1
            else:
                emis_count[tag] = {word: 1}

    # hapx distribution
    # {tag: prob}
    hapx_count = {}
    total_count = 0
    for tag in emis_count:
        cur_dict = emis_count[tag]
        for word in cur_dict:
            if cur_dict[word] == 1:
                total_count += 1
                if tag in hapx_count:
                    hapx_count[tag] += 1
                else:
                    hapx_count[tag] = 1

    for tag in emis_count:
        cur_laplace = 0
        if tag == "START":
            continue
        if tag in hapx_count:
            cur_laplace = e_laplace * pow(hapx_count[tag], 1.4)
        else:
            cur_laplace = e_laplace
        cur_laplace = cur_laplace / total_count
        print(cur_laplace)
        v = len(emis_count[tag])
        emis_prob[tag] = {}
        cur_dict = emis_count[tag]
        cur_total = 0
        for word in cur_dict:
            cur_total += cur_dict[word]
        for word in cur_dict:
            emis_prob[tag][word] = (cur_dict[word] + cur_laplace) / (cur_total + cur_laplace * (v + 1))
            emis_prob[tag]["UNKNOWN"] = cur_laplace / (cur_total + cur_laplace * (v + 1))

        # reset START and END emissions
        emis_prob["START"] = {"START": 1}
        emis_prob["END"] = {"END": 1}

    return trans_prob, emis_prob, tag_list


"""
Class:
fields:
methods:
"""


class Node:
    def __init__(self, set_index):
        self.v = {}
        self.b = {}
        self.index = set_index

    def get_tag_prob(self, tag):
        return self.v[tag]

    def set_tag_prob(self, tag, prob):
        self.v[tag] = prob

    def get_tag_parent(self, tag):
        return self.b[tag]

    def set_tag_parent(self, tag, par):
        self.b[tag] = par

    def find_max(self):
        pass


"""
helper function to do viterbi on a single sentence
"""


def best_list(sentence, tag_list, trans_prob, emis_prob):
    to_return = []
    node_list = []
    start_node = Node(0)
    start_node.set_tag_prob("START", 1)
    start_node.set_tag_parent("START", "START")
    node_list.append(start_node)
    for i in range(1, len(sentence) - 1):
        cur_node = Node(i)
        cur_v = {}
        cur_b = {}
        cur_word = sentence[i]
        # hard code to start
        if i == 1:
            for tag_b in tag_list:
                if cur_word in emis_prob[tag_b]:
                    if tag_b in trans_prob["START"]:
                        cur_value = math.log(node_list[i - 1].get_tag_prob("START")) + math.log(
                            trans_prob["START"][tag_b]) + math.log(
                            emis_prob[tag_b][cur_word])
                    else:
                        cur_value = math.log(node_list[i - 1].get_tag_prob("START")) + math.log(
                            trans_prob["START"]["UNKNOWN"]) + math.log(
                            emis_prob[tag_b][cur_word])
                else:
                    if tag_b in trans_prob["START"]:
                        cur_value = math.log(node_list[i - 1].get_tag_prob("START")) + math.log(
                            trans_prob["START"][tag_b]) + math.log(
                            emis_prob[tag_b]["UNKNOWN"])
                    else:
                        cur_value = math.log(node_list[i - 1].get_tag_prob("START")) + math.log(
                            trans_prob["START"]["UNKNOWN"]) + math.log(
                            emis_prob[tag_b]["UNKNOWN"])
                cur_v[tag_b] = cur_value
                cur_b[tag_b] = "START"

        # none-start node
        else:
            # tag_b is current tag
            for tag_b in tag_list:
                # store a list of current results
                selection_list = {}
                # tag_a is previous tag
                for tag_a in tag_list:
                    if cur_word in emis_prob[tag_b]:
                        if tag_b in trans_prob[tag_a]:
                            cur_value = node_list[i - 1].get_tag_prob(tag_a) + math.log(
                                trans_prob[tag_a][tag_b]) + math.log(
                                emis_prob[tag_b][cur_word])
                        else:
                            cur_value = node_list[i - 1].get_tag_prob(tag_a) + math.log(
                                trans_prob[tag_a]["UNKNOWN"]) + math.log(
                                emis_prob[tag_b][cur_word])
                    else:
                        if tag_b in trans_prob[tag_a]:
                            cur_value = node_list[i - 1].get_tag_prob(tag_a) + math.log(
                                trans_prob[tag_a][tag_b]) + math.log(
                                emis_prob[tag_b]["UNKNOWN"])
                        else:
                            cur_value = node_list[i - 1].get_tag_prob(tag_a) + math.log(
                                trans_prob[tag_a]["UNKNOWN"]) + math.log(
                                emis_prob[tag_b]["UNKNOWN"])
                    selection_list[tag_a] = cur_value
                # select maximum pair after filling all values
                prev_tag = max(selection_list, key=lambda k: selection_list[k])
                cur_v[tag_b] = selection_list[prev_tag]
                cur_b[tag_b] = prev_tag
        cur_node.v = cur_v
        cur_node.b = cur_b
        node_list.append(cur_node)

    # trace back
    last_node = node_list[len(node_list) - 1]
    last_tag = max(last_node.v, key=lambda k: last_node.v[k])
    to_return.insert(0, last_tag)
    cur_tag = last_node.b[last_tag]
    i = len(node_list) - 2
    while i != 0:
        to_return.insert(0, cur_tag)
        cur_node = node_list[i]
        cur_tag = cur_node.b[cur_tag]
        i -= 1
    return to_return


def viterbi_3(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    pair = train_v1(train)
    trans_prob = pair[0]
    emis_prob = pair[1]
    tag_list = pair[2]
    to_return = []
    count = 0

    for sentence in test:
        count += 1
        cur_list = best_list(sentence, tag_list, trans_prob, emis_prob)
        cur_result = []
        cur_result.append(("START", "START"))
        for i in range(1, len(sentence) - 1):
            cur_result.append((sentence[i], cur_list[i-1]))
        cur_result.append(("END", "END"))
        to_return.append(cur_result)
        print(count)

    return to_return


"""
Fix transtable ENDs
"""