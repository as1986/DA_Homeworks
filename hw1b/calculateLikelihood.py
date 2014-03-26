#!/usr/bin/python


def getStateTransit(seg):
    return [int(x[3]) for x in seg]


import collections
wordCounts = [collections.Counter()] * 5


def addWordsToClass(listOfWords, classIdx):
    global wordCounts
    for word in listOfWords:
        wordCounts[classIdx][word] += 1
    return


def segment(lines):
    toReturn = []
    currentEpisode = None
    for eachLine in lines:
        splitted = eachLine.strip().split()
        if len(splitted) < 2:
            continue
        try:
            parent = splitted[1]
        except:
            print eachLine
            exit()
        if parent == '-1':
            # new segment
            if currentEpisode is not None:
                toReturn.append(currentEpisode)
            currentEpisode = [splitted]
        else:
            currentEpisode.append(splitted)
    if currentEpisode is not None:
        toReturn.append(currentEpisode)
    return toReturn


def getTransProb(transitions):
    import math
    numClasses = len(transitions[0].strip().split())
    toReturn = []
    for i in range(numClasses):
        toAppend = [math.log(float(t.strip().split()[i]))
                    for t in transitions[:numClasses]]
        toReturn.append(toAppend)
    return toReturn


def calculateSeqProb(logTable, seq):
    # print logTable
    # print len(logTable)
    toReturn = 0
    if len(seq) < 2:
        return toReturn
    for i in range(1, len(seq)):
        # print i
        # print seq[i - 1]
        # print seq[i]
        toReturn += logTable[seq[i - 1]][seq[i]]
    return toReturn / len(seq)


def main():
    import sys
    with open(sys.argv[1]) as inputFile:
        inputLines = inputFile.read().split('\n')
        episodes = segment(inputLines)
        for x in episodes:
            print getStateTransit(x)
    with open(sys.argv[2]) as transitionFile:
        transitions = transitionFile.read().split('\n')
        transProb = getTransProb(transitions)
        print transProb
        for idx, x in enumerate(episodes):
            print \
                'episode {}, likelihood: {}'.format(
                    idx, calculateSeqProb(transProb, getStateTransit(x)))

        def printEpisode(episode):
            for eachUtterance in episode:
                print ' '.join(eachUtterance[:3])
                print ' '.join([x.split(':')[0] for x in eachUtterance[4:]])

        # max
        maxIdx = max(enumerate(episodes), key=lambda x:
                     calculateSeqProb(transProb, getStateTransit(x[1])))[0]
        print 'max: episode {}'.format(maxIdx)
        printEpisode(episodes[maxIdx])

        # min
        minIdx = min(enumerate(episodes), key=lambda x:
                     calculateSeqProb(transProb, getStateTransit(x[1])))[0]
        print 'min: episode {}'.format(minIdx)
        printEpisode(episodes[minIdx])

    return

if __name__ == '__main__':
    main()
