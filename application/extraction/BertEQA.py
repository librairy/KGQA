# -*- coding: utf-8 -*-
import application.extraction.ExtractiveQA as eqa

class BertEQA(eqa.ExtractiveQA):

    def __init__(self):
        super().__init__("bert-large-uncased-whole-word-masking-finetuned-squad")
