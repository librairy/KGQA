import streamlit as st

def app():

    #Subtitulo de la seccion de subida de conjuntos de datos
    st.subheader('Dataset Upload')
        
    #Texto del cuerpo de la pagina web
    st.markdown("""
    You may upload your dataset below. For it to correctly be processed and uploaded to our dataset database, please follow these guidelines:
    """, unsafe_allow_html=True)

    inputBuffer = st.file_uploader("Upload an Image", type=["csv","json"])
