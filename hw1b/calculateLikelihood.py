#!/usr/bin/python


def getStateTransit(seg):
    return [x[3] for x in seg]


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


def main():
    import sys
    with open(sys.argv[1]) as inputFile:
        inputLines = inputFile.read().split('\n')
        episodes = segment(inputLines)
        for x in episodes:
            print getStateTransit(x)
    return

if __name__ == '__main__':
    main()
