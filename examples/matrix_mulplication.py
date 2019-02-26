from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)

A = [[1,1],[2,2]]
B = [[0,0],[2,1]]

def parallel_matrix(M):
    res = []
    for (i,v) in zip(range(len(M)),M):
        for (j,vv) in zip(range(len(v)),v):
            res.append((i,j,vv))
    return sc.parallelize(res)

M1 = parallel_matrix(A).map(lambda x: (x[1],(1,x[0],x[2])))
M2 = parallel_matrix(B).map(lambda x: (x[0],(2,x[1],x[2])))
res = M1.join(M2).map(lambda x: ((x[1][0][1],x[1][1][1]),x[1][0][2]*x[1][1][2])).reduceByKey(lambda x,y: x+y).collect()
