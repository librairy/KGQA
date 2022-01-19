# -*- coding: utf-8 -*-

class Summarizer:

    def __init__(self,lang):
        if lang == 'en':
            self.the_text = " The "
            self.of_text = " of "
            self.is_text = " is "
        elif lang == 'es':
            self.the_text = " "
            self.of_text = " de "
            self.is_text = " es "

    def get_single_fact_summary(self, entity, properties):
        summary = ""
        if properties != None:
            for key in properties:
                normalized_key = key.replace('\n', ' ').replace('\r', '')
                normalized_value = properties[key].replace('\n', ' ').replace('\r', '')
                single_fact_sentence = self.the_text + normalized_key + self.of_text + entity + self.is_text + normalized_value + ". "
                summary += single_fact_sentence
        return summary
