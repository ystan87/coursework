# Part 2: classification of orientation of images
#
# team members: piyurai and yeestan
#
# For report and comments on the code and analysis,
# please refer to "Part_2_Report.pdf" in the root folder

import sys
import re
import numpy as np
import operator
import math
import os

methods = [
    "nearest",
    "adaboost",
    "nnet",
    "best"
]
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print "Invalid format. Please refer:"
    print "pyton orient.py [train_file.txt] [test_file.txt] [method] [parameter (optional)]"
    exit()
elif sys.argv[3] not in methods:
    print "Unknown method."
    exit()
elif len(sys.argv) == 4 and (sys.argv[3] == methods[1] or sys.argv[3] == methods[2]):
    print "Invalid format. Parameter argument (argument number 5) must be specified."
    exit()

shape = (8, 8, 3)
train_input = {}
test_input = {}
id_lookup = {}
img_std = {}
str_write = ""
confusion_matrix = np.zeros((4,4))
debug_train_limit = 4e4
debug_test_limit = 1e3
test_mode = False
model_file = ""
num_nnet_iter = 0


### section for file input/output
def input_train_data():
    with open(train_file, 'r') as f:
        num_example = 0
        num_parsed_example = 0

        for example in f:
            num_example += 1
            example = example.rstrip('\n')
            entries = example.split(' ')
            if len(entries) != 194:
                continue

            example_name = entries.pop(0)
            example_id = re.search(r'[0-9]+', example_name).group()
            id_lookup[example_name] = example_id
            if example_name not in train_input:
                train_input[example_name] = {}

            orientation = int(entries.pop(0)) / 90
            array = np.empty(shape)
            for idx, entry in enumerate(entries):
                idx0 = idx / (shape[1] * shape[2])
                idx1 = idx % (shape[1] * shape[2]) / shape[2]
                idx2 = idx % (shape[1] * shape[2]) % shape[2]
                array[idx0][idx1][idx2] = int(entry)
            train_input[example_name][orientation] = array
            if example_name not in img_std:
                img_std[example_name] = np.std(array)
            num_parsed_example += 1
            if num_example >= debug_train_limit:
                break

        print "number of examples:", num_example
        print "number of parsed examples:", num_parsed_example
    return num_example, num_parsed_example


def input_test_data():
    with open(test_file, 'r') as f:
        num_test = 0
        for sample in f:
            entries = sample.split(' ')
            sample_name = entries.pop(0)
            sample_id = re.search(r'[0-9]+', sample_name).group()
            id_lookup[sample_name] = sample_id

            correct_orientation = int(entries.pop(0)) / 90
            array = np.empty(shape)
            for idx, entry in enumerate(entries):
                idx0 = idx / (shape[1] * shape[2])
                idx1 = idx % (shape[1] * shape[2]) / shape[2]
                idx2 = idx % (shape[1] * shape[2]) % shape[2]
                array[idx0][idx1][idx2] = int(entry)
            test_input[sample_name] = (correct_orientation, array)
            num_test += 1
            if num_test >= debug_test_limit:
                break


def output_to_file(str_write):
    if sys.argv[3] == "best":
        return
    if method == "nearest":
        with open('nearest_output.txt', 'w') as f:
            f.write(str_write)
    elif method == "adaboost":
        with open('adaboost_output.txt', 'w') as f:
            f.write(str_write)
    elif method == "nnet":
        with open('nnet_output.txt', 'w') as f:
            f.write(str_write)


def read_model_file(filename):
    w1 = []
    w2 = []
    with open(filename, 'r') as f:
        w1_str = f.readline()
        w = w1_str.split(' ')
        for l in w:
            l = l.split(',')
            l = [float(e) for e in l]
            w1.append(l)
        w2_str = f.readline()
        w = w2_str.split(' ')
        for l in w:
            l = l.split(',')
            l = [float(e) for e in l]
            w2.append(l)
        hidden_count = len(w2)
        num_nnet_iter = int(4e5/hidden_count)
    return True, w1, w2


