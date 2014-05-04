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

verb_counter = Counter()

from nltk.stem.wordnet import WordNetLemmatizer

lm = WordNetLemmatizer()


def extract_verb(s):
    global pat, patd, patg, patn, patp, patz
    global verb_counter

    patterns = [pat, patd, patg, patn, patp, patz]

    verbs = []

    for ind, _ in enumerate(patterns):
        search = patterns[ind].search(s)
        if search is not None:
            verb_counter.update([lm.lemmatize(x, 'v') for x in search.groups()])
            verbs.extend(search.groups())

    return verbs


def find_best_and_stem(l, threshold=0):
    to_return = set()
    for each_v in l:
        if verb_counter[each_v] > threshold:
            to_return.add((each_v, verb_counter[each_v]))
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
    print 'Verbs: {}'.format(verb_counter)

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

