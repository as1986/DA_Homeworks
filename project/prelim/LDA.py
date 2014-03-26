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
    lda_model = gensim.models.ldamodel.LdaModel(per_student_bow.values(),id2word=d, num_topics=5)
    print lda_model.print_topic(0)
    hdp_model = gensim.models.hdpmodel.HdpModel(per_student_bow.values(), id2word=d)
    print hdp_model

    return

if __name__ == '__main__':
    main()
