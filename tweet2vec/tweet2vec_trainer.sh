#!/bin/bash

# specify train and validation files here
traindata="../misc/trainer_multilingual_example.txt"
valdata="../misc/tester_multilingual_example.txt"

# specify model name here
exp="tweet2vec"

# model save path
modelpath="model/$exp/"
mkdir -p $modelpath

# train
echo "Training..."
THEANO_FLAGS='floatX=float32' python char.py $traindata $valdata $modelpath

