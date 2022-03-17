import os
import pandas as pd
import streamlit as st
from utils import dbManager
import plotly.graph_objs as go
from utils import questionClassifier

dbDirection = "mongodb://localhost:27017"

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath("__file__"))))
resourcesDir = os.path.join(parentDir,"resources_dir")

classifier = questionClassifier.QuestionClassifier(resourcesDir)

def main():

    st.markdown("""
    Select a dataset to generate a quality report on it.
    """, unsafe_allow_html=True)

    db = dbManager.DbManager(dbDirection)

    selectorList = [] 
    selectorList.extend(db.getCollections())
    dataset = st.selectbox("Select a DataSet", selectorList)
    run = st.button("Run")

    if dataset and run:

        with st.spinner(text=":hourglass: Generating report. This may take some minutes..."):

            datasetName = dataset
            df = pd.DataFrame(db.getAllDocuments(datasetName))
            df = df[["question", "answer"]]

            df["answerType"] = df["question"].apply(classifier.getAnswerCategory)
            answerTypes = df.answerType.unique()
            df["fluencyScore"] = df["question"].apply(classifier.getFluencyScore)

            meanfluencyScore = df.fluencyScore.mean()
            medianfluencyScore = df.fluencyScore.median()
            stdfluencyScore = df.fluencyScore.std()
            maxfluencyScore = df.fluencyScore.max()
            minfluencyScore = df.fluencyScore.min()

            count = df["answerType"].value_counts()
            labels = count.index
            values = count.values
            layout = go.Layout(height = 600,
                    width = 600,
                    autosize = False,
                    title = "Questions by answer type, " + dataset + " dataset")                   
            traces = go.Pie(labels = labels, values = values)
            fig = go.Figure(data = traces, layout = layout)

            st.header("Quality report")
            st.write(df.head(10))
            st.write(df.tail(10))

            st.write("The number of distinct questions in the dataset is ", len(df))
            st.write("The average fluency score is ", meanfluencyScore, " and its median is ", medianfluencyScore)
            st.write("Maximum and minimum fluency scores are ", maxfluencyScore, " and ", minfluencyScore, " respectively. Standard deviation is ", stdfluencyScore)
            st.write("There are ", len(answerTypes), " different types of answer in this dataset, which are: ", answerTypes)
            st.plotly_chart(fig)