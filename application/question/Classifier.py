#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:39:26 2021

@author: cbadenes
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
import joblib
from sklearn.model_selection import GridSearchCV
import os

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Classifier:
    def __init__(self, model_file_path=None):
        self.model_file_path = model_file_path
        if self.model_file_path is not None and os.path.exists(self.model_file_path):
            print("loading svm model to classify questions..")
            self.load(model_file_path)
            print("model ready")
        else:
            self.model = None
        self.pipeline = Pipeline([('vect', CountVectorizer()), ('tf-idf', TfidfTransformer()),
                                  ('svm',
                                   SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter_no_change=5, random_state=42))])
        self.parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tf-idf__use_idf': (True, False),
                           'svm__alpha': (1e-2, 1e-3)}


    @property
    def is_trained(self):
        return self.model is not None

    def save(self, file_path):
        joblib.dump(self.model, file_path)

    def load(self, file_path):
        self.model = joblib.load(file_path)

    def train(self, X_train, y_train):
        optimized_classifier = GridSearchCV(self.pipeline, self.parameters, n_jobs=-1, cv=10)
        self.model = optimized_classifier.fit(X_train, y_train)
        if self.model_file_path is not None:
            self.save(self.model_file_path)
        return self.model.best_score_

    def predict(self, X_test):
        if self.is_trained:
            return self.model.predict(X_test)
        else:
            return None

    def predict_proba(self, X_test):
        if self.is_trained:
            return self.model.predict_proba(X_test)
        else:
            return None
