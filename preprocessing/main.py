import random
import networkx as nx
import numpy as np
from copy import deepcopy
import math
# with open('facebook_combined.txt', 'r') as f:
#     data = f.read().split('\n')
with open('processedMat.txt', 'r') as f:
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
hiddenRate = 0.2
testEdges = {}
testNegEdges = {}

hiddenEdges = {}
hiddenNegEdges = {}

observedEdges = {}

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

# edgeMap = []
# nodeMap = []
totalNegEdgeList = {}
totalPosEdgeList = {}
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

    hiddenCnt = int(hiddenRate * degree)
    edgeList = addDict(hiddenEdges, edgeList, hiddenCnt)
    # testCnt = int(testRate * degree)
    # edgeList = addDict(testEdges, edgeList, testCnt)

    # addAllDict(observedEdges, edgeList, 0)  # 0 is all
    addAllDict(totalPosEdgeList, edgeList, 0)  # 0 is all
    # negtive sample

    # testNegCount = testCnt
    hiddenNegCnt = hiddenCnt

    negEdgeList = [(i, v) for v in nodes - set(nbrs) - set([i])]


    random.shuffle(negEdgeList)

    negEdgeList = addDict(hiddenNegEdges, negEdgeList, hiddenNegCnt)

    totalNegEdgeList[i] = negEdgeList

    # negEdgeList = addDict(testNegEdges, negEdgeList, testNegCount)
    # edgeMap.append(edgeList)
    # nodeMap.append(nbrs)



#
# for i in range(size):
#     edgeList = edgeMap[i]
#     nbrs = nodeMap[i]
#     originEdgeList = edgeList # avoid edgelist to be edited
#     degree = len(edgeList)
#     if degree  < 10:
#         # addDict(smallDgreeEdges, edgeList,  0)
#         addDict(observedEdges, edgeList, 0)
#         continue
#
#     hiddenCnt = int(hiddenRate * degree)
#     edgeList = addDict(hiddenEdges, edgeList, hiddenCnt)
#     testCnt = int(testRate * degree)
#     edgeList = addDict(testEdges, edgeList, testCnt)
#
#     addDict(observedEdges, edgeList, 0) # 0 is all
#     # negtive sample
#
#     testNegCount = testCnt
#     hiddenNegCnt = hiddenCnt
#
#     negEdgeList = [(i, v) for v in nodes-set(nbrs) - set([i])]
#
#
#     negEdgeList = addDict(hiddenNegEdges, negEdgeList, hiddenNegCnt)
#
#     negEdgeList = addDict(testNegEdges, negEdgeList, testNegCount)
#

#
# for n, nbrs in G.adj.items():
#     # positive sample
#     degree = len(nbrs)
#     edgeList = [(n, v) for v in nbrs]
#     if degree  < 10:
#         addDict(smallDgreeEdges, edgeList,  0)
#
#     hiddenCnt = int(hiddenRate * degree)
#     edgeList = addDict(hiddenEdges, edgeList, hiddenCnt)
#     testCnt = int(testRate * degree)
#     edgeList = addDict(testEdges, edgeList, testCnt)
#
#     addDict(observedEdges, edgeList, 0) # 0 is all
#     # negtive sample
#     negEdgeList = [(n, v) for v in nodes-set(nbrs)]
#     testNegCount = testCnt
#     negEdgeList = addDict(testNegEdges, negEdgeList, testNegCount)
#
#     hiddenNegCnt = hiddenCnt
#     addDict(hiddenNegEdges, negEdgeList, hiddenNegCnt)

hiddenEdges = d2l(hiddenEdges)
hiddenNegEdges = d2l(hiddenNegEdges)
testEdges = d2l(testEdges)
# testNegEdges = d2l(testNegEdges)
# observedEdges = d2l(observedEdges)

totalPosEdgeList =  d2l(totalPosEdgeList)

hiddens = deepcopy(hiddenEdges)
hiddens.extend(hiddenNegEdges)
testEdges = []


hidden_node = {}
for edge in hiddens:
    hidden_node[edge[0]] = True
    hidden_node[edge[1]] = True
hidden_node = hidden_node.keys()

print("hidden_node", len(hidden_node))



hidden_pos_size = len(hiddenEdges)
hidden_neg_size = len(hiddenNegEdges)



test_pos_size = hidden_pos_size//4
test_neg_size = hidden_neg_size//4

print('test pos size', test_pos_size)
print('test neg size', test_neg_size)
test_pos_count = 0
test_neg_count = 0

observedEdges = []


for edge in totalPosEdgeList:
    if test_pos_count < test_pos_size and edge[0] in hidden_node and edge[1] in hidden_node:
        testEdges.append(edge)
        test_pos_count += 1
    else:
        observedEdges.append(edge)

testNegEdges = []



# for edge in totalNegEdgeList:
#     if test_neg_count < test_neg_size and edge[0] in hiddens and edge[1] in hiddens:
#         testNegEdges.append(edge)
#         test_neg_count +=1
#     elif test_neg_count >= test_neg_size:
#         break
print(test_neg_size)
break_flag = False
for v, edgeList in totalNegEdgeList.items():

    if v in hidden_node:
        tempList = deepcopy(edgeList)
        random.shuffle(tempList)
        for edge in tempList:
            if edge[1] in hidden_node:
                testNegEdges.append(edge)
                test_neg_count +=1
                if test_neg_count >= test_neg_size:
                    break_flag = True
                    break
                # print(test_neg_count)
        if break_flag == True:
            break


# smallDgreeEdges = d2l(smallDgreeEdges)
print('hidden')
print(hiddenEdges)
print(len(hiddenEdges))
print('hidden neg')
print(hiddenNegEdges[:10])
print(len(hiddenNegEdges))
print('test')
print(testEdges[:10])
print(len(testEdges))
print('test neg')
print(testNegEdges[:10])
print(len(testNegEdges))
print('observed')
print(observedEdges[:10])
print(len(observedEdges))
# print('small degree')
# print(smallDgreeEdges[:10])
# print(len(smallDgreeEdges))
print('total')
print(len(hiddenEdges)  + len(testEdges) + len(observedEdges))



def output(filename, edges):
    with open(filename, 'w') as f:
        for e in edges:
            f.write(str(e[0]) + ' ' +  str(e[1]) + '\n')


random.shuffle(observedEdges)
random.shuffle(hiddenEdges)
random.shuffle(hiddenNegEdges)
random.shuffle(testEdges)
random.shuffle(testNegEdges)

# hiddenNegEdges = random.sample(hiddenNegEdges, len(hiddenEdges))
# print(len(hiddenNegEdges))
# testNegEdges = random.sample(testNegEdges, len(testEdges))
# print(len(testEdges))
output('hiddenEdges.txt', hiddenEdges)
output('hiddenNegEdges.txt', hiddenNegEdges)
output('testEdges.txt', testEdges)
output('testNegEdges.txt', testNegEdges)
output('observedEdges.txt', observedEdges)
# output('smallDegreeEdges.txt', smallDgreeEdges)






