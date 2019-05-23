# Network Link Prediction
Predict links in social network graph.

## Requirement
* python == 3.6
* networkx == 2.3
* numpy == 1.15.1
* tensorflow == 1.10.1
* keras == 2.2.2
* scikit-learn == 0.19.1
* gensim == 3.7.3


Requirement for embedding can be found in [here](#Reference)
## Usage

* Prepare Data

```
cd preprocessing
```
```
python preprocess_id.py
```
```
python main.py
```

* Embedding 

```
cd embedding
```

Prepare a python2.7 environment in conda, and change to this environment.

```
source activate python2
```

```
python src/main.py --input observedEdges.txt --output emb/embedding.emb
```
* predicting

```
cd classifer
```
```
python main.py
```

## Reference
[Node2Vector](https://github.com/aditya-grover/node2vec)
