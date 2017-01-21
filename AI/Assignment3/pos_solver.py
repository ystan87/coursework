###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
#  mtsmoot
#  yeestan
# (Based on skeleton code by D. Crandall)
#
#
####
# Data from the training set is used to generate the following:
# 1. Initial probabilities: The distribution of POS of first word in each sentence
# 2. Transition probabilities: The transition of POS between consecutive words in each sentence
# 3. Emission probabilities: The emission probabilities of each POS to words in the training set
# 4. Second-order transition probabilities: The modeling of POS in the complex model as 2nd order Markov chain
#    with hidden variables. The transition to time t depends on the previous two states, t-1 and t-2.
#
# Emission probabilities of missing words: after trying various approaches, it is found to have best match when
# words not found in the training set are assumed to be nouns.
#
# Calculations:
# The simplified model consists of independent words. The MAP of each of these can be calculated separately.
# The HMM is implemented via the Viterbi algorithm.
# The complex model is a generalization of hidden state space into n-1 tuples (S_i, S_{i+1}) for i = 1, 2, ..., n-1
# In the forward step, the probability of S_1 is computed the initial probability, and S_2 is computed with
# first-order Markov assumption. Thereafter S_i is computed from (S_{i-2}, S_{i-1}), and is joined into
# (S_{i-1}, S_i) for the next step of computation. The backward step is similar to Viterbi.
#
# Posterior probabilities:
# Running the test on test.bc the probability of words correct in descending order are:
# Simplified, HMM, Complex
# For sentences correct the order is
# Simplified, Complex, HMM
# An Explanation is that the simplified model is optimized for words, while HMM and complex models also optimize
# dependencies between proximate words.
####

