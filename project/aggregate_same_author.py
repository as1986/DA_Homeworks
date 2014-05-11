#!/usr/bin/python

__author__ = 'as1986'

import csv, sys


def get_idx(headrow, s):
    return next(x[0] for x in enumerate(headrow) if x[1] == s)


def main():
    to_open = sys.argv[1]
    rows = []
    with open(to_open, 'rU') as fh:
        reader = csv.reader(fh)
        for row in reader:
            rows.append(row)
    print rows[0]
    author_idx = get_idx(rows[0], 'post_author')
    text_idx = get_idx(rows[0], 'post_text')
    drop_idx = get_idx(rows[0], 'Drop')
    sbar_idx = get_idx(rows[0],'has_sbar')
    verb_idx = get_idx(rows[0],'verb')

    from collections import defaultdict, Counter

    same_author = defaultdict(list)
    same_author_drop = defaultdict(str)
    same_author_sbar = defaultdict(str)
    same_author_verb = defaultdict(Counter)


    for row in rows[1:]:
        same_author[row[author_idx]].extend(row[text_idx].strip().split())
        same_author_verb[row[author_idx]].update(row[verb_idx].strip().split())
        same_author_drop[row[author_idx]] = row[drop_idx]
        if same_author_sbar[row[author_idx]] != 'True':
            same_author_sbar[row[author_idx]] = row[sbar_idx]

    print len(same_author)
    to_write = sys.argv[2]
    with open(to_write, 'w') as w_fh:
        writer = csv.writer(w_fh)
        writer.writerow(['post_author','post_text','Drop','has_sbar','verb'])
        for author in same_author:
            row_to_write = [author, ' '.join(same_author[author]), same_author_drop[author], same_author_sbar[author], ' '.join(list(same_author_verb[author].elements()))]
            writer.writerow(row_to_write)

    return


if __name__ == '__main__':
    main()
