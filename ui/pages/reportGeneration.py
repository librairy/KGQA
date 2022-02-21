import streamlit as st
from utils import db

def main():

    st.markdown("""
    Select a dataset to generate a quality report on it.
    """, unsafe_allow_html=True)

    database = db.createConnection()

    col1, col2 = st.columns([1,1])
    with col1:
        selectorList = ["All"] 
        selectorList.extend(db.getCollections(database))
        dataset = st.selectbox("Select a DataSet", selectorList)
    with col2:
        run = st.button("Run")