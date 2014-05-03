#!/usr/bin/python

import pickle, untangle


def main():
   import sys, glob
   
   # filename pattern
   patt = glob.glob(sys.argv[1])
   print 'all files: {}'.format(len(patt))

   for each_xml in patt:
      # print 'file name: {}'.format(each_xml)
      obj = untangle.parse(each_xml)
      to_append = []
      try:
         for sentence in obj.root.document.sentences.sentence:
            to_append.append(sentence.parse.cdata)
      except IndexError:
         continue
      if len(to_append) > 0:
         with open(each_xml + '.parses', 'w') as w_fh:
            for a in to_append:
               w_fh.write(a.encode('utf8') + '\n')

   return

if __name__ == '__main__':
   main()
