#!/usr/bin/python

import re


def compile_pat(v):
    return re.compile('\(VP \({} (\w+)\) \(SBAR'.format(v))


pat = compile_pat('VB')
patd = compile_pat('VBD')
patg = compile_pat('VBG')
patn = compile_pat('VBN')
patp = compile_pat('VBP')
patz = compile_pat('VBZ')

from collections import Counter

vbs = Counter()
vbds = Counter()
vbgs = Counter()
vbns = Counter()
vbps = Counter()
vbzs = Counter()


def extract_verb(s):
    global pat, patd, patg, patn, patp, patz
    global vbs, vbds, vbgs, vbns, vbps, vbzs

    patterns = [pat, patd, patg, patn, patp, patz]
    counters = [vbs, vbds, vbgs, vbns, vbps, vbzs]

    verbs = []

    for ind, _ in enumerate(patterns):
        search = patterns[ind].search(s)
        if search is not None:
            counters[ind].update(search.groups())
            verbs.extend(search.groups())

    return verbs


def find_best_and_stem(l, threshold=0):
    from nltk.stem.wordnet import WordNetLemmatizer

    lm = WordNetLemmatizer()
    to_return = set()
    for each_v in l:
        if vbs[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
        if vbds[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
        if vbgs[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
        if vbns[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
        if vbps[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
        if vbzs[each_v] > threshold:
            to_return.add(lm.lemmatize(each_v, 'v'))
    return to_return


def main():
    import sys, glob

    files = glob.glob(sys.argv[1])
    sbar_presence = {}
    for f in files:
        for each_line in open(f):
            p = extract_verb(each_line)
            if f not in sbar_presence:
                sbar_presence[f] = p
            else:
                sbar_presence[f].extend(p)
    print 'VB: {}'.format(vbs)
    print 'VBD: {}'.format(vbds)
    print 'VBG: {}'.format(vbgs)
    print 'VBN: {}'.format(vbns)
    print 'VBP: {}'.format(vbps)
    print 'VBZ: {}'.format(vbzs)

    row_num_pat = re.compile('_(\d+)\.')

    rows = [[]] * 853
    for f in files:
        l_name = f[f.rfind('/'):]
        row_num = int(row_num_pat.search(l_name).groups()[0])
        print row_num
        if f in sbar_presence:
            if len(rows[row_num]) > 0:
                print 'row {} already exists: {}'.format(row_num, rows[row_num])
            bests = list(find_best_and_stem(sbar_presence[f]))
            if len(bests) > 0:
                rows[row_num] = ['True'] + bests
            else:
                rows[row_num] = ['False']
        else:
            rows[row_num] = ['False']

    for r in rows:
        print r

    return


if __name__ == '__main__':
    main()

