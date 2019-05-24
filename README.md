# Network Link Prediction
Predict links in social network graph. A methods combined by node feature embedding and nerual network classfication. Inspired by [pnrl](http://www4.comp.polyu.edu.hk/~csztwang/paper/pnrl.pdf) and [node2vec](https://cs.stanford.edu/people/jure/pubs/node2vec-kdd16.pdf).

## Requirement
* python == 3.6
* networkx == 2.3
* numpy == 1.15.1
* tensorflow == 1.10.1
* keras == 2.2.2
* scikit-learn == 0.19.1
* gensim == 3.7.3


Requirement for embedding can be found in [Reference](#Reference)
## Usage

### Prepare Data

```
cd preprocessing
```

Mapping id in graph to continous number start from 0

```
python preprocess_id.py
```

Generate observed, hidden and testing data
```
python main.py
```

### Embedding 

```
cd embedding
```

Prepare a python2.7 environment in conda, and change to this environment. 

* Script

```
sh run.sh
```
* Manual

```
source activate python2
```

Generate embedding only use observedEdges

```
python src/main.py --input observedEdges.txt --output emb/embedding.emb
```
### Predicting

```
cd classifer
```

Using nerual network to predict links

```
python main.py
```

## Datasets

All experimental datasets are public, you can find in the following links:

* **Facebook**: J. McAuley and J. Leskovec. Learning to Discover Social Circles in Ego Networks. NIPS, 2012. https://snap.stanford.edu/data/egonets-Facebook.html

* **Email**: R. Guimera, L. Danon, A. Diaz-Guilera, F. Giralt and A. Arenas, Physical Review E , vol. 68, 065103(R), (2003). http://deim.urv.cat/~alexandre.arenas/data/welcome.htm

* **Condensed Matter Collaborations**: M. E. J. Newman, The structure of scientific collaboration networks, Proc. Natl. Acad. Sci. USA 98, 404-409 (2001). http://www-personal.umich.edu/~mejn/netdata/

## Reference
[Node2Vector](https://github.com/aditya-grover/node2vec)