train_file = sys.argv[1]
test_file = sys.argv[2]
method = sys.argv[3]
if sys.argv[3] == "nearest":
    # adjust for time constraints
    debug_train_limit = 2e3
if len(sys.argv) == 5:
    if sys.argv[3] == "adaboost":
        parameter = int(sys.argv[4])
        stump_count = parameter
        num_adaboost_hypotheses = 4
        # adjust for time constraint
        debug_train_limit = int(4e6/stump_count)
    elif sys.argv[3] == "nnet":
        parameter = int(sys.argv[4])
        hidden_count = parameter
        # adjust for time constraint
        num_nnet_iter = int(4e5/hidden_count)
    elif sys.argv[3] == "best":
        method = "nnet"
        hidden_count = 11
        # adjust for time constraint
        num_nnet_iter = int(4e5/hidden_count)
        if len(sys.argv) == 5:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            model_file = "/".join([dir_path, sys.argv[4]])
            if os.path.isfile(model_file):
                test_mode, w1, w2 = read_model_file(model_file)


# section for nearest neighbor
def dist_sq(array1, array2):
    sum_dist_sq = 0
    for idx in range(192):
        idx0 = idx / 24
        idx1 = idx % 24 / 3
        idx2 = idx % 3
        sum_dist_sq += (array1[idx0][idx1][idx2] - array2[idx0][idx1][idx2])**2
    return sum_dist_sq


# section for adaboost
def normalize_weight(weight):
    total = np.sum(weight)
    return weight/total


def adaboost_split(total_store):
    min_entropy = math.log(2)
    split = -1
    same_below = 0
    same_above = 1
    diff_below = 0
    diff_above = 3
    for index,temp in enumerate(total_store):
        if index == len(total_store)-1:
            break
        weight = temp[2]
        orientation = temp[3]
        train_orient = temp[1]
        if train_orient == orientation:
            same_above -= weight
            same_below += weight
        else:
            diff_above -= weight
            diff_below += weight
        if same_above < 0 or same_below < 0 or diff_above < 0 or diff_below < 0:
            continue
        entropy = 0
        if same_below != 0 and diff_below != 0:
            same_prob = float(same_below) / (same_below + diff_below)
            diff_prob = 1 - same_prob
            prob_below = float(same_below + diff_below) / 4
            if same_prob > 0 and same_prob < 1:
                entropy -= (same_prob * math.log(same_prob) + diff_prob * math.log(diff_prob)) * prob_below
        if same_above != 0 and diff_above != 0:
            same_prob = float(same_above) / (same_above + diff_above)
            diff_prob = 1 - same_prob
            prob_above = float(same_above + diff_above) / 4
            if same_prob > 0 and same_prob < 1:
                entropy -= (same_prob * math.log(same_prob) + diff_prob * math.log(diff_prob)) * prob_above
        if entropy < min_entropy:
            min_entropy = entropy
            split = (total_store[index][0]+total_store[index+1][0])/2
            if diff_below == 0:
                is_above = True if same_above*3 > diff_above else False
            elif diff_above == 0:
                is_above = False if same_below*3 > diff_below else True
            else:
                is_above = False if float(same_below)/diff_below > float(same_above)/diff_above else True
    return split, min_entropy, is_above


