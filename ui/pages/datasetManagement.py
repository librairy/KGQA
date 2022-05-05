import streamlit as st
from utils import dbManager
from utils import parseDatasets

dbDirection = "mongodb://localhost:27017"

def main():

    #Subtitulo de la seccion de gestion de conjuntos de datos
    st.subheader('Dataset Management')
        
    #Texto del cuerpo de la pagina web
    st.markdown(""" 
    You may upload your dataset below. For it to be processed and uploaded to our database, please follow these guidelines:
    - 1. Upload your dataset either on .CSV or .JSON format.
    - 2. JSONs may be on JSON lines or JSON array format.
    - 3. Answers should be on the "answer" column/key, and Questions on the "question" column/key.
    - 4. If your Answer is verbalized, you shall name its key/column "verbalized_answer", and format it with the answer between brackets, i.e. "Fernando Alonso was born in [Oviedo]."
    """, unsafe_allow_html=True)

    inputBuffer = st.file_uploader("Upload an Image", type=["csv","json"])

    if inputBuffer:
        try:
            db = dbManager.DbManager(dbDirection)
            filename = inputBuffer.name
            splitFilename = filename.split(".")
            datasetDict = parseDatasets.parseDataset(inputBuffer, isCsv=(splitFilename[1] == "csv"))
            datasetName = splitFilename[0].lower()
            if datasetDict:
                db.importDataset(datasetDict, datasetName)
                if datasetName in db.getCollections():
                    st.success("✨ Your dataset has been registered on our database!")
                    st.write("A dataset with name ", datasetName, "and length ", len(datasetDict), " questions has been registered on MongoDB")
                else:
                    st.error("We could not upload your dataset on our database. Please contact the administrator.")
            else:
                st.error("Your dataset could not be processed correctly. Please revise the format or contact the administrator")
        except Exception as e:
            st.exception(e)    