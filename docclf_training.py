from __future__ import print_function
import numpy as np
import pandas as pd
import util
import data_structures as helpers
from pprint import pprint
from time import time
import logging
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pickle

input = 'raw-data.csv'
f = open(input, 'r')

labels = []
x_stuff = ''
x_words = []

for line in f: 
    comma = line.find(',')
    if comma != -1:
        labels.append(util.DOC_LABELS[line[0:comma]])
        words = line[comma + 1:]
        x_words.append(words.strip())
        x_stuff += words


x_train, x_test, y_train, y_test = train_test_split(x_words, labels, test_size=0.1)

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

parameters = {'clf__alpha': (1e-05,),
'clf__max_iter': (10,),
'clf__penalty': ('elasticnet',),
'tfidf__use_idf': (True,),
'vect__max_features': (50000,),
'vect__ngram_range':((1,1),)}


if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block
    # # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=100)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(x_train, y_train)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    predicted = grid_search.predict(x_test)
    
    print(np.mean(predicted == y_test))


pickle.dump(grid_search, open('doc_clf.sav', 'wb'))

print(metrics.classification_report(y_test, predicted,target_names=util.DOC_LABELS.keys()))

print(metrics.confusion_matrix(y_test, predicted))


    