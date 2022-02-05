# -*- coding: utf-8 -*-
import application.summary.kg.nlg.DataModel as dm

import application.summary.Summarizer as summarizer

class KGSummarizer(summarizer.Summarizer):

    rdf_verbalizer = dm.DataModel()

    def __init__(self,lang,rules=True):
        super().__init__()
        self.rules = rules
        self.lang = lang
        if self.lang == 'en':
            self.the_text = " The "
            self.of_text = " of "
            self.is_text = " is "
        if self.lang == 'es':
            self.the_text = " "
            self.of_text = " de "
            self.is_text = " es "

    def get_single_fact_summary(self, entity, properties):
        summary = ""
        if properties != None:
            for key in properties:
                normalized_key = key.replace('\n', ' ').replace('\r', '')
                normalized_value = properties[key].replace('\n', ' ').replace('\r', '')
                if (self.rules):
                    summary += self.the_text + normalized_key + self.of_text + entity + self.is_text + normalized_value + ". "
                else:
                    summary += self.rdf_verbalizer.verbalize(entity, normalized_key, normalized_value)
        return summary
