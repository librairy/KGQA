import os
import pytz
import requests
import operator
import streamlit as st
from utils import spreadManager
from datetime import datetime
from annotated_text import annotated_text

"""
#Read environment variables and setup spreadsheet timezone
EQA_SERVICE_URL = os.getenv("EQA_SERVICE_URL")
EQA_SERVICE_ROUTINGS = os.getenv("EQA_SERVICE_ROUTINGS","").split(",")

WORKSHEET = os.getenv("WORKSHEET")
WORKSHEET_ID = os.getenv("WORKSHEET_ID")
SPREADSHEET = os.getenv("SPREADSHEET")
SPREAD_TIMEZONE = pytz.timezone("Europe/Madrid")

DEFAULT_NUMBER_OF_ANSWERS = int(os.getenv("DEFAULT_NUMBER_OF_ANSWERS"))
MULTIPLE_ANSWERS_JSON = os.getenv("MULTIPLE_ANSWERS")
"""
EQA_SERVICE_URL = "http://localhost:5000/muheqa/"
EQA_SERVICE_ROUTINGS = "dbpedia/en?evidence=true,wikidata/en?evidence=true,cord19/en?evidence=true".split(",")

WORKSHEET = "MuHeQa_Validation"
WORKSHEET_ID = "1TY6Tj1OwITOW3o1nYRFFRY1bunvHNImUj-J0omRq4-I"
SPREADSHEET = "Validation"
SPREAD_TIMEZONE = pytz.timezone("Europe/Madrid")

DEFAULT_NUMBER_OF_ANSWERS = 1
MULTIPLE_ANSWERS_JSON = "False"

def queryJSON(queryURL, question):
    """
    Auxiliary function to query the QA service
    """
    files = {
        'question': (None, question),
    }
    response = requests.get(queryURL, files = files)
    #Si la respuesta del servidor es distinta de None, devolvemos esta respuesta en formato json.
    if response:
        return response.json()

def app(db):

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def getAnswers(question):
        """
        Auxiliary function that queries the QA service and returns the answers
        """
        answerList = []
        #We iterate over the routings defined in the environment variable EQA_SERVICE_ROUTINGS if it is not empty
        if EQA_SERVICE_ROUTINGS:
            for routing in EQA_SERVICE_ROUTINGS:
                queryURL = EQA_SERVICE_URL + routing
                answer = queryJSON(queryURL,question)
                #If the answer is not None, we add it to the answerList
                if answer:
                    answer["source"] = routing.partition("/")[0]
                    #If there are multiple answers in the returned JSON, we iterate over them
                    if MULTIPLE_ANSWERS_JSON == "True":
                        for uniqueAnswer in answer["answers"]:
                            answerList.append(uniqueAnswer)
                    else:
                        answerList.append(answer)
        else:
            queryURL = EQA_SERVICE_URL
            answer = queryJSON(queryURL,question)
            if answer:
                if MULTIPLE_ANSWERS_JSON:
                    for uniqueAnswer in answer["answers"]:
                        answerList.append(uniqueAnswer)
                else:
                    answerList.append(answer)

        return answerList
    
    def annotateContext(answer, context, answerStart, answerEnd):
        '''
        Auxiliary function that annotates the context of the answer
        '''
        #Extract answer from context. Initialize tag as "ANSWER" and colour as green
        answerInText = context[answerStart:answerEnd]
        color = "#adff2f"
        tag = "ANSWER"
        #If the answer is different from the one in the context, we annotate it in blue with "EVIDENCE" tag
        if answer != answerInText:
            tag = "EVIDENCE"
            color = "#8ef"
        #Annotate answer in context text
        annotated_text(context[:answerStart],(answerInText,tag,color),context[answerEnd:],)

    #Create worksheet connection
    spread = spreadManager.SpreadManager(WORKSHEET, WORKSHEET_ID, SPREADSHEET)

    #Question-Answering module subtitle and description
    st.subheader('MuHeQa UI - Question Answering over Multiple and Heterogeneous Knowledge Bases')
    
    st.markdown("""
    Write any question below or use a random one from a pre-loaded datasets!
    """, unsafe_allow_html=True)
    
    #Search bar
    question = st.text_input("")

    #Dataset Selector for random questions.
    selectorList = ["All"] 
    selectorList.extend(db.getCollections())
    if selectorList == ["All"]:
        st.markdown("No datasets available")
    else: 
        dataset = st.selectbox("Select a DataSet", selectorList)  
    
    #Button to get a random question
    randomQuestion = st.button("Make a Random Question")
    
    #Sidebar title and slider
    st.sidebar.subheader("Options")
    answerNumber = st.sidebar.slider("How many relevant answers do you want?", 1, 10, DEFAULT_NUMBER_OF_ANSWERS)
    
    modelAnswer = None

    if randomQuestion:
        randomDict = db.getRandomDocument(1,dataset)[0]
        question = randomDict["question"]
        modelAnswer = randomDict["answer"]

    #If the question is not empty, we query the QA service
    if question:
        st.write("**Question: **", question)
        #If there is a model answer, we show it
        if modelAnswer:
            st.write("**Expected Answer: **", modelAnswer)
            st.write("\n")
            modelAnswer = None
        #Spinner to show that the app is looking for answers
        with st.spinner(text=':hourglass: Looking for answers...'):
            counter = 0
            highestScoreAnswer = {}
            results = getAnswers(question)
            #Sort the answers by score
            results.sort(key = operator.itemgetter('confidence'), reverse = True)
            for idx,response in enumerate(results):
                if counter >= answerNumber:
                    break
                counter += 1
                answer = response['answer']
                if answer and answer != "-":
                    context = "..." + response["evidence"]["summary"] + "..."
                    confidence = response["confidence"]
                    annotateContext(answer, context, response["evidence"]["start"] + 3, response["evidence"]["end"] + 3)
                    st.write("**Answer: **", answer)
                    source = response["source"]
                    st.write('**Relevance:** ', confidence , '**Source:** ' , source)
                    #Save the answer with the highest score in a dictionary
                    if idx == 0:
                        highestScoreAnswer = {
                            "answer": answer,
                            "confidence": confidence
                        }
        #Once answers are found, we display buttons to rate them
        st.write("Please rate if our answer has been helpful to you so we can further improve our system!")
        col1, col2 = st.columns([1,1])
        with col1:
            isRight = st.button("👍")
        with col2:
            isWrong = st.button("👎")

        #If the correct/incorrect button is pressed, we save the answer in the spreadsheet
        if isRight or isWrong:
            spread.insertRow([[question, highestScoreAnswer["answer"], str(highestScoreAnswer["confidence"]), isRight, str(datetime.now(tz=SPREAD_TIMEZONE))]])
            #Reset buttons value and show a receipt message to the user
            isRight = False
            isWrong = False
            st.success("✨ Thanks for your input!")

    #Sidebar Checkbox. If checked, we show the QA Service JSON response
    if question and st.sidebar.checkbox('Show JSON Response', key = 0):
        st.subheader('API JSON Response')
        st.write(results)