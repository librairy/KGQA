import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor


# Load the preprocessed data and randomly shuffle the rows to have triplets with different lengths (1 triplet to 7triplets)
# distributed across the data frame and hence to generalize the loss quickly.
train_df=pd.read_csv('webNLG2020_train.csv', index_col=[0])
train_df=train_df.iloc[  :35000,:]
train_df=train_df.sample(frac = 1)
batch_size=8
num_of_batches=len(train_df)/batch_size

# Detecting the GPU.
if torch.cuda.is_available():
   dev = torch.device("cuda:0")
   print("Running on the GPU")
else:
   dev = torch.device("cpu")
   print("Running on the CPU")

# Loading the pre-trained models, tokenizers, and moving the model into GPU.
tokenizer = T5Tokenizer.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained('t5-base',return_dict=True)
model.to(dev)

# Initiating the Adafactor optimizer with recommended T5 settings.
optimizer = Adafactor(model.parameters(),lr=1e-3,
                      eps=(1e-30, 1e-3),
                      clip_threshold=1.0,
                      decay_rate=-0.8,
                      beta1=None,
                      weight_decay=0.0,
                      relative_step=False,
                      scale_parameter=False,
                      warmup_init=False)

def progress(loss,value, max=100):
 print(loss,value,max)

#Sets the module in training mode
model.train()

# Train the model
loss_per_10_steps=[]
num_of_epochs=4
for epoch in range(1,num_of_epochs+1):
  print('Running epoch: {}'.format(epoch))

  running_loss=0

  out = display(progress(1, num_of_batches+1), display_id=True)
  for i in range(int(num_of_batches)):
    inputbatch=[]
    labelbatch=[]
    new_df=train_df[i*batch_size:i*batch_size+batch_size]
    for indx,row in new_df.iterrows():
      input = 'WebNLG: '+row['input_text']+'</s>'
      labels = row['target_text']+'</s>'
      inputbatch.append(input)
      labelbatch.append(labels)
    inputbatch=tokenizer.batch_encode_plus(inputbatch,padding=True,max_length=400,return_tensors='pt')["input_ids"]
    labelbatch=tokenizer.batch_encode_plus(labelbatch,padding=True,max_length=400,return_tensors="pt") ["input_ids"]
    inputbatch=inputbatch.to(dev)
    labelbatch=labelbatch.to(dev)

    # clear out the gradients of all Variables
    optimizer.zero_grad()

    # Forward propogation
    outputs = model(input_ids=inputbatch, labels=labelbatch)
    loss = outputs.loss
    loss_num=loss.item()
    logits = outputs.logits
    running_loss+=loss_num
    if i%10 ==0:
      loss_per_10_steps.append(loss_num)
    progress(loss_num,i, num_of_batches+1)

    # calculating the gradients
    loss.backward()

    #updating the params
    optimizer.step()

  running_loss=running_loss/int(num_of_batches)
  print('Epoch: {} , Running loss: {}'.format(epoch,running_loss))

# Serializing the model
torch.save(model.state_dict(),'pytorch_model.bin')
