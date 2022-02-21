import streamlit as st
from utils import db

def main():

    st.markdown("""
    Select a dataset to generate a quality report on it.
    """, unsafe_allow_html=True)

    database = db.createConnection()

    col1, col2 = st.columns([1,1])
    with col1:
        run = st.button("Run")
    with col2:
        selectorList = ["All"] 
        selectorList.extend(db.getCollections(database))