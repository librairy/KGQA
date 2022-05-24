import streamlit as st
from utils.multipage import MultiPage
from utils import dbManager 
from pages import questionAnswering, datasetManagement, reportGeneration

dbDirection = "mongodb://localhost:27017"

#Set Page attributes
st.set_page_config(
    page_title = "QA UI",
    page_icon = ":book:",
    layout = "centered",
    initial_sidebar_state = "auto",
)

#Initialize Multipage and Database.
app = MultiPage()
db = dbManager.DbManager(dbDirection)

#Set page title and body
st.title("Web Interface for Question-Answering and Dataset Validation")

st.markdown("""
    Streamlit Web Interface. \n
    It allows users to make questions onto this Service, giving input on its performance, and Upload their own Question-Answering Datasets.
    """, unsafe_allow_html=True)

#Add pages to the MultiPage.
app.addPage("Question-Answering",questionAnswering.app)
app.addPage("Upload Dataset",datasetManagement.app)
app.addPage("Report Generation",reportGeneration.app)

#Run the MultiPage (executes the selected page).
app.run(db)