# -*- coding: utf-8 -*-
import application.extraction.LanguageModel as language_model

class RobertaCovidEN(language_model.LanguageModel):    
        
    def __init__(self):
        super().__init__("deepset/roberta-base-squad2-covid")        
