import requests
import pysolr
import pprint
import spacy
import application.summary.Summarizer as summarizer


class Cord19(summarizer.Summarizer):

    def __init__(self,lang):
        url = "http://librairy.linkeddata.es/solr/cord19-paragraphs"
        self.solr = pysolr.Solr(url, search_handler="/select", timeout=5)
        #self.nlp = spacy.blank(lang)
        self.nlp = spacy.load("en_core_web_sm")


    def get_summary(self,question):
        # extract named entites
        ner_api = "https://librairy.linkeddata.es/bio-ner/entities"
        message = {'text':question}
        headers = {'contentType': 'application/json; charset=utf-8'}
        r = requests.post(ner_api, json = message, headers=headers)
        response = r.json()
        chemicals = response['entities']['chemicals']
        diseases = response['entities']['diseases']
        genetics = response['entities']['genetics']

        search_filter = []
        for chemical in chemicals:
            if 'found_term' in chemical:
                search_filter.append("biobert_chemical_normalized_term:"+chemical['found_term'])
        for disease in diseases:
            if 'found_term' in disease:
                search_filter.append("biobert_disease_normalized_term:"+disease['found_term'])
        for gene in genetics:
            if 'found_term' in gene:
                search_filter.append("biobert_genetic_normalized_term:"+gene['found_term'])

        # extract nouns and verbs
        doc = self.nlp(question)

        valid_pos = ["NOUN","VERB"]
        for token in doc:
            if token.is_stop:
                continue
            if token.pos_ in valid_pos:
                search_filter.append("text_t:"+token.text)

        pprint.pprint(search_filter)

        entities = ['']
        text = ""

        q = " OR ".join(search_filter)
        fl = "text_t,score"
        fq = ""
        rows = 5

        results = self.solr.search(q, **{
            'fl': fl,
            'fq': fq,
            'rows': rows
        })
        #print("Number of hits: {0}".format(len(results)))
        for result in results:
          text += result['text_t'] + " "

        return text


if __name__ == "__main__" :

    cord19 = Cord19("en")
    cord19.get_summary("what is the effect of chloroquine on thrombosis?")
