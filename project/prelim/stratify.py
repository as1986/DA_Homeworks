#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals

def stratify(student_dict, idx, folds):
   from random import shuffle
   dropped_authors = {k:v for k,v in student_dict.iteritems() if v[0][idx] == '1'}
   dk = dropped_authors.keys()
   shuffle(dk)
   non_dropped_authors = {k:v for k,v in student_dict.iteritems() if v[0][idx] == '0'}
   ndk = non_dropped_authors.keys()
   shuffle(ndk)

   sampled_dropped = {k:dropped_authors[k] for k in dk[:len(dk)/folds]}
   rest_dropped = {k:dropped_authors[k] for k in dk[len(dk)/folds:]}
   sampled_non_dropped = {k:non_dropped_authors[k] for k in ndk[:len(ndk)/folds]}
   rest_non_dropped = {k:non_dropped_authors[k] for k in ndk[len(ndk)/folds:]}
   return sampled_dropped, rest_dropped, sampled_non_dropped, rest_non_dropped

def write_csv_dict(cd, fn):
   import csv
   with open(fn, 'w') as fh:
      writer = csv.writer(fh)
      for v in cd.itervalues():
         for each_row in v:
            writer.writerow(each_row)


def main():
   import csv
   import sys
   ratio = 20
   with open(sys.argv[1],'rU') as fh:
      reader = csv.reader(fh)
      rows = [x for x in reader]
      author_idx = next(x[0] for x in enumerate(rows[0]) if x[1] == 'post_author')
      drop_idx = next(x[0] for x in enumerate(rows[0]) if x[1] == 'Drop')
      per_student = dict()
      for each_post in rows[1:]:
         to_append = per_student.setdefault(each_post[author_idx],[])
         to_append.append(each_post)
   print len(per_student)
   (dropped, rest_dropped, nondropped, rest_nondropped) = stratify(per_student, drop_idx, ratio)
   write_csv_dict(dropped, 'd.csv')
   write_csv_dict(nondropped, 'nd.csv')
   write_csv_dict(rest_dropped, 'dr.csv')
   write_csv_dict(rest_nondropped, 'ndr.csv')


if __name__ == '__main__':
   main()