def generate_decision(stump_pxl, weight, finished):
    store = {}
    total_store = {}
    decision = {}
    min_entropy = {}
    for orientation in range(4):
        min_entropy[orientation] = math.log(2)
    for orientation in range(4):
        print "adaboost training: orientation", orientation
        if finished[orientation]:
            continue
        total_store[orientation] = {}
        for stump_no,pxls in enumerate(stump_pxl):
            if stump_no%100==0 and stump_no>0:
                print "adaboost training: stump number", stump_no
            if stump_no not in total_store[orientation]:
                total_store[orientation][stump_no] = []
            pxl0 = pxls[0]
            pxl1 = pxls[1]
            store[orientation] = []
            for idx,example in enumerate(train_input):
                for train_orient in range(4):
                    if train_orient not in train_input[example]:
                        continue
                    image = train_input[example][train_orient]
                    diff = image[int(pxl0[0])][int(pxl0[1])][int(pxl0[2])] - \
                           image[int(pxl1[0])][int(pxl1[1])][int(pxl1[2])] + 255
                    total_store[orientation][stump_no].append((diff/img_std[example], train_orient,
                                                              weight[orientation][idx][train_orient], orientation))
            total_store[orientation][stump_no] = sorted(total_store[orientation][stump_no], key=operator.itemgetter(0))
            split, entropy, is_above = adaboost_split(total_store[orientation][stump_no])
            if entropy < min_entropy[orientation]:
                min_entropy[orientation] = entropy
                decision[orientation] = (stump_no, split, is_above)

    return decision


def implement_decision(stump_pxl, decision, weight, finished):
    correctness = np.ones((4,num_parsed_example,4))
    h_weight = {}
    for orientation in range(4):
        if finished[orientation]:
            continue
        error = 0
        for idx,example in enumerate(train_input):
            for train_orient in range(4):
                if train_orient not in train_input[example]:
                    continue
                image = train_input[example][train_orient]
                pxls = stump_pxl[decision[orientation][0]]
                pxl0 = pxls[0]
                pxl1 = pxls[1]
                diff = image[int(pxl0[0])][int(pxl0[1])][int(pxl0[2])] - \
                       image[int(pxl1[0])][int(pxl1[1])][int(pxl1[2])] + 255
                result = diff/img_std[example]
                same_orientation = 1 if train_orient == orientation else 0
                result_is_above = 1 if result > decision[orientation][1] else 0
                decision_is_above = 1 if decision[orientation][2] else 0
                summary = same_orientation + result_is_above + decision_is_above
                if summary == 0 or summary == 2:
                    error += weight[orientation][idx][train_orient]
                    correctness[orientation][idx][train_orient] = False
        w_update_factor = error/(1-error)
        for idx,example in enumerate(train_input):
            for train_orient in range(4):
                if not correctness[orientation][idx][train_orient]:
                    weight[orientation][idx][train_orient] *= w_update_factor
        weight[orientation] = normalize_weight(weight[orientation])
        if error == 0:
            h_weight[orientation] = 1e3
            finished[orientation] = True
        else:
            h_weight[orientation] = -math.log(w_update_factor)
    return weight, h_weight, finished


def adaboost_train(stump_count):
    print "training adaboost"
    # select stumps from random sampling
    if stump_count > 192*191/2:
        stump_count = 192*191/2
    stump = np.zeros((stump_count, 2))
    stump_pxl = []
    selection = np.random.choice(range(192*191/2+1), size = stump_count, replace = False)
    for index,selected in enumerate(selection):
        n = 1
        while n*(n+1)/2 < selected:
            n += 1
        stump[index][0] = n*(n+1)/2 - selected
        stump[index][1] = stump[index][0] + 192 - n
        a = stump[index][0]
        b = stump[index][1]
        # initialize weight
        weight = np.ones((4,num_parsed_example/4,4))
        weight /= num_parsed_example
        # pixel-pair location of the decision stump
        stump_pxl.append([(a/24,a%24/3,a%3),(b/24,b%24/3,b%3)])

    decision = {}
    h_weight = {}
    finished = [False] * 4
    for i in range(num_adaboost_hypotheses):
        print "adaboost hypothesis", i
        decision[i] = generate_decision(stump_pxl, weight, finished)
        weight, h_weight[i], finished = implement_decision(stump_pxl, decision[i], weight, finished)

    return stump_pxl, decision, h_weight

# section for neural networks
if num_nnet_iter > 12000:
    target_values = [-0.995, 0.995]
else:
    target_values = [-0.99, 0.99]


def normalize_image(image):
    image = np.array(image)
    return (image-np.mean(image))/np.std(image)


