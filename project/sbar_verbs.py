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
    for ind, _ in enumerate(patterns):
        search = patterns[ind].search(s)
        if search is not None:
            counters[ind].update(search.groups())


def main():
    import sys, glob

    files = glob.glob(sys.argv[1])
    for f in files:
        for each_line in open(f):
            extract_verb(each_line)
    print 'VB: {}'.format(vbs)
    print 'VBD: {}'.format(vbds)
    print 'VBG: {}'.format(vbgs)
    print 'VBN: {}'.format(vbns)
    print 'VBP: {}'.format(vbps)
    print 'VBZ: {}'.format(vbzs)

    row_num_pat = re.compile('_(\d+)\.')

    for f in files:
        l_name = f[f.rfind('/'):]
        row_num = int(row_num_pat.search(l_name).groups()[0])
        print row_num

    return


if __name__ == '__main__':
    main()

