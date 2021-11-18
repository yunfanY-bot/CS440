"""
helper function to train for baseline algorithm
data structure: {word:{tag:count}}
"""


def baseline_train(train):
    tag_count = {}  # global tag count
    count_dict = {}  # tag count for each word
    best_dict = {}  # best tag for each word
    for sentence in train:
        for pair in sentence:
            cur_word = pair[0]
            cur_tag = pair[1]

            # count times this tag has occurred
            if cur_tag in tag_count:
                tag_count[cur_tag] += 1
            else:
                tag_count[cur_tag] = 1

            # count tag frequency for each word
            if cur_word in count_dict:
                cur_dict = count_dict[cur_word]
                if cur_tag in cur_dict:
                    cur_dict[cur_tag] += 1
                else:
                    cur_dict[cur_tag] = 1

            # if its the first time we've seen this word,
            # set up the tag frequency table and set the Frequency
            # for current tag to be 1
            else:
                count_dict[cur_word] = {cur_tag: 1}
    for key in count_dict:
        cur_tag_dict = count_dict[key]
        best_dict[key] = max(cur_tag_dict, key=lambda k: cur_tag_dict[k])

    best_dict["UNKNOWN"] = max(tag_count, key=lambda k: tag_count[k])
    return best_dict


"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""


def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    to_return = []
    best_dict = baseline_train(train)
    for sentence in test:
        cur_list = []
        for word in sentence:

            if word in best_dict:
                cur_list.append((word, best_dict[word]))
            else:
                cur_list.append((word, best_dict["UNKNOWN"]))
        to_return.append(cur_list)
    return to_return
