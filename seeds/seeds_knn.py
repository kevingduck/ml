# Implementation of k_nearest_neighbors classifier: Using measurements of
# geometrical properties of kernels belonging to classify into three different
# varieties of wheat. A soft X-ray technique and GRAINS package were used to
# construct all seven, real-valued attributes.
# Implementation based on YT series by Sentdex

import numpy as np
from math import sqrt
import warnings
from collections import Counter
import pandas as pd
import random


def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to value less than total voting groups :/')
    distances = []
    for group in data:
        for features in data[group]:
            # the better NumPy way of getting Euclidean distance on k-dim data
            euclidean_distance = np.linalg.norm(np.array(features) - np.array(predict))
            distances.append([euclidean_distance, group])
    votes = [i[1] for i in sorted(distances) [:k]]
    # print (Counter(votes).most_common(1))
    vote_result = Counter(votes).most_common(1)[0][0]

    return vote_result

df = pd.read_csv("seeds_dataset.csv")
full_data = df.astype(float).values.tolist() # Converts strings like '1' to 1

# Shuffle data
random.shuffle(full_data)
print full_data

test_size = 0.2
train_set = {1.0:[], 2.0:[], 3.0:[]}
test_set = {1.0:[], 2.0:[], 3.0:[]}
# last X% of data used to train (e.g., 80% w/ test_size = 2)
train_data = full_data[:-int(test_size*len(full_data))]
# first 100-X% used to test (e.g., 20% w/ test_size = 2)
test_data = full_data[-int(test_size*len(full_data)):]

for i in train_data:
    train_set[i[-1]].append(i[:-1])

for i in test_data:
    test_set[i[-1]].append(i[:-1])

correct = 0
total = 0

for group in test_set:
    for data in test_set[group]:
        vote = k_nearest_neighbors(train_set, data, k=5)
        if group == vote:
            correct += 1
        total += 1

print ('Accuracy: ', float(correct)/total)