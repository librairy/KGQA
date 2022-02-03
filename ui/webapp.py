import streamlit as st
import requests
from annotated_text import annotated_text
import operator
from utils import db

def queryJSON(queryURL, question):
    '''
    Funcion auxiliar que realiza las preguntas al servidor de EQA
    '''
    files = {
        'question': (None, question),
    }
    response = requests.get(queryURL, files = files)
    return response.json()

def main():

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def getAnswers(data):
        '''
        Funcion auxiliar que obtiene una lista con todas las respuestas sobre las distintas bases de conocimiento
        '''
        answerList = [

        ]

        for i in knowledgeBases:
            queryURL = "http://127.0.0.1:5000/muheqa/" + i + "/en?evidence=true"
            answer = queryJSON(queryURL,data["question"])
            answer["source"] = i
            answerList.append(answer)

        return answerList
    
    def annotateContext(response, answer, context):
        '''
        Funcion auxiliar que anota la respuesta sobre el texto de evidencia
        '''
        tag = "ANSWER"
        color = "#adff2f"
        if response['result'] != response['answer']:
            answer = response['result']
            tag = "EVIDENCE"
            color = "#8ef"
    
        answerPosition = context.find(answer)
        answerPositionEnd = answerPosition + len(answer)
        annotated_text(context[:answerPosition],(answer,tag,color),context[answerPositionEnd:],)

    #Atributos de la pestana
    st.set_page_config(
        page_title = "MuHeQa",
        page_icon = ":book:",
        layout = "centered",
        initial_sidebar_state = "auto",
    )

    #Creamos la conexion para la base de datos de validacion
    #conn = db.connect()

    #Titulo y subtitulo del cuerpo de la interfaz
    st.title('MuHeQa UI')

    st.subheader('Question Answering over Multiple and Heterogeneous Knowledge Bases')
    
    #Texto del cuerpo de la pagina web con Markdown (convierte de texto a HTML)
    st.markdown("""
    Streamlit Web Interface based on MuHeQa - Web Service that creates Natural Language answers from Natural Language questions using as Knowledge Base a combination of both Structured (Knowledge Graphs) and Unstructured (documents) Data.
    """, unsafe_allow_html=True)
    
    question = st.text_input('')

    data = {
        'question': question,
        'answerNumber': 10
    }

    #Establecemos el titulo de la barra lateral
    st.sidebar.subheader('Options')
    #Control deslizante para el numero de respuestas a mostrar
    answerNumber = st.sidebar.slider('How many relevant answers do you want?', 1, 10, 5)

    #Lista de bases de conocimiento sobre las que haremos nuestra consulta
    knowledgeBases = ["wikidata","dbpedia","cord19"]

    if question:
        #Mensaje de carga para las preguntas. Se muestra mientras que estas se obtienen.
        with st.spinner(text=':hourglass: Looking for answers...'):
            counter = 0
            buttonKey = 1
            results = getAnswers(data)
            results.sort(key = operator.itemgetter('confidence'), reverse = True)
            for i in results:
                if counter >= answerNumber:
                    break
                counter += 1
                answer = i['answer']
                if answer:
                    st.write("**Answer: **", answer)
                    context = '...' + i['evidence'] + '...'
                    source = i['source']
                    relevance = i['confidence']
                    annotateContext(i, answer, context)
                    '**Relevance:** ', relevance , '**Source:** ' , source
                    col1, col2 = st.columns([1,1])
                    with col1:
                        isRight = st.button("👍", buttonKey)
                    with col2:
                        isWrong = st.button("👎", buttonKey + 1)
                    buttonKey += 2
                    if isRight or isWrong:
                        st.success("✨ Thanks for your input!")
                        #db.insert(conn, [[question,source,answer,isRight]])
                        #Reseteamos los valores de los botones
                        isRight = False
                        isWrong = False


    #Checkbox. Si tenemos respuesta y la caja es marcada, imprimimos las respuestas JSON obtenidas.
    if question and st.sidebar.checkbox('Show JSON Response', key = 0):
        st.subheader('API JSON Response')
        st.write(results)

if __name__ == "__main__":
    main()