# -*- coding: utf-8 -*-
import application.extraction.LanguageModel as language_model

class BertEN(language_model.LanguageModel):
    
    def __init__(self):
        super().__init__("bert-large-uncased-whole-word-masking-finetuned-squad")
        