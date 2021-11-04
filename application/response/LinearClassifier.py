#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 12:54:44 2021

@author: cbadenes
"""
import logging
import os

import pandas
import joblib
import spacy
from time import time

from scipy.sparse import csr_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

logger = logging.getLogger(__name__)


class TRECClassifier:
    
    def __init__(self):
        self.en_nlp_l = spacy.load("en_core_web_lg")
        
        training_data_path = os.path.join("./application/question/train/train_5500.csv")
        self.df_question_train = pandas.read_csv(training_data_path, sep='|', header=0, encoding = "ISO-8859-1")
        
        
        self.df_question_class = self.df_question_train.pop('Class')
    
        self.df_question_train.pop('Question')
        self.df_question_train.pop('WH-Bigram')
    
        self.df_question_train = pandas.get_dummies(self.df_question_train)
        
        self.question_clf = joblib.load("./application/question/question_classifier.pkl")
        
        print("TREC Question Classifier ready")

    def get_category(self, question):
        en_doc_l = self.en_nlp_l(u'' + question)

        question_class = self.classify_question(en_doc=en_doc_l, df_question_train=self.df_question_train)
        
        return question_class

    def pre_process(self,dta):
        return pandas.get_dummies(dta)
    
    
    def remove_irrelevant_features(self, df_question):
        df_question_class = df_question.pop('Class')
    
        df_question.pop('Question')
        df_question.pop('WH-Bigram')
    
        return df_question_class
    
    
    def transform_data_matrix(self, df_question_train, df_question_predict):
    
        df_question_train_columns = list(df_question_train.columns)
        df_question_predict_columns = list(df_question_predict.columns)
    
        df_question_trans_columns = list(set(df_question_train_columns + df_question_predict_columns))
    
        logger.debug("Union Columns: {0}".format(len(df_question_trans_columns)))
    
        trans_data_train = {}
    
        for feature in df_question_trans_columns:
            if feature not in df_question_train:
                trans_data_train[feature] = [0 for i in range(len(df_question_train.index))]
            else:
                trans_data_train[feature] = list(df_question_train[feature])
    
        df_question_train = pandas.DataFrame(trans_data_train)
        logger.debug("Training data: {0}".format(df_question_train.shape))
        df_question_train = csr_matrix(df_question_train)
    
        trans_data_predict = {}
    
        for feature in trans_data_train:
            if feature not in df_question_predict:
                trans_data_predict[feature] = 0
            else:
                trans_data_predict[feature] = list(df_question_predict[feature])  # KeyError
    
        df_question_predict = pandas.DataFrame(trans_data_predict)
        logger.debug("Target data: {0}".format(df_question_predict.shape))
        df_question_predict = csr_matrix(df_question_predict)
    
        return df_question_train, df_question_predict
    
    
    def naive_bayes_classifier(self, x_train, y, x_predict):
        gnb = GaussianNB()
        gnb.fit(x_train, y)
        prediction = gnb.predict(x_predict)
        return prediction
    
    
    def support_vector_machine(self, df_question_train, df_question_class, df_question_predict):
        lin_clf = LinearSVC()
        lin_clf.fit(df_question_train, df_question_class)
        prediction = lin_clf.predict(df_question_predict)
        return prediction, lin_clf
    
    
    def predict_question_class(self, question_clf, df_question_predict):
        return question_clf.predict(df_question_predict), question_clf
    
    
    def load_classifier_model(self, model_type="linearSVC"):
    
        # HELP: Not using the persistent classifier. SVC fails when it encounters previously unseen features at training.
        # Refer the comment in query_container
    
        training_model_path = os.path.join("./application/question/question_classifier.pkl")
    
        if model_type == "linearSVC":
            return joblib.load(training_model_path)
    
    
    def get_question_predict_data(self, en_doc=None, df_question_test=None):
    
        if df_question_test is None:
            # currently only supports single sentence classification
            sentence_list = list(en_doc.sents)[0:1]
    
        else:
            sentence_list = df_question_test["Question"].tolist()
    
            import spacy
            en_nlp = spacy.load("en_core_web_lg")
    
        question_data_frame = []
    
        for sentence in sentence_list:
    
            wh_bi_gram = []
            root_token, wh_pos, wh_nbor_pos, wh_word = [""] * 4
    
            if df_question_test is not None:
                en_doc = en_nlp(u'' + sentence)
                sentence = list(en_doc.sents)[0]
    
            for token in sentence:
    
                if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
                    wh_pos = token.tag_
                    wh_word = token.text
                    wh_bi_gram.append(token.text)
                    wh_bi_gram.append(str(en_doc[token.i + 1]))
                    wh_nbor_pos = en_doc[token.i + 1].tag_
    
                if token.dep_ == "ROOT":
                    root_token = token.tag_
    
            question_data_frame_obj = {'WH': wh_word, 'WH-POS': wh_pos, 'WH-NBOR-POS': wh_nbor_pos, 'Root-POS': root_token}
            question_data_frame.append(question_data_frame_obj)
            logger.debug("WH : {0} | WH-POS : {1} | WH-NBOR-POS : {2} | Root-POS : {3}"
                         .format(wh_word, wh_pos, wh_nbor_pos, root_token))
    
        df_question = pandas.DataFrame(question_data_frame)
    
        return df_question
    
    
    def classify_question(self, en_doc=None, df_question_train=None, df_question_test=None):
        """ Determine whether this is a who, what, when, where or why question """
    
    
        if df_question_test is None:
            df_question_predict = self.get_question_predict_data(en_doc=en_doc)
        else:
            df_question_predict = self.get_question_predict_data(df_question_test=df_question_test)
    
        
        df_question_predict = self.pre_process(df_question_predict)
    
        df_question_train, df_question_predict = self.transform_data_matrix(self.df_question_train, df_question_predict)

    
        #logger.debug("Classifier: {0}".format(question_clf))
    
        predicted_class, svc_clf = self.support_vector_machine(df_question_train, self.df_question_class, df_question_predict)
    
        if df_question_test is not None:
            return predicted_class, svc_clf, self.df_question_class, df_question_train
        else:
            return predicted_class

