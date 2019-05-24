# with open('ca-CondMat.txt', 'r') as f:
#     data = f.read().split('\n')
# with open('email-Enron.txt', 'r') as f:
#     data = f.read().split('\n')
with open('data/graph_small.txt', 'r') as f:
    data = f.read().split('\n')



id2no = {}
count = 0
for line in data:
    # i+=1
    # if i > 1000:
    #     break
    if line == '':
        continue
    # points = line.split(' ')
    points = line.split('\t')
    p1 = int(points[0])
    if id2no.get(p1, -1) == -1:
        id2no[p1] = count
        count +=1
    p2 = int(points[1])
    if id2no.get(p2, -1) == -1:
        id2no[p2] = count
        count +=1




with open('data/processedMat.txt', 'w') as f:
    for line in data:
        if line == '':
            continue
        # points = line.split(' ')
        points = line.split('\t')
        p1 = int(points[0])
        p2 = int(points[1])
        f.write(str(id2no[p1]) + ' ' + str(id2no[p2]) + '\n')