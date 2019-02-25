import re
import sys
from pyspark import SparkConf, SparkContext
from os import listdir

conf = SparkConf()
sc = SparkContext(conf=conf)

def text_reader(fname):
    # load files
    lines = sc.textFile(f"datafiles/{fname}")
    # remove stopwords
    words = lines.flatMap(remove_stopwords)
    # create pairs
    pairs = words.map(lambda w:(w,1))
    

def remove_stopwords(line):
    with open('stopwords.txt','r') as f:
        stopwords = [word.rstrip('\n') for word in f.readlines()]
    words = line.split()
    words = [''.join([i for i in w if i.isalpha() if w not in stopwords]).lower() for w in words]
    return [i for i in words if i not in stopwords]

words = lines.flatMap(lambda l: re.split(" ",l))
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)
counts.saveAsTextFile(sys.argv[2])
sc.stop()
