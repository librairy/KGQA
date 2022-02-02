# The configuration file for the t5 base model can be downloaded and placed on the same directory as the saved model. Make sure to rename it to config.json
#!wget https://s3.amazonaws.com/models.huggingface.co/bert/t5-base-config.json
import pandas as pd
import torch
import pathlib
import os.path
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor


# Load the trained model for inference
# Make sure that the given path has both saved model and the configuration file. Also, remember to move the model and input tensors to GPU if you have one for performing the inference.

class DataModel:

    def __init__(self):
        current_path=pathlib.Path(__file__).parent.resolve()
        model_path = os.path.join(current_path, 'model')
        print("Data-to-text model directory:",model_path)
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.model =T5ForConditionalGeneration.from_pretrained(model_path,return_dict=True)
        self.model.eval()
        print("Data-to-Text model load successfully!")

    def verbalize(self,subject,predicate,object):
        text = " | ".join([object,predicate,subject])
        input_ids = self.tokenizer.encode("WebNLG:{} </s>".format(text),return_tensors="pt")
        outputs = self.model.generate(input_ids)
        output_text = self.tokenizer.decode(outputs[0])
        phrase = output_text.split("<pad>")[1]
        clean_phrase = phrase.split("</s>")[0]
        print("subject:",subject,", predicate:", predicate, ", object:", object, "-> ",clean_phrase)
        return clean_phrase
