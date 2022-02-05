# The configuration file for the t5 base model can be downloaded and placed on the same directory as the saved model. Make sure to rename it to config.json
#!wget https://s3.amazonaws.com/models.huggingface.co/bert/t5-base-config.json
import pandas as pd
import torch
import re
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor


# Load the trained model for inference
# Make sure that the given path has both saved model and the configuration file. Also, remember to move the model and input tensors to GPU if you have one for performing the inference.

t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
t5_model =T5ForConditionalGeneration.from_pretrained('model/',return_dict=True)
def generate(text,model=t5_model,tokenizer=t5_tokenizer):
   model.eval()
   input_ids = tokenizer.encode("WebNLG:{} </s>".format(text),
                               return_tensors="pt")
   outputs = model.generate(input_ids)
   output = outputs[0]
   value = tokenizer.decode(output)
   phrase = value.split("<pad>")[1]
   clean_phrase = phrase.split("</s>")[0]
   return clean_phrase

   #return tokenizer.decode(outputs[0])


print(generate('Fernando Alonso | place of birth | Oviedo'))
print(generate('Fernando | place of birth | Oviedo'))
print(generate('Fernando_Alonso | place of birth | Oviedo'))
print(generate('Russia | leader | Putin'))
