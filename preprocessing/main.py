import random
import networkx as nx
import numpy as np
from copy import deepcopy
import math
# with open('facebook_combined.txt', 'r') as f:
#     data = f.read().split('\n')
with open('data/processedMat.txt', 'r') as f:
    data = f.read().split('\n')

random.seed(42)
random.shuffle(data)
G = nx.Graph()


# edges = np.zeros()
# this data (u v) keeps u < v and no (v, u) exist again
# however networkx will not do this, it will only keep (v, u) nor exist, but not promise the order
for line in data:
    # i+=1
    # if i > 1000:
    #     break
    if line == '':
        continue
    points = line.split(' ')
    p1 = int(points[0])
    p2 = int(points[1])
    G.add_edge(p1, p2)



    # if p1 > p2:
    #     print(132)
    #     print(p1)
    #     print(p2)
    #     exit()
# for n in G:
#   neighbors = G.neighbors(n)
#   print
# neighbors1 = [n for n in G.neighbors(0)]
# print(neighbors1)
# random.shuffle(data)


# size = len(data)
# test = data[:size//10]
# train = data[size//10:]
testRate = 0.1
testEdges = {}
testNegEdges = {}

observedEdges = {}
negEdges = {}

smallDgreeEdges = {}


def addAllDict(dictionary, pairs, cnt):

    for pair in pairs[-cnt:]:
        # if pair[0] > pair[1]:
        #     continue

        dictionary[pair] = True
        mat[pair[0]][pair[1]] = 0
        mat[pair[1]][pair[0]] = 0
    pairs = pairs[:-cnt]
    # remove it from graph
    return pairs


def addDict(dictionary, pairs, cnt):


    for pair in pairs[-cnt:]:
        # if pair[0] > pair[1]:
        #     continue

        if sum(mat[pair[1]]) == 1:
            # print('last link')
            continue

        dictionary[pair] = True
        mat[pair[0]][pair[1]] = 0
        mat[pair[1]][pair[0]] = 0
    pairs = pairs[:-cnt]
    # remove it from graph

    return pairs

testList = []
def d2l(dicts):
    return list(dicts.keys())
nodes = set(G.nodes())
size = len(list(G.nodes()))
mat = np.zeros((size, size), dtype=int)
for n, nbrs in G.adj.items():
    for nbr in nbrs:
        mat[n][nbr] = 1

for i in range(size):
    edgeList = []
    nbrs = []
    for j in range(i, size):
        if mat[i][j] == 1:
            edgeList.append((i, j))
            nbrs.append(j)
    originEdgeList = edgeList  # avoid edgelist to be edited
    degree = len(edgeList)
    if degree < 10:
        # addDict(smallDgreeEdges, edgeList,  0)
        addAllDict(observedEdges, edgeList, 0)
        continue

    testCnt = int(testRate * degree)

    edgeList = addDict(testEdges, edgeList, testCnt)

    posLen = len(edgeList)

    addAllDict(observedEdges, edgeList, 0)  # 0 is all
    # negtive sample

    negEdgeList = [(i, v) for v in nodes - set(nbrs) - set([i])]

    random.shuffle(negEdgeList)

    edgeList = addDict(negEdges, negEdgeList, posLen)

    addDict(testNegEdges, negEdgeList, testCnt)




testEdges = d2l(testEdges)
testNegEdges = d2l(testNegEdges)
observedEdges = d2l(observedEdges)
negEdges = d2l(negEdges)

print(testEdges[:10])
print(len(testEdges))
print('test neg')
print(testNegEdges[:10])
print(len(testNegEdges))
print('observed')
print(observedEdges[:10])
print(len(observedEdges))

print('observed neg')
print(negEdges[:10])
print(len(negEdges))




def output(filename, edges):
    with open(filename, 'w') as f:
        for e in edges:
            f.write(str(e[0]) + ' ' +  str(e[1]) + '\n')


random.shuffle(observedEdges)
random.shuffle(testEdges)
random.shuffle(testNegEdges)
random.shuffle(negEdges)

# hiddenNegEdges = random.sample(hiddenNegEdges, len(hiddenEdges))
# print(len(hiddenNegEdges))
# testNegEdges = random.sample(testNegEdges, len(testEdges))
# print(len(testEdges))
output('../classifier/data/testEdges.txt', testEdges)
output('../classifier/data/testNegEdges.txt', testNegEdges)
output('../embedding/observedEdges.txt', observedEdges)
output('../classifier/data/hiddenEdges.txt', observedEdges)
output('../classifier/data/hiddenNegEdges.txt', negEdges)
# output('smallDegreeEdges.txt', smallDgreeEdges)






