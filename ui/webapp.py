import streamlit as st
from streamlit import cli as stcli
import requests
from annotated_text import annotated_text
import sys
import operator

def queryJSON(queryURL, question):
    '''
    Funcion auxiliar que dado un JSON con una pregunta, realiza una consulta (con esta pregunta) a una URL
    '''
    files = {
        'question': (None, question),
    }
    response = requests.get(queryURL, files = files)
    return response.json()

def main():

    st.set_page_config(
        page_title = "MuHeQa",
        page_icon = ":book:",
        layout = "centered",
        initial_sidebar_state = "auto",
    )

    st.title('MuHeQa')

    st.subheader('Question Answering over Multiple and Heterogeneous Knowledge Bases')
    
    st.markdown("""
    Web Service that creates Natural Language answers from Natural Language questions using as Knowledge base a combination of both structured (KG) and unstructured (documents) data.
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

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def getAnswers(data):
        '''
        Funcion auxiliar que obtiene una lista con todas las respuestas sobre las distintas bases de conocimiento
        '''
        answerList = [

        ]

        for i in knowledgeBases:
            queryURL = "http://localhost:5000/eqakg/" + i + "/en?text=true"
            answerList.append(queryJSON(queryURL,data["question"]))

        return answerList

    def annotateContext(response, answer, context):
        '''
        Funcion auxiliar que anota la respuesta sobre el texto de evidencia
        '''
        tag = "ANSWER"
        if response['answer-2'] != "":
            answer = response['answer-2']
            tag = "EVIDENCE"

        answerPosition = context.find(answer)
        answerPositionEnd = answerPosition + len(answer)
        annotated_text(context[:answerPosition],(answer,tag,"#8ef"),context[answerPositionEnd:],)

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

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())