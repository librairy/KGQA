# -*- coding: utf-8 -*-
import application.extraction.LanguageModel as language_model

class RobertaEN(language_model.LanguageModel):    
        
    def __init__(self):
        super().__init__("deepset/roberta-base-squad2")        
