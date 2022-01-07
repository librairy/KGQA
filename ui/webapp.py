import streamlit as st
from streamlit import cli as stcli
import requests
from annotated_text import annotated_text
import sys

def queryJSON(queryURL, question):
    '''
    Funcion auxiliar que dado un JSON con una pregunta, realiza una consulta (con esta pregunta) a una URL
    '''
    files = {
        'question': (None, question),
    }
    response = requests.get(queryURL, files = files)
    #pprint(response.json())
    #Obtenemos la respuesta como JSonObject y la devolvemos
    return response.json()

def main():

    st.set_page_config(
        page_title="MuHeQa",
        page_icon=":book:",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.title('MuHeQa')
    st.subheader('Question Answering over Multiple and Heterogeneous Knowledge Bases')
    st.markdown("""
    Web service that creates natural language answers from natural language questions using as knowledge base a combination of structured (KG) and unstructured (documents) data.
    """, unsafe_allow_html=True)
    question = st.text_input('')
    data = {'question': "",'answerNumber': 5}
    data['question'] = question

    st.sidebar.subheader('Options')
    answerNumber = st.sidebar.slider('How many relevant answers do you want?', min_value=1, max_value=5)

    knowledgeBases = ["dbpedia"]

    @st.cache(show_spinner=False)
    def getAnswers(data):
        answerList = []
        for i in knowledgeBases:
            queryURL = "http://localhost:5000/eqakg/" + i + "/en?text=true"
            answerList.append(queryJSON(queryURL,data["question"]))

        return answerList

    def annotateContext(answer, context):
        idx = context.find(answer)
        idx_end = idx + len(answer)
        annotated_text(context[:idx],(answer,"ANSWER","#8ef"),context[idx_end:],)

    if question:
        with st.spinner(text=':hourglass: Looking for answers...'):
            results = getAnswers(data)
            for i in results:
                answer = i['answer']
                #answer_display.subheader(answer)
                if answer:
                        context = '...' + i['text'] + '...'
                        source = "source"
                        relevance = i['score']
                        annotateContext(answer, context)
                        '**Relevance:** ', relevance , '**source:** ' , source

    if question and st.sidebar.checkbox('Show debug info'):
        st.subheader('REST API JSON response')
        st.write(results)

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())