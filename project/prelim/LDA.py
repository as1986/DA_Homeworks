__author__ = 'as1986'
import gensim
import csv

def main():
    import sys
    with open(sys.argv[1], 'rU') as fh:
        reader = csv.reader(fh)
        rows = [x for x in reader]
    student_dict = {}
    for each_row in rows:
        to_append = student_dict.setdefault(each_row[4], [])
        to_append.append(each_row[7])
    per_student_dict = {}
    for s,l_docs in student_dict.iteritems():
        all_docs = []
        for d in l_docs:
            all_docs.extend([unicode(x, errors='ignore') for x in d.strip().split()])
        per_student_dict[s] = all_docs
    d = gensim.corpora.Dictionary(per_student_dict.itervalues())
    per_student_bow = {k:d.doc2bow(v) for k,v in per_student_dict.iteritems()}
    lda_model = gensim.models.ldamodel.LdaModel(per_student_bow.values(),id2word=d, num_topics=100)
    lists = lda_model.show_topics(formatted=False, topn=10000)
    disclaim = {'no', 'didn\'t', 'never', 'yet', 'amazingly', 'although','but'}
    proclaim = {'naturally', 'obviously', 'sure', 'fact', 'indeed', 'shows', 'proves', 'demonstrates'}
    entertain = {'perhaps', 'probable', 'maybe', 'may', 'must', 'seems', 'apparently'}
    attribute = {'argues', 'believes', 'claims', 'claimed'}
    sum_pro = []
    sum_dis = []
    sum_ent = []
    sum_att = []

    def get_sum(topic, wordlist):
       words = [x for x in topic if x[1] in wordlist]
       return sum([x[0] for x in words])

    for idx, t in enumerate(lists):
       sum_pro.append((idx, get_sum(t, proclaim)))
       sum_dis.append((idx, get_sum(t, disclaim)))
       sum_ent.append((idx, get_sum(t, entertain)))
       sum_att.append((idx, get_sum(t, attribute)))
    
    def max_and_print(sum_list, word_list):
       import numpy
       m = max(sum_list, key=lambda x:x[1])
       print m
       print [(idx, x) for idx, x in enumerate(lists[m[0]]) if x[1] in word_list]
       print 'average: {}'.format(sum([x[1] for x in sum_list])/len(sum_list))
       print 'std dev: {}'.format(numpy.std([x[1] for x in sum_list]))
       return

    max_and_print(sum_pro, proclaim)
    max_and_print(sum_dis, disclaim)
    max_and_print(sum_ent, entertain)
    max_and_print(sum_att, attribute)
    n  = lda_model[per_student_bow.itervalues().next()]
    print n

    return

if __name__ == '__main__':
    main()
