#!/usr/bin/python

def main():
   import sys,json
   to_open = sys.argv[1]
   output_dir = sys.argv[2]
   output_list = sys.argv[3]
   counter = 1
   lst_files = []
   for each_line in open(to_open):
      with open('{}/file_{}'.format(output_dir, counter),'w') as w_fh:
         decoded = json.loads(each_line)
         for each_decoded in decoded:
            w_fh.write(each_decoded.encode('utf8'))
      lst_files.append('{}/file_{}'.format(output_dir, counter))
      counter = counter+1

   with open(output_list,'w') as w_fh:
      for l in lst_files:
         w_fh.write(l + '\n')

   return


if __name__ == '__main__':
   main()
