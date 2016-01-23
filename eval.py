'''
For evaluating precision and recall metrics
'''
import numpy as np
import sys
import cPickle as pkl
import io

K1 = 1
K2 = 10

def precision(p, t, k):
    '''
    Compute precision @ k for predictions p and targets t
    '''
    n = len(p)
    res = np.zeros(n)
    for idx,item in enumerate(p):
        index = np.argsort(item)[::-1]
        for i in index[:k]:
            if i in t[idx]:
                res[idx] = 1
                break
    return np.sum(res)/n

def recall(p, t, k):
    '''
    Compute recall @ k for predictions p and targets k
    '''
    n = len(p)
    res = np.zeros(n)
    for idx,items in enumerate(t):
        index = np.argsort(p[idx])[::-1][:k]
        for i in items:
            if i in index:
                res[idx] = 1
                break
    return np.sum(res)/n

def meanrank(p, t):
    '''
    Compute mean rank of targets in the predictions
    '''
    n = len(p)
    res = np.zeros(n)
    for idx, items in enumerate(t):
        ind = np.argsort(p[idx])[::-1]
        minrank = n
        for i in items:
            currrank = np.where(ind==i)[0]
            if currrank < minrank:
                minrank = currrank
        res[idx] = minrank
    return np.mean(res)

def readable_predictions(p, t, d, k, labeldict):
    out = []
    for idx, item in enumerate(d):
        preds = np.argsort(p[idx])[::-1][:k]
        plabels = ','.join([labeldict.keys()[ii-1] if ii > 0 else '<unk>' for ii in preds])
        tlabels = ','.join([labeldict.keys()[ii-1] if ii > 0 else '<unk>' for ii in t[idx]])
        out.append('%s\t%s\t%s\n'%(tlabels,plabels,item))
    return out

def main(result_path, dict_path):
    with open('%s/predictions.pkl'%result_path,'r') as f:
        p = pkl.load(f)
    with open('%s/targets.pkl'%result_path,'r') as f:
        t = pkl.load(f)
    with open('%s/data.pkl'%result_path,'r') as f:
        d = pkl.load(f)
    with open('%s/embeddings.pkl'%result_path,'r') as f:
        e = pkl.load(f)
    with open('%s/label_dict.pkl'%dict_path,'r') as f:
        labeldict = pkl.load(f)

    readable = readable_predictions(p, t, d, 10, labeldict)
    with io.open('%s/readable.txt'%result_path,'w') as f:
        for line in readable:
            f.write(line)

    print("Precision @ {} = {}".format(K1,precision(p,t,K1)))
    print("Recall @ {} = {}".format(K2,recall(p,t,K2)))
    print("Mean rank = {}".format(meanrank(p,t)))

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])