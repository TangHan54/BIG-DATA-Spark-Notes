# Pyspark == 2.4.0
# java version "1.8.0_202-ea"
from pyspark import SparkConf, SparkContext
from os import listdir
import re
import math

all_files = listdir('testfiles')
all_files = [fname for fname in all_files if fname.endswith('txt')]
with open('stopwords.txt','r') as f:
        stopwords = [word.rstrip('\n') for word in f.readlines()]

conf = SparkConf()
sc = SparkContext(conf=conf)

def remove_stopwords(line):
    words = line.split()
    words = [''.join([i for i in w if i.isalpha()]).lower() for w in words ]
    return [i for i in words if i not in stopwords]

# Compute TF of every word in each document
n = len(all_files)
tf_rdd = sc.parallelize([])
for i in range(n):
    lines = sc.textFile(f"testfiles/{all_files[i]}")
    words = lines.flatMap(remove_stopwords)
    pairs = words.map(lambda w: ((w, i), 1))
    tf = pairs.reduceByKey(lambda n1, n2: n1 + n2)
    tf_rdd = sc.union([tf_rdd, tf])

# Compute DF of every word in all documents
df = tf_rdd.map(lambda x: (x[0][0], 1)).reduceByKey(lambda n1,n2: n1+n2)

# Compute TF-IDF of every word in all documents
def tf_idf(x):
    value = (1 + math.log10(x[1][0]))*math.log10(n/x[1][1])
    return (x[0], value)

lines = sc.textFile("query.txt")
words = lines.flatMap(remove_stopwords)
pairs = words.map(lambda w: (w, 1))
query_tf = pairs.reduceByKey(lambda n1, n2: n1 + n2)
query_vector = query_tf.collect()
query_words = query_tf.keys().collect()
query_scale = math.sqrt(query_tf.reduce(lambda x,y: x[1]**2+y[1]**2))

revelance = sc.parallelize([])
for i in range(n):
    df_rdd = df.map(lambda x: ((x[0],i),x[1]))
    # calculate tfidf
    doc_tfidf = tf_rdd.join(df_rdd).map(tf_idf)
    S_rt = math.sqrt(doc_tfidf.map(lambda x: (x[0][1], x[1])).values().map(lambda x: x*x).sum())
    # normalize tfidf
    temp_norm_tf_idf = doc_tfidf.map(lambda x: (x[0], x[1]/S_rt))
    # calculate product
    product = temp_norm_tf_idf.filter(lambda x: x[0][0] in query_words).map(lambda x: (x[0][0], x[1])).join(query_tf).map(lambda x: (x[0],x[1][0]*x[1][1])).values().sum()
    # doc_scale should be 1 since it is normalized.
    doc_scale = temp_norm_tf_idf.values().map(lambda x: x**2).sum()
    temp_relevance = sc.parallelize([(all_files[i], product/doc_scale/query_scale)])
    revelance = revelance.union(temp_relevance)

result = revelance.sortBy(lambda x:x[1],ascending=False).collect()
with open('output/result.txt','w') as f:
        for i in result:
                f.write(str(i[0])+', '+str(i[1]))
                f.write('\n')
