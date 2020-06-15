from random import random
from bisect import bisect_right
import numpy as np

def weighted_shuffle(original, weights):
    shuffed_list = np.empty_like(original)
    cum_weights = np.cumsum(weights)
    for i in range(len(original)):
         rnd = random() * cum_weights[-1]
         j = bisect_right(cum_weights, rnd)
         shuffed_list[i] = original[j]
         cum_weights[j:] -= weights[j]
    return shuffed_list

a = np.arange(1,1000)
w = np.arange(1,1000)
r = weighted_shuffle(a,w)
#print(r[:2])
