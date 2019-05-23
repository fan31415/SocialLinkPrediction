from keras.layers import Dense, Input, Embedding, Activation, Dot, Reshape, merge
from keras.models import Model
import keras

def link_prediction_model(embedding_matrix):

    num_nodes = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    input1 = Input(shape=(1, ))
    input2 = Input(shape=(1, ))
    embedding = Embedding(num_nodes, embedding_dim, weights=[embedding_matrix], trainable=True, input_length=1)
    x1 = Reshape((-1, ))(embedding(input1))
    x2 = Reshape((-1, ))(embedding(input2))

    # setup a cosine similarity operation which will be output in a secondary model

    # similarity = merge([x1, x2], mode='cos', dot_axes=0)

    # now perform the dot product operation to get a similarity measure
    # dot_product = merge([x1, x2], mode='dot', dot_axes=1)
    dot_product = Dot(axes=-1)([x1, x2])





    dot_product = Reshape((1,))(dot_product)
    # add the sigmoid output layer
    output1 = Dense(128, activation='sigmoid')(dot_product)


    output = Dense(1, activation='sigmoid')(output1)
   

    
    # output = Activation(activation="sigmoid")(dot_product)



    model = Model(inputs=[input1, input2], outputs=output)
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    print(model.summary())

    return model
