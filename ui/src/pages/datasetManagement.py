import streamlit as st
from utils import processDatasets

def app(db):

    #Question-Answering module subtitle and how to use it
    st.subheader('Dataset Management')
        
    st.markdown(""" 
    You may upload your dataset below. For it to be processed and uploaded to our database, please follow these guidelines:
    - 1. Upload your dataset either on .CSV or .JSON format.
    - 2. JSONs may be on JSON lines or JSON array format.
    - 3. Answers should be on the "answer" column/key, and Questions on the "question" column/key.
    - 4. If your Answer is verbalized, you shall name its key/column "verbalized_answer", and format it with the answer between brackets, i.e. "Fernando Alonso was born in [Oviedo]."
    """, unsafe_allow_html=True)

    #Buffer to store the uploaded file (dataset)
    inputBuffer = st.file_uploader("Upload a Dataset", type=["csv","json"])

    #If a file is uploaded, we process it and upload it to the database
    if inputBuffer:
        try:
            filename = inputBuffer.name
            #Split name into file name and extension
            splitFilename = filename.split(".")
            datasetDict = processDatasets.formatDataset(inputBuffer, isCsv=(splitFilename[1] == "csv"))
            datasetName = splitFilename[0].lower()
            #If the dataset is correctly processed, we try to upload it to MongoDB
            if datasetDict:
                db.importDataset(datasetDict, datasetName)
                #If the dataset is successfully uploaded, we show a success message
                if datasetName in db.getCollections():
                    st.success("✨ Your dataset has been registered on our database!")
                    st.write("A dataset with name ", datasetName, "and length ", len(datasetDict), " questions has been registered on MongoDB")
                else:
                    st.error("We could not upload your dataset on our database. Please contact the administrator.")
            else:
                st.error("Your dataset could not be processed correctly. Please revise the format or contact the administrator")
        except Exception as e:
            st.exception(e)