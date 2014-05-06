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
            verb_counter.update([lm.lemmatize(x, 'v').lower() for x in search.groups()])
            verbs.extend(search.groups())

    return verbs


def find_best_and_stem(l, threshold=0):
    to_return = set()
    for each_v in l:
        if verb_counter[each_v] > threshold:
            to_return.add((each_v, verb_counter[each_v]))
    return to_return


def combine_rows(read_rows, new_rows):
    return map(list.__add__, read_rows, new_rows)


def read_from_csv(fname):
    import csv

    rows = []
    with open(fname, 'rU') as fh:
        reader = csv.reader(fh, delimiter=',')
        for r in reader:
            rows.append(r)
    return rows


def fill_missing_rows(rows):
    example = len(rows[0])
    for r in rows:
        if len(r) == len(example)-2:
            r.extend(['False','NONE'])


def write_csv(fname, rows):
    import csv

    new_fname = fname[:fname.rfind('.csv')] + '.appended.csv'
    with open(new_fname, 'w') as w_fh:
        writer = csv.writer(w_fh)
        for r in rows:
            writer.writerow(r)


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

    csv_to_append = sys.argv[2]
    read_rows = read_from_csv(csv_to_append)
    
    rows = [[]] * len(read_rows)
    rows[0] = ['has_sbar', 'verb']
    for f in files:
        l_name = f[f.rfind('/'):]
        row_num = int(row_num_pat.search(l_name).groups()[0]) - 1
        if row_num == 0:
            continue
        print row_num
        if f in sbar_presence:
            if len(rows[row_num]) > 0:
                print 'row {} already exists: {}'.format(row_num, rows[row_num])
            bests = list(find_best_and_stem(sbar_presence[f]))
            if len(bests) > 0:
                # rows[row_num] = ['True', (max(bests, key=lambda x: x[1]))[0]]
                rows[row_num] = ['True', ' '.join([x[0] for x in bests])]
            else:
                rows[row_num] = ['False', 'NONE']
        else:
            rows[row_num] = ['False', 'NONE']


    appended = combine_rows(read_rows, rows)
    fill_missing_rows(appended)
    write_csv(csv_to_append, appended)

    return


if __name__ == '__main__':
    main()