def activation_func(input):
    return np.tanh(input)


def derivative_func(back_input):
    if math.fabs(back_input) > 100:
        return 0
    temp = math.exp(back_input)
    temp = 2*temp/(1+temp**2)
    return temp**2


def initialize_weights():
    weight1 = np.random.normal(loc=0.0, scale=1.0/math.sqrt(hidden_count), size=(192,hidden_count))
    weight2 = np.random.normal(loc=0.0, scale=0.5, size=(hidden_count,4))
    return weight1, weight2


def backpropagate(image, orientation, weight1, weight2, learn1, learn2):
    layer1 = [0] * hidden_count
    layer2 = [0] * 4
    output = [target_values[0]] * 4
    output[orientation] = [target_values[1]]
    a = {
        2 : [0] * 4,
        1 : [0] * hidden_count,
        0 : np.ndarray.flatten(np.array(image))
    }
    delta = {
        2 : [0] * 4,
        1 : [0] * hidden_count
    }
    for j in range(hidden_count):
        for i in range(192):
            layer1[j] += weight1[i][j] * a[0][i]
        a[1][j] = activation_func(layer1[j])
    for j in range(4):
        for i in range(hidden_count):
            layer2[j] += weight2[i][j] * a[1][i]
        a[2][j] = activation_func(layer2[j])
    debug = np.sum([math.fabs(output[j]-a[2][j]) for j in range(4)])
    debug2 = np.argmax([a[2][j] for j in range(4)])
    debug3 = np.zeros((192,hidden_count))
    debug4 = np.zeros((hidden_count, 4))
    if debug2 == orientation:
        debug2 = 1
    else:
        debug2 = 0
    for j in range(4):
        delta[2][j] = derivative_func(layer2[j]) * (output[j]-a[2][j])
    for i in range(hidden_count):
        for j in range(4):
            delta[1][i] += delta[2][j] * weight2[i][j]
        delta[1][i] *= derivative_func(layer1[i])
    for i in range(hidden_count):
        for j in range(4):
            weight2[i][j] += learn2 * a[1][i] * delta[2][j]
            debug4[i][j] += math.fabs(learn2 * a[1][i] * delta[2][j])
    for i in range(192):
        for j in range(hidden_count):
            weight1[i][j] += learn1 * a[0][i] * delta[1][j]
            debug3[i][j] += math.fabs(learn1 * a[0][i] * delta[1][j])

    return weight1, weight2, debug, debug2, debug3, debug4


def nnet_train():
    example_index = []
    for example in train_input:
        example_index.append(example)
    num_example = len(example_index)
    w1, w2 = initialize_weights()
    print "training neural nets"
    for t in range(num_nnet_iter):
        # implements stochastic gradient descent
        e = np.random.randint(0, num_example)
        o = np.random.randint(0, 4)
        image = normalize_image(train_input[example_index[e]][o])
        l1 = 0.5/(t+1)
        l2 = l1*0.7
        w1, w2, debug, debug2, debug3, debug4 = backpropagate(image, o, w1, w2, l1, l2)
        if t%1000==0 :
            print "iteration", t
    return w1, w2


def nnet_run(image, weight1, weight2):
    layer1 = [0] * hidden_count
    layer2 = [0] * 4
    a = {
        2: [0] * 4,
        1: [0] * hidden_count,
        0: np.ndarray.flatten(np.array(image))
    }
    for j in range(hidden_count):
        for i in range(192):
            layer1[j] += weight1[i][j] * a[0][i]
        a[1][j] = activation_func(layer1[j])
    for j in range(4):
        for i in range(hidden_count):
            layer2[j] += weight2[i][j] * a[1][i]
        a[2][j] = activation_func(layer2[j])
    return np.argmax([a[2][j] for j in range(4)])

if not test_mode:
    num_example, num_parsed_example = input_train_data()
input_test_data()


