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

    from collections import defaultdict

    same_author = defaultdict(list)
    same_author_drop = defaultdict(str)


    for row in rows[1:]:
        same_author[row[author_idx]].extend(row[text_idx].strip().split())
        same_author_drop[row[author_idx]] = row[drop_idx]

    print len(same_author)
    to_write = sys.argv[2]
    with open(to_write, 'w') as w_fh:
        writer = csv.writer(w_fh)
        for author in same_author:
            row_to_write = [author, ' '.join(same_author[author]), same_author_drop[author]]
            writer.writerow(row_to_write)

    return


if __name__ == '__main__':
    main()