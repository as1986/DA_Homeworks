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
    words = {'seems', 'believe'}
    disclaim = {'no', 'didn\'t', 'never', 'yet', 'amazingly', 'although','but'}
    proclaim = {'naturally', 'obviously', 'sure', 'fact', 'indeed', 'shows', 'proves', 'demonstrates'}
    sum_pro = []
    sum_dis = []
    for idx, t in enumerate(lists):
       disclaim_words = [x for x in t if x[1] in disclaim]
       # print disclaim_words
       sum_pro.append((idx, sum([x[0] for x in disclaim_words])))
       proclaim_words = [x for x in t if x[1] in proclaim]
       # print proclaim_words
       sum_dis.append((idx, sum([x[0] for x in proclaim_words])))
    print len(lists)
    m = max(sum_pro, key=lambda x:x[1])
    print [(idx, x) for idx, x in enumerate(lists[m[0]]) if x[1] in proclaim]
    print 'average: {}'.format(sum([x[1] for x in sum_pro])/len(sum_pro))
    print max(sum_dis, key=lambda x:x[1])
    print 'average: {}'.format(sum([x[1] for x in sum_dis])/len(sum_dis))

    return

if __name__ == '__main__':
    main()
