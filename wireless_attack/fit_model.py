import csv

import numpy as np

from pyod.models.cblof import CBLOF

# Load it with pandas and change strings to number values for CBLOF fitting
def load_dataset(filename):
    dataset = []
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            dataset.append(row)
    dataset = np.array(dataset)
    return dataset

def fit_cblof(dataset):
    cblof = CBLOF(4)
    estimator = cblof.fit(dataset)
    return estimator

if __name__ == '__main__':
    dataset = load_dataset('dataset.csv')
    estimator = fit_cblof(dataset)
    print(estimator.predict_confidence(dataset))