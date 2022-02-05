# -*- coding: utf-8 -*-
import application.extraction.ExtractiveQA as eqa

class RobertaEQA(eqa.ExtractiveQA):    

    def __init__(self):
        super().__init__("deepset/roberta-base-squad2")
