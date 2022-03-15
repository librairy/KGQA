import streamlit as st

#Importamos el gestor de multiples paginas
from utils.multipage import MultiPage 
#Importamos las aplicaciones correspondientes a las distintas paginas de nuestra interfaz
from pages import questionAnswering, datasetManagement, reportGeneration

#Atributos de la pagina
st.set_page_config(
    page_title = "MuHeQa UI",
    page_icon = ":book:",
    layout = "centered",
    initial_sidebar_state = "auto",
)

#Inicializamos la aplicacion
app = MultiPage()

#Titulo para todas las paginas
st.title('Web Interface for Question-Answering and Dataset Validation')

#Texto del cuerpo de la pagina, con Markdown (convierte de texto a HTML)
st.markdown("""
    Streamlit Web Interface based on MuHeQa - Web Service that creates Natural Language answers from Natural Language questions using as Knowledge Base a combination of both Structured and Unstructured Data. \n
    It allows users to make questions onto this Service, giving input on its performance, and Upload their own Question-Answering Datasets.
    """, unsafe_allow_html=True)

#Agregamos las distintas paginas
app.add_page("Question-Answering",questionAnswering.main)
app.add_page("Upload Dataset",datasetManagement.main)
app.add_page("Report Generation",reportGeneration.main)

#Ejecutamos el codigo de la pagina principal
app.run()