import random
import math
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # default the emission probability to 1 for nouns and 0 otherwise for all words
    def findMissingEmissions(self, data):
        toReturn = {}
        #posList = [x[1] for x in data]

        #for sentence in posList:
        #    for key in sentence:
        #        if key in toReturn:
        #            toReturn[key] = toReturn[key] + 1
        #        else:
        #            toReturn[key] = 1
        #for pos in self.posList:
            #toReturn[pos] = 1.0/len(self.posValues)
            #toReturn[pos] = toReturn[pos]/np.sum([toReturn[x] for x in self.posValues])
            #toReturn[pos] = 1.0 / (toReturn[pos] + 1)

        for pos in self.posValues:
            if pos == 'noun':
                toReturn[pos] = 1
            else:
                toReturn[pos] = 0
        return toReturn

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    # NOTE: Assuming label list matches
    def posterior(self, sentence, label):
        labelCnt = len(label)

        initial = self.initial[label[0]]
        toReturn = initial
        for idx, pos in enumerate(label):
            if idx < len(label) - 1:
                toReturn = toReturn * self.transitional[pos][label[idx + 1]]

                em = 0.0
                if sentence[idx] in self.emission[pos]:
                    em = self.emission[pos][sentence[idx]]
                else:
                    em = self.missingEmissions[pos]
                toReturn = toReturn * em
        # avoid running log(0)
        if toReturn == 0:
            return float('inf')
        return -1.0 * np.log(toReturn)

    # Do the training!
    #
    def train(self, data):
        self.posValues, self.posList = self.getPOS(data)
        self.initial = self.findInitial(data)
        self.transitional = self.findTransitional(data)
        self.emission, self.posProb, self.wordProb = self.findEmission(data)
        self.missingEmissions = self.findMissingEmissions(data)
        print self.missingEmissions
        print self.posList
        self.secondOrderTransition, self.hasSecondOrder = self.findSecondOrderTransition(data)

    # Get all parts-of-speech found in supplied data

    # Finds all possible POS values
    def getPOS(self, data):
        temp = set([x[1][0] for x in data])
        return temp, list(temp)

    # Finds P(S1) by grabbing the first POS of each line in data
    # RETURN: Hash of trained probabilities for each word's POS beginning a sentence
    # TODO: Possibly account for lines beginning with space or non-letter character?
    def findInitial(self, data):
        toReturn = {}
        #            v---POS list of element (second element of each top-level element of data)
        #            |  v---First POS of that list
        posList = [x[1][0] for x in data]

        for pos in set(posList):
            # Multiple by float identity to "cast" to decimal
            toReturn[pos] = (posList.count(pos) * 1.0) / len(posList)
        return toReturn

    def findTransitional(self, data):
        toReturn = {}

        posList = [x[1] for x in data]

        for header in self.posValues:
            toReturn[header] = {}
            for nextPos in self.posValues:
                toReturn[header][nextPos] = 0

        for sentence in posList:
            for idx, pos in enumerate(sentence):
                if idx < len(sentence) - 1:
                    toReturn[pos][sentence[idx + 1]] = toReturn[pos][sentence[idx + 1]] + 1

        for header in self.posValues:
            for nextPos in self.posValues:
                toReturn[header][nextPos] = toReturn[header][nextPos] * 1.0 / sum(toReturn[header].values())
        return toReturn

    def findSecondOrderTransition(self, data):
        secondOrderTransition = {}
        hasSecondOrder = {}

        posList = [x[1] for x in data]

        for Prev1 in self.posValues:
            secondOrderTransition[Prev1] = {}
            hasSecondOrder[Prev1] = {}
            for Prev2 in self.posValues:
                secondOrderTransition[Prev1][Prev2] = {}
                hasSecondOrder[Prev1][Prev2] = False
                for nextPos in self.posValues:
                    secondOrderTransition[Prev1][Prev2][nextPos] = 0

        for sentence in posList:
            for idx,pos in enumerate(sentence):
                if idx > 1 and idx < len(sentence):
                    secondOrderTransition[sentence[idx-2]][sentence[idx-1]][pos] += 1
                    if not hasSecondOrder[sentence[idx-2]][sentence[idx-1]]:
                        hasSecondOrder[sentence[idx - 2]][sentence[idx - 1]] = True

        return secondOrderTransition, hasSecondOrder

    def findEmission(self, data):
        posCount = {}
        posWordProb = {}
        vocabulary = set()
        totalCount = 0
        margPosProb = {}
        margWordProb = {}

        for pos in set(self.posValues):
            posCount[pos] = 0
            posWordProb[pos] = {}

        for sentence in data:
            for word in sentence[0]:
                if word not in vocabulary:
                    vocabulary.add(word)

        for sentence in data:
            if len(sentence[0]) != len(sentence[1]):
                print "Error input format"
                exit()

            for y in range(len(sentence[0])):
                word = sentence[0][y]
                pos = sentence[1][y]
                posCount[pos] += 1
                totalCount += 1
                if word in posWordProb[pos]:
                    posWordProb[pos][word] += 1
                else:
                    posWordProb[pos][word] = 1

                if pos in margPosProb:
                    margPosProb[pos] += 1
                else:
                    margPosProb[pos] = 1

                if word in margWordProb:
                    margWordProb[word] += 1
                else:
                    margWordProb[word] = 1

        for pos, posDict in posWordProb.iteritems():
            for word in posDict:
                posDict[word] = posDict[word] * 1.0 / posCount[pos]

        for pos in margPosProb:
            margPosProb[pos] = margPosProb[pos] * 1.0 / totalCount

        for word in margWordProb:
            margWordProb[word] = margWordProb[word] * 1.0 / totalCount

        return posWordProb, margPosProb, margWordProb

    # returns the integer index of self.posValues
    def posIndex(self, pos):
        for index, item in enumerate(self.posList):
            if item == pos:
                return index
        return -1

    # Functions for each algorithm.
    #
    def simplified(self, sentence):
        MAP = [None] * len(sentence)
        maxProb = [None] * len(sentence)
        for index, word in enumerate(sentence):
            maxProb[index] = 0
            if word not in self.wordProb:
                maxEm  = max(self.missingEmissions.values())
                for idx,emPOS in enumerate(self.missingEmissions):
                    if self.missingEmissions[emPOS] == maxEm:
                        MAPpos = emPOS
                MAP[index] = MAPpos
                maxProb[index] = maxEm
                continue
            for pos in self.posValues:
                if word in self.emission[pos]:
                    curProb = self.emission[pos][word] * self.posProb[pos] / self.wordProb[word]
                else:
                    curProb = 0
                if curProb > maxProb[index]:
                    maxProb[index] = curProb
                    MAP[index] = pos
        return [[MAP], [maxProb]]

    def hmm(self, sentence):
        MAP = [None] * len(sentence)
        store = np.ndarray((len(sentence), len(self.posValues)), dtype=float)
        maxTo = np.ndarray((len(sentence), len(self.posValues)), dtype=int)
        defaultMaxTo = self.posIndex('noun')
        for i in range(len(sentence)):
            for j in range(len(self.posValues)):
                maxTo[i][j] = defaultMaxTo
        # forward
        for indexWord, word in enumerate(sentence):
            if indexWord == 0:
                if word not in self.wordProb:
                    for pos in self.posValues:
                        indexPos = self.posIndex(pos)
                        store[indexWord][indexPos] = self.missingEmissions[pos]
                    continue
                for pos in self.posValues:
                    indexPos = self.posIndex(pos)
                    if word in self.emission[pos]:
                        store[indexWord][indexPos] = self.initial[pos] * self.emission[pos][word]
                    else:
                        store[indexWord][indexPos] = 0
                continue

            if word not in self.wordProb:
                for posCurrent in self.posValues:
                    idxPosCurrent = self.posIndex(posCurrent)
                    transitionValues = [store[indexWord-1][self.posIndex(posPrev)] *
                                        self.transitional[posPrev][posCurrent]
                                        for posPrev in self.posValues]
                    maxTo[indexWord][idxPosCurrent] = np.argmax(transitionValues)
                    store[indexWord][idxPosCurrent] = max(transitionValues) * self.missingEmissions[posCurrent]
            for posCurrent in self.posValues:
                indexPosCurrent = self.posIndex(posCurrent)
                if word in self.emission[posCurrent]:
                    transitionValues = [store[indexWord-1][self.posIndex(posPrev)] *
                                        self.transitional[posPrev][posCurrent]
                                        for posPrev in self.posValues]
                    maxTo[indexWord][indexPosCurrent] = np.argmax(transitionValues)
                    store[indexWord][indexPosCurrent] = max(transitionValues) * self.emission[posCurrent][word]
                else:
                    store[indexWord][indexPosCurrent] = 0
        # backward
        for indexWord in range(len(sentence))[::-1]:
            if indexWord == len(sentence) - 1:
                maxIndex = np.argmax(store[indexWord])
                maxPos = self.posList[maxIndex]
                MAP = [maxPos]
                continue

            maxIndex = maxTo[indexWord+1][maxIndex]
            maxPos = self.posList[maxIndex]
            MAP = [maxPos] + MAP
        return [[MAP], [[0] * len(sentence), ]]

    def complex(self, sentence):
        MAP = [None] * len(sentence)
        store = np.ndarray((len(sentence), len(self.posValues), len(self.posValues)), dtype=float)
        defaultMaxTo = self.posIndex('noun')
        maxTo = np.ndarray((len(sentence), len(self.posValues), len(self.posValues)), dtype=int)
        for i in range(len(sentence)):
            for j in range(len(self.posValues)):
                for k in range(len(self.posValues)):
                    maxTo[i][j][k] = defaultMaxTo
                    store[i][j][k] = 0.0
        # forward
        # ordering sequence
        # idxWord-2 idxWord-1 idxWord
        # Prev1     Prev2     word
        for idxWord,word in enumerate(sentence):
            if idxWord == 0:
                if word not in self.wordProb:
                    for pos in self.posValues:
                        indexPos = self.posIndex(pos)
                        store[idxWord][-1][indexPos] = self.missingEmissions[pos]
                    continue
                for pos in self.posValues:
                    indexPos = self.posIndex(pos)
                    if word in self.emission[pos]:
                        store[idxWord][-1][indexPos] = self.initial[pos] * self.emission[pos][word]
                    else:
                        store[idxWord][-1][indexPos] = 0
                continue

            if idxWord == 1:
                if word not in self.wordProb:
                    for posCurrent in self.posValues:
                        idxPosCurrent = self.posIndex(posCurrent)
                        for posPrev in self.posValues:
                            idxPosPrev = self.posIndex(posPrev)
                            store[idxWord][idxPosPrev][idxPosCurrent] = store[idxWord-1][-1][idxPosPrev] * \
                                                                        self.transitional[posPrev][posCurrent] * \
                                                                        self.missingEmissions[posCurrent]
                        continue
                for posCurrent in self.posValues:
                    idxPosCurrent = self.posIndex(posCurrent)
                    if word in self.emission[posCurrent]:
                        transitionValues = [store[idxWord-1][-1][self.posIndex(Prev)] *
                                            self.transitional[Prev][posCurrent]
                                            for Prev in self.posValues]
                        idxPosPrev = np.argmax(transitionValues)
                        store[idxWord][idxPosPrev][idxPosCurrent] = max(transitionValues) * \
                                                                    self.emission[posCurrent][word]
                    else:
                        for Prev in self.posValues:
                            store[idxWord][self.posIndex(Prev)][idxPosCurrent] = 0
                continue

            if word not in self.wordProb:
                for posCurrent in self.posValues:
                    idxPosCurrent = self.posIndex(posCurrent)
                    for Prev2 in self.posValues:
                        idxPrev2 = self.posIndex(Prev2)
                        transitionValues = [store[idxWord-1][self.posIndex(Prev1)][idxPrev2] *
                                            self.secondOrderTransition[Prev1][Prev2][posCurrent]
                                            for Prev1 in self.posValues]
                        store[idxWord][idxPrev2][idxPosCurrent] = max(transitionValues) * \
                                                                  self.missingEmissions[posCurrent]
                        maxTo[idxWord][idxPrev2][idxPosCurrent] = np.argmax(transitionValues)
                    continue
            for posCurrent in self.posValues:
                idxPosCurrent = self.posIndex(posCurrent)
                if word in self.emission[posCurrent]:
                    for Prev2 in self.posValues:
                        idxPrev2 = self.posIndex(Prev2)
                        transitionValues = [store[idxWord-1][self.posIndex(Prev1)][idxPrev2] *
                                           self.secondOrderTransition[Prev1][Prev2][posCurrent]
                                           for Prev1 in self.posValues]
                        store[idxWord][idxPrev2][idxPosCurrent] = max(transitionValues) * \
                                                                  self.emission[posCurrent][word]
                        maxTo[idxWord][idxPrev2][idxPosCurrent] = np.argmax(transitionValues)
                else:
                    for pos in self.posValues:
                        store[idxWord][self.posIndex(pos)][idxPosCurrent] = 0
        # backward
        if len(sentence) == 1:
            maxProb = 0
            maxIndex = -1
            for posIndex in range(len(self.posValues)):
                prob = store[idxWord][-1][posIndex]
                if prob > maxProb:
                    maxProb = prob
                    maxIndex = posIndex
            return [ [ [ self.posList[maxIndex] ] ], [ [0]*len(sentence) ] ]

        for idxWord in range(len(sentence))[::-1]:
            if idxWord == len(sentence) - 1:
                maxValue = 0
                iMax = -1
                jMax = -1
                for i in range(len(self.posValues)):
                    for j in range(len(self.posValues)):
                        if store[idxWord][i][j] > maxValue:
                            maxValue = store[idxWord][i][j]
                            iMax = i
                            jMax = j
                MAP = [self.posList[iMax], self.posList[jMax]]
                continue
            if idxWord == len(sentence) - 2:
                continue

            maxIndex = maxTo[idxWord+2][self.posIndex(MAP[0])][self.posIndex(MAP[1])]
            maxPos = self.posList[maxIndex]
            MAP = [maxPos] + MAP
        return [[MAP], [[0] * len(sentence), ]]

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"