if method == "nearest":
    orient_count = {}
    example_count = {}
    num_sample = 0
    num_correct = 0

    for sample in test_input:
        min_dist = 3*8*8 * 255**2
        min_orient = -1
        min_example = "not found"
        test_image = normalize_image(test_input[sample][1])
        for example in train_input:
            for orientation in train_input[example]:
                # minimizing distance is same as minimizing the square of distance
                dist = dist_sq(normalize_image(train_input[example][orientation]), test_image)
                if dist<min_dist:
                    min_dist = dist
                    min_orient = orientation
                    min_example = example
        if min_orient not in orient_count:
            orient_count[min_orient] = 1
        else:
            orient_count[min_orient] += 1
        if min_example not in example_count:
            example_count[min_example] = 1
        else:
            example_count[min_example] += 1
        str_write += sample + " " + str(min_orient * 90) + "\n"
        if min_orient != -1:
            confusion_matrix[test_input[sample][0]][min_orient] += 1
        if min_orient == test_input[sample][0]:
            num_correct += 1
        num_sample += 1
        if num_sample % 100 == 0:
            print "testing nearest: current iteration", num_sample
        if num_sample > debug_test_limit:
            break
    #print "The counts for each orientation is", orient_count
    #print "The distinct number of examples included is", len(example_count)
elif method == "adaboost":
    num_sample = 0
    num_correct = 0
    stump_pxl, decision, h_weight = adaboost_train(stump_count)
    print "testing adaboost"
    for sample in test_input:
        #print "sample", sample
        correct_orientation = test_input[sample][0]
        image = test_input[sample][1]
        image = np.array(image)
        std_image = np.std(image)
        vote = np.zeros(4)
        for orientation in range(4):
            for i in decision:
                if orientation not in decision[i]:
                    # finished, the error is trained to be 0
                    break
                sub_decision = decision[i][orientation]
                stump = stump_pxl[sub_decision[0]]
                split = sub_decision[1]
                train_above = sub_decision[2]
                pxl0 = stump[0]
                pxl1 = stump[1]
                diff = image[int(pxl0[0])][int(pxl0[1])][int(pxl0[2])] - \
                       image[int(pxl1[0])][int(pxl1[1])][int(pxl1[2])] + 255
                res = diff/std_image
                test_above = res > split
                if train_above == test_above:
                    vote[orientation] += h_weight[i][orientation]
        detected_orientation = np.argmax(vote)
        confusion_matrix[correct_orientation][detected_orientation] += 1
        str_write += sample + " " + str(detected_orientation*90) + "\n"
        if detected_orientation == correct_orientation:
            num_correct += 1
        num_sample += 1
        #print "voted", vote
        #print "correct orientation", correct_orientation
elif method == "nnet":
    num_sample = 0
    num_correct = 0
    if not test_mode:
        w1, w2 = nnet_train()
        if sys.argv[3] == "best" and len(model_file)>0:
            with open(model_file, 'w') as f:
                model_write = ""
                for idx,w in enumerate(w1):
                    for idx_,w_ in enumerate(w):
                        model_write += str(w_)
                        if idx_ != len(w)-1:
                            model_write += ","
                    if idx != len(w1)-1:
                        model_write += " "
                f.write(model_write + "\n")
                model_write = ""
                for idx,w in enumerate(w2):
                    for idx_,w_ in enumerate(w):
                        model_write += str(w_)
                        if idx_ != len(w)-1:
                            model_write += ","
                    if idx != len(w2)-1:
                        model_write += " "
                f.write(model_write)
    print "testing neural nets"
    for sample in test_input:
        correct_orientation = test_input[sample][0]
        image = normalize_image(test_input[sample][1])
        detected_orientation = nnet_run(image, w1, w2)
        confusion_matrix[correct_orientation][detected_orientation] += 1
        str_write += sample + " " + str(detected_orientation*90) + "\n"
        if detected_orientation == correct_orientation:
            num_correct += 1
        num_sample += 1

print "Number of correct guesses", num_correct, "out of", num_sample
print "Confusion matrix"
print confusion_matrix
output_to_file(str_write)