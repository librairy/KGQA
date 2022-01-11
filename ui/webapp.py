import streamlit as st
import requests
from annotated_text import annotated_text
import operator

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
            queryURL = "http://127.0.0.1:5000/eqakg/" + i + "/en?text=true"
            answerList.append(queryJSON(queryURL,data["question"]))

        return answerList

    def annotateContext(response, answer, context):
        '''
        Funcion auxiliar que anota la respuesta sobre el texto de evidencia
        '''
        tag = "ANSWER"
        color = "#adff2f"
        if response['answer-2'] != "":
            answer = response['answer-2']
            tag = "EVIDENCE"
            color = "#8ef"
    
        answerPosition = context.find(answer)
        answerPositionEnd = answerPosition + len(answer)
        annotated_text(context[:answerPosition],(answer,tag,color),context[answerPositionEnd:],)

    st.set_page_config(
        page_title = "MuHeQa",
        page_icon = ":book:",
        layout = "centered",
        initial_sidebar_state = "auto",
    )

    st.title('MuHeQa UI')

    st.subheader('Question Answering over Multiple and Heterogeneous Knowledge Bases')
    
    st.markdown("""
    Streamlit Web Interface based on MuHeQa - Web Service that creates Natural Language answers from Natural Language questions using as Knowledge Base a combination of both Structured (Knowledge Graphs) and Unstructured (documents) Data.
    """, unsafe_allow_html=True)
    
    question = st.text_input('')

    data = {
        'question': question,
        'answerNumber': 10
    }

    st.sidebar.subheader('Options')
    answerNumber = st.sidebar.slider('How many relevant answers do you want?', min_value=1, max_value=10)

    #Lista de bases de conocimiento sobre las que haremos nuestra consulta
    knowledgeBases = ["dbpedia"]

    if question:
        with st.spinner(text=':hourglass: Looking for answers...'):
            counter = 0
            results = getAnswers(data)
            results.sort(key = operator.itemgetter('score'), reverse = True)
            for i in results:
                if counter >= answerNumber:
                    break
                counter += 1
                answer = i['answer']
                if answer:
                    st.write("**Answer: **", answer)
                    context = '...' + i['text'] + '...'
                    source = "source"
                    relevance = i['score']
                    annotateContext(i, answer, context)
                    '**Relevance:** ', relevance , '**Source:** ' , source

    if question and st.sidebar.checkbox('Show debug info'):
        st.subheader('API JSON Response')
        st.write(results)

if __name__ == "__main__":
    main()