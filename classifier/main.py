import argparse
import networkx as nx
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from sklearn.utils import shuffle
from sklearn.metrics import classification_report, accuracy_score

from link_prediction import link_prediction_model

def parse_args():
    parser = argparse.ArgumentParser(description="Run node2vec.")
    parser.add_argument('--input', nargs='?', default='data/observedEdges', help='Input graph path')
    parser.add_argument('--directed', dest='directed', action='store_true', help='Graph is (un)directed. Default is undirected.')
    parser.add_argument('--undirected', dest='undirected', action='store_false')
    parser.set_defaults(directed=False)
    parser.add_argument('--weighted', dest='weighted', action='store_true', help='Boolean specifying (un)weighted. Default is unweighted.')
    parser.add_argument('--unweighted', dest='unweighted', action='store_false')
    parser.set_defaults(weighted=False)
    parser.add_argument('--embedding', nargs='?', default='data/embedding.emb', help='Node embedding path')
    parser.add_argument('--embedding_dim', type=int, default=128, help='Node embedding dimension')

    return parser.parse_args()

def read_graph(graph_file, is_postive):
    if args.weighted:
        G = nx.read_edgelist(graph_file, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
    else:
        G = nx.read_edgelist(graph_file, nodetype=int, create_using=nx.DiGraph())
        if is_postive:
            for edge in G.edges():
                G[edge[0]][edge[1]]['weight'] = 1
        else:
            for edge in G.edges():
                G[edge[0]][edge[1]]['weight'] = 0
    if not args.directed:
        G = G.to_undirected()

    return G

def read_node_embedding():
    model = KeyedVectors.load_word2vec_format(args.embedding)
    node2index = dict(zip(map(int, model.wv.index2word), range(len(model.wv.index2word))))
    embedding_matrix = np.zeros((len(model.wv.vocab), args.embedding_dim))
    for i in range(len(model.wv.vocab)):
        embedding_vector = model.wv[model.wv.index2word[i]]
        embedding_matrix[i] = embedding_vector

    return embedding_matrix, node2index

def generate_data_set(G, node2index, is_postive):
    X1 = []
    X2 = []
    num_edges = 0
    for edge in G.edges:
        if edge[0] not in node2index or edge[1] not in node2index:
            continue
        num_edges += 1
        v1 = node2index[edge[0]]
        v2 = node2index[edge[1]]
        if v1 < v2:
            X1.append(v1)
            X2.append(v2)
        else:
            X1.append(v2)
            X2.append(v1)
    if is_postive:
        y = [1] * num_edges
    else:
        y = [0] * num_edges

    return X1, X2, y

def main(args):
    embedding_matrix, node2index = read_node_embedding()
    print(embedding_matrix.shape)

    G_hidden_pos = read_graph("data/hiddenEdges.txt", is_postive=True)
    print(G_hidden_pos.number_of_nodes(), G_hidden_pos.number_of_edges())
    G_hidden_neg = read_graph("data/hiddenNegEdges.txt", is_postive=False)
    print(G_hidden_neg.number_of_nodes(), G_hidden_neg.number_of_edges())

    X1_hidden_pos, X2_hidden_pos, y_hidden_pos = generate_data_set(G_hidden_pos, node2index, is_postive=True)
    print(len(X1_hidden_pos), len(X2_hidden_pos), len(y_hidden_pos))
    X1_hidden_neg, X2_hidden_neg, y_hidden_neg = generate_data_set(G_hidden_neg, node2index, is_postive=False)
    print(len(X1_hidden_neg), len(X2_hidden_neg), len(y_hidden_neg))
    #print(y_hidden_pos[:10])
    #print(y_hidden_neg[:10])

    X1 = X1_hidden_pos + X1_hidden_neg
    X2 = X2_hidden_pos + X2_hidden_neg
    y = y_hidden_pos + y_hidden_neg
    print(len(X1), len(X2), len(y))

    X1, X2, y = shuffle(X1, X2, y, random_state=2019)

    model = link_prediction_model(embedding_matrix)
    batch_size = 128
    num_epochs = 15
    model.fit([X1, X2], y, batch_size=batch_size, epochs=num_epochs, shuffle=True, validation_split=0.2, verbose=1)

    G_test_pos = read_graph("data/testEdges.txt", is_postive=True)
    print(G_test_pos.number_of_nodes(), G_test_pos.number_of_edges())
    G_test_neg = read_graph("data/testNegEdges.txt", is_postive=False)
    print(G_test_neg.number_of_nodes(), G_test_pos.number_of_edges())

    X1_test_pos, X2_test_pos, y_test_pos = generate_data_set(G_test_pos, node2index, is_postive=True)
    print(len(X1_test_pos), len(X2_test_pos), len(y_test_pos))
    X1_test_neg, X2_test_neg, y_test_neg = generate_data_set(G_test_neg, node2index, is_postive=False)
    print(len(X1_test_neg), len(X2_test_neg), len(y_test_neg))

    X1_test = X1_test_pos + X1_test_neg
    X2_test = X2_test_pos + X2_test_neg
    y_test = y_test_pos + y_test_neg
    print(len(X1_test), len(X2_test), len(y_test))

    pred_prob = model.predict([X1_test, X2_test])
    y_pred = (pred_prob[:, 0] > 0.5).astype(int)
    print(classification_report(y_test, y_pred))
    print("accuracy:", accuracy_score(y_test, y_pred))

if __name__ == "__main__":
    args = parse_args()
    main(args)
