import os
import base64
import pandas as pd
import streamlit as st
from utils import dbManager
import plotly.graph_objs as go
from fpdf import FPDF, HTMLMixin
from utils import questionClassifier
from tempfile import NamedTemporaryFile

dbDirection = "mongodb://localhost:27017"

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath("__file__"))))
resourcesDir = os.path.join(parentDir,"resources_dir")

classifier = questionClassifier.QuestionClassifier(resourcesDir)

class MyFPDF(FPDF, HTMLMixin):
    pass

def writeSection(pdf, title, body, newPage = False):
    """
    Funcion auxiliar que escribe una seccion del reporte en la interfaz 
    y en el archivo pdf. Puede agregar una nueva pagina al documento
    """
    if newPage:
        pdf.add_page()

    pdf.set_font('Times', 'B', 16)
    pdf.cell(40, 10, title)
    pdf.ln(10)
    st.subheader(title)
            
    pdf.set_font('Times', '', 12)
    for i in body:
        st.write(i)
        pdf.cell(40, 10, i)
        pdf.ln(10)
    pdf.ln(5)

def writeTable(pdf, df, newPage = False, title = ""):
    """
    Funcion auxiliar que escribe una tabla (pandas dataframe) en en la interfaz 
    y en el archivo pdf. Puede agregar una nueva pagina al documento
    """
    if newPage:
        pdf.add_page()
        
    if title:
        st.subheader(title)
        pdf.set_font('Times', 'B', 16)
        pdf.cell(40, 10, title)
        pdf.ln(10)
    
    pdf.set_font('Times', '', 10)
    st.write(df)

    df = df.head(5)
    pdf.cell(100, 10, "Question", 1, 0, 'C')
    pdf.cell(45, 10, "Answer", 1, 0, 'C')
    pdf.cell(22, 10, "fluencyScore", 1, 0, 'C')
    pdf.cell(22, 10, "answerType", 1, 0, 'C')
    pdf.ln(10)
    for i in range(0, len(df)): 
        pdf.cell(100, 10, '%s' % (df["question"].iloc[i][:50] + "...") if (len(df["question"].iloc[i]) > 50) else df["question"].iloc[i], 1, 0, 'C')
        pdf.cell(45, 10, '%s' % (df["answer"].iloc[i][:20] + "...") if (len(df["answer"].iloc[i]) > 20) else df["answer"].iloc[i], 1, 0, 'C')
        pdf.cell(22, 10, '%s' % "{:.2f}".format(df["fluencyScore"].iloc[i]), 1, 0, 'C')
        pdf.cell(22, 10, '%s' % df["answerType"].iloc[i], 1, 0, 'C')
        pdf.ln(10)
    pdf.ln(5)

def writeFigure(pdf, fig, newPage = False, title = ""):
    """
    Funcion auxiliar que escribe una figura de Plotly en en la interfaz 
    y en el archivo pdf. Puede agregar una nueva pagina al documento
    """
    if newPage:
        pdf.add_page()

    if title:
        pdf.set_font('Times', 'B', 16)
        pdf.cell(40, 10, title)
        pdf.ln(10)

    st.plotly_chart(fig)
    with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.write_image(tmpfile.name)
        pdf.image(tmpfile.name, w = 115, h = 115)
    pdf.ln(5)

def generatePDF(pdf, fileName, export = False):
    """
    Funcion auxiliar que genera el reporte en PDF como enlace o archivo 
    """
    downloadLink = f'<a href="data:application/octet-stream;base64,{(base64.b64encode((pdf.output(dest = "S")))).decode()}" download="{fileName}.pdf">Download file</a>'
    st.markdown(downloadLink, unsafe_allow_html=True)
    if export:
        pdf.output(fileName, "F")

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

            st.header("Quality Report")
            pdf = MyFPDF()
            writeTable(pdf, df, title = "Dataset Preview", newPage = True)
            body = ["The number of distinct questions in the dataset is " + str(len(df)), "The average fluency score is " + "{:.2f}".format(meanfluencyScore) + " and its median is " + "{:.2f}".format(medianfluencyScore), "Maximum and minimum fluency scores are " + "{:.2f}".format(maxfluencyScore) + " and " + "{:.2f}".format(minfluencyScore) + " respectively. Standard deviation is " + "{:.2f}".format(stdfluencyScore)]
            writeSection(pdf, "Fluency Score", body)

            body = ["There are " + str(len(answerTypes)) + " different types of answer in this dataset, which are: " + ", ".join(answerTypes)]
            writeSection(pdf, "Answer Types", body)
            writeFigure(pdf,fig)
            generatePDF(pdf, datasetName + "_report")