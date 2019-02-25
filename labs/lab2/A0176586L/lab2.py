# Pyspark == 2.4.0
# java version "1.8.0_202-ea"

from pyspark import SparkContext, SparkConf, SparkFiles
from os import listdir

all_files = listdir('datafiles')
all_files = [fname for fname in all_files if fname.endswith('txt')]


conf = SparkConf()
sc = SparkContext(conf=conf)

def text_reader(fname):
    # Step 0. load textfiles
    lines = sc.textFile(f"datafiles/{fname}")
    # Step 1. remove stopwords
    words = lines.flatMap(remove_stopwords)
    # create pairs
    pairs = words.map(lambda w: (w, 1))
    # Step 2. count occurence in each file
    counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)
    return counts

def remove_stopwords(line):
    with open('stopwords.txt','r') as f:
        stopwords = [word.rstrip('\n') for word in f.readlines()]
    words = line.split()
    words = [''.join([i for i in w if i.isalpha()]).lower() for w in words ]
    return [i for i in words if i not in stopwords]

commonwords = text_reader(all_files[0])
for fname in all_files[1::]:
    # Step 3. identify common words
    intersection = commonwords.cogroup(text_reader(fname)).filter(lambda x:x[1][0] and x[1][1])
    # Step 4. sort the list of common words
    commonwords = intersection.map(lambda x: (x[0], min(list(x[1][0])[0], list(x[1][1])[0])))

commonwords.sortBy(lambda x: x[1],ascending=False).collect()
print(commonwords.collect())
# commonwords.saveAsTextFile('output/lab2result.txt')