import os
import base64
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from fpdf import FPDF, HTMLMixin
from utils import questionClassifier
from tempfile import NamedTemporaryFile

resourcesDir = os.path.join(os.path.dirname(os.path.realpath("__file__")),"resources_dir")

classifier = questionClassifier.QuestionClassifier(resourcesDir)

class MyFPDF(FPDF, HTMLMixin):
    pass

def writeSection(pdf, title, body, newPage = False):
    """
    Auxiliary Function to write a section in the PDF and in the interface
    """
    #If newPage is True, add a new page onto the PDF
    if newPage:
        pdf.add_page()

    #Write the title of the new section
    pdf.set_font('Times', 'B', 16)
    pdf.cell(40, 10, title)
    pdf.ln(10)
    st.subheader(title)

    #Write the body of the section        
    pdf.set_font('Times', '', 12)
    for i in body:
        st.write(i)
        pdf.cell(40, 10, i)
        pdf.ln(10)
    #Add extra space
    pdf.ln(5)

def writeTable(pdf, df, newPage = False, title = ""):
    """
    Auxiliary function to write a table in the PDF and in the interface
    """
    if newPage:
        pdf.add_page()
    
    #Write the title of the new section if it exists    
    if title:
        st.subheader(title)
        pdf.set_font('Times', 'B', 16)
        pdf.cell(40, 10, title)
        pdf.ln(10)
    
    #Write the table on the UI
    st.write(df)

    #The table written on the PDF report will be a preview (first 5 rows)
    df = df.head(5)
    #Write the table headers
    pdf.set_font('Times', '', 10)
    pdf.cell(100, 10, "Question", 1, 0, 'C')
    pdf.cell(45, 10, "Answer", 1, 0, 'C')
    pdf.cell(22, 10, "fluencyScore", 1, 0, 'C')
    pdf.cell(22, 10, "answerType", 1, 0, 'C')
    pdf.ln(10)
    #Write the table rows
    for i in range(0, len(df)): 
        pdf.cell(100, 10, '%s' % (df["question"].iloc[i][:50] + "...") if (len(df["question"].iloc[i]) > 50) else df["question"].iloc[i], 1, 0, 'C')
        pdf.cell(45, 10, '%s' % (df["answer"].iloc[i][:20] + "...") if (len(df["answer"].iloc[i]) > 20) else df["answer"].iloc[i], 1, 0, 'C')
        pdf.cell(22, 10, '%s' % "{:.2f}".format(df["fluencyScore"].iloc[i]), 1, 0, 'C')
        pdf.cell(22, 10, '%s' % df["answerType"].iloc[i], 1, 0, 'C')
        pdf.ln(10)
    pdf.ln(5)

def writeFigure(pdf, fig, newPage = False, title = ""):
    """
    Auxiliary function to write a figure in the PDF and in the interface
    """
    if newPage:
        pdf.add_page()

    if title:
        pdf.set_font('Times', 'B', 16)
        pdf.cell(40, 10, title)
        pdf.ln(10)
    #Write the figure on the UI
    st.plotly_chart(fig)
    #Write the figure on the PDF report. Save it onto a temporary file in png format
    with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.write_image(tmpfile.name)
        #Read the temporary file and insert it into the PDF
        pdf.image(tmpfile.name, w = 115, h = 115)
    pdf.ln(5)

def generatePDF(pdf, fileName, export = False):
    """
    Auxiliary function to generate the PDF report
    """
    #Create download link and write it on the UI
    downloadLink = f'<a href="data:application/octet-stream;base64,{(base64.b64encode((pdf.output(dest = "S")))).decode()}" download="{fileName}.pdf">Download file</a>'
    st.markdown(downloadLink, unsafe_allow_html=True)
    #If export is True, save the report as a local file
    if export:
        pdf.output(fileName, "F")

def generateDataframe(db, datasetName):
    """
    Auxiliary function to generate a dataframe from the database
    """
    #Get the dataset from the database and convert it into a dataframe
    df = pd.DataFrame(db.getAllDocuments(datasetName))
    #Keep only "question" and "answer" columns
    df = df[["question", "answer"]]

    #Create new columns answerType and fluencyScore using the classifier methods
    df["answerType"] = df["question"].apply(classifier.getAnswerCategory)
    df["fluencyScore"] = df["question"].apply(classifier.getFluencyScore)
    return df

def app(db):    

    st.markdown("""
    Select a dataset to generate a quality report on it.
    """, unsafe_allow_html=True)

    selectorList = [] 
    selectorList.extend(db.getCollections())

    if selectorList == []:
        st.markdown("No datasets available. Please upload one from the Upload Dataset Module.", unsafe_allow_html=True)
        
    dataset = st.selectbox("Select a DataSet", selectorList)
    run = st.button("Run")

    if dataset and run:

        with st.spinner(text=":hourglass: Generating report. This may take some minutes..."):

            df = generateDataframe(db, dataset)
            pdf = MyFPDF()

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
            writeTable(pdf, df, title = "Dataset Preview", newPage = True)
            body = ["The number of distinct questions in the dataset is " + str(len(df)), 
            "The average fluency score is " + "{:.2f}".format(df.fluencyScore.mean()) + " and its median is " + "{:.2f}".format(df.fluencyScore.median()), 
            "Maximum and minimum fluency scores are " + "{:.2f}".format(df.fluencyScore.max()) + " and " + "{:.2f}".format(df.fluencyScore.min()) + " respectively. Standard deviation is " + "{:.2f}".format(df.fluencyScore.std())]
            writeSection(pdf, "Fluency Score", body)

            answerTypes = df.answerType.unique()
            body = ["There are " + str(len(answerTypes)) + " different types of answer in this dataset, which are: " + ", ".join(answerTypes)]
            writeSection(pdf, "Answer Types", body)
            writeFigure(pdf,fig)
            generatePDF(pdf, dataset + "_report")