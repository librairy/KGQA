# QA Streamlit Webapp
![Docker](https://img.shields.io/badge/docker-v20.10.2+-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Task](https://img.shields.io/badge/task-EQAKG-green.svg)
[![License](https://img.shields.io/badge/license-MIT-red)](https://choosealicense.com/licenses/mit/)

## Basic Overview
Web Interface based on Streamlit for a QA service working as a REST API. This User Interface was developed for the Extractive Question-Answering Service [MuHeQa](https://github.com/librairy/MuHeQA) as part of my End of Degree Project (Trabajo de Fin de Grado) for my Bachelor's Degree in Mathematics and Computer Science.  
For a detailed guide on implementation, usage and more please refer to [this Document](https://www.overleaf.com/read/ggqhsgrcjhgf) (in Spanish).

## JSON Responses
When using this User Interface for your Extractive Question-Answering Service, you need to bear in mind that the Question Answering Module on our webapp is able to read answers from JSON Responses with the following formats. 
- In case there is a single answer per JSON:
    ```
        {
        "answer": "Oviedo, Asturias, Spain",
        "source": dbpedia,
        "confidence": 0.801,
        "evidence": {
            "end": 149,
            "summary": "  The car number of Fernando Alonso is 14.   The Last win of Fernando Alonso is 2013.   The birth place of Fernando Alonso is Oviedo, Asturias, Spain.   The name of
            Fernando Alonso is Fernando Alonso.   The First win of Fernando Alonso is 2003.   The last season of Fernando Alonso is 2018.   The birth name of Fernando Alonso is Fernando
            Alonso D\u00edaz.   The caption of Fernando Alonso is Alonso in 2016.   The First race of Fernando Alonso is 2001.   The image size of Fernando Alonso is 240.   The last win of
            Fernando Alonso is 2013 Spanish Grand Prix.   The nationality of Fernando Alonso is Spanish.   The title of Fernando Alonso is Fernando Alonso achievements, Fernando Alonso
            teams and series.   The first race of Fernando Alonso is 2001 Australian Grand Prix.   The 2021 Team of Fernando Alonso is Alpine F1, Renault in Formula One.   The source  of
            Fernando Alonso is Alonso's race engineer at Ferrari, Andrea Stella, on Alonso's ability and similarities to Michael Schumacher.   The first win of Fernando Alonso is 2003
            Hungarian Grand Prix.  .
            ",
            "start": 126
        },
        "question": "where was Fernando Alonso born?"
        } 
    ```
- For multiple answers in one unique JSON Response:
    ```
        {
        "question": "where was Fernando Alonso born?"
        "answers": [
        {
            "answer": "Oviedo",
            "source": wikidata,
            "confidence": 0.9754,
            "evidence":{
                "end":523,
                "start":517,
                "summary":" The Encyclopædia Universalis ID of Fernando Alonso is fernando-alonso. The BAnQ author ID of Fernando Alonso is ncf10786137. The Treccani ID of Fernando Alonso
                is fernando-alonso. The sibling of Fernando Alonso is Lorena Alonso. The Quora topic ID of Fernando Alonso is Fernando-Alonso. The AS. com athlete ID of Fernando Alonso is
                fernando_alonso/24337. The image of Fernando Alonso is http://commons. wikimedia. org/wiki/Special:FilePath/Alonso%202016. jpg. The place of birth of Fernando Alonso is
                Oviedo. The sex or gender of Fernando Alonso is male. The father of Fernando Alonso is José Luis Alonso. The spouse of Fernando Alonso is Raquel del Rosario. The country of
                citizenship of Fernando Alonso is Spain. The instance of of Fernando Alonso is human. The position held of Fernando Alonso is UNICEF Goodwill Ambassador. The member of
                sports team of Fernando Alonso is Minardi, Scuderia Ferrari, McLaren, Renault F1 Team, Alpine F1 Team. The native language of Fernando Alonso is Spanish"
            }

        },
        {
            "answer": "Oviedo, Asturias, Spain",
            "source": dbpedia,
            "confidence": 0.801,
            "evidence": {
                "end": 149,
                "summary": "  The car number of Fernando Alonso is 14.   The Last win of Fernando Alonso is 2013.   The birth place of Fernando Alonso is Oviedo, Asturias, Spain.   The name 
                of Fernando Alonso is Fernando Alonso.   The First win of Fernando Alonso is 2003.   The last season of Fernando Alonso is 2018.   The birth name of Fernando Alonso is
                Fernando Alonso D\u00edaz.   The caption of Fernando Alonso is Alonso in 2016.   The First race of Fernando Alonso is 2001.   The image size of Fernando Alonso is 240.   The
                last win of Fernando Alonso is 2013 Spanish Grand Prix.   The nationality of Fernando Alonso is Spanish.   The title of Fernando Alonso is Fernando Alonso achievements,
                Fernando Alonso teams and series.   The first race of Fernando Alonso is 2001 Australian Grand Prix.   The 2021 Team of Fernando Alonso is Alpine F1, Renault in Formula
                One.   The source  of Fernando Alonso is Alonso's race engineer at Ferrari, Andrea Stella, on Alonso's ability and similarities to Michael Schumacher.   The first win of
                Fernando Alonso is 2003 Hungarian Grand Prix.  .
                ",
                "start": 126
            }
        },
        ...   
        ]
        } 
    ```

## Docker Quick Start
### Prerequisites
1. [Install Docker](https://docs.docker.com/get-docker/) in your system to be able to deploy this web tool.
2. Create a new Spreadhseet on Google Sheets and save the Worksheet Name, as well as the name of the Spreadsheet you will store user validation into. You will also need the Spreadsheet ID, which can be found on the URL for your sheet after `gid=`. These variables will be of use in the .env file used to set the container up:
```
    WORKSHEET=" "
    WORKSHEET_ID=" "
    SPREADSHEET="Validation"
```
3. Next, you will need to create a Service Account and obtain OAuth2 Credentials to access your Spreadsheet from the Google Drive API for Python.
    1. Head over to the [Google API Dashboard](https://console.developers.google.com/).
    2. Create a new project from the Navigation Bar by clicking "My First Project", and then "New Project" on the pop-up window:
    <p align="center"><img src="https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20First%20Project.png"></p>
    <p align="center"><img src="https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20New%20Project.png"></p>
    3. Next, from "Enabled APIs and Services" (Sidebar) click on "+ Enable APIs and Services".
    <p align="center"><img src="https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20Enable%20APIs.png"></p>
    4. From the search bar, look for "Google Drive API" and "Google Sheets API" and enable them so you can access Sheets uploaded on Google Drive.
    <p align="center"><img src="https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20Drive.png"></p>
    <p align="center"><img src="https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20Sheets.png"></p>
    5. Go to "Credentials" (sidebar), click "Create Credentials" -> "Service Account Key". Create a new account.
    <p align="center"><img src=https://raw.githubusercontent.com/Josemvg/QA-Streamlit-Webapp/master/docs/imgs/Google%20API%20Credentials%20-%20Create%20Credentials.png></p> 
    6. From the "Credentials" page, access your newly created account at the "Service Accounts" Section. Finally, on "Keys" add a new key from the "Add Keys" button, with Type "JSON".
4. A JSON with the following format should have been downloaded onto your PC. Save it on `src/utils/` as `credentials.json`.
```
{
    "type": "service_account",
    "project_id": " ",
    "private_key_id": " ",
    "private_key": "-----BEGIN PRIVATE KEY-----\n KEY =\n-----END PRIVATE KEY-----\n",
    "client_email": " ",
    "client_id": " ",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ "
}
```
5. Give your newly created Service Account Editor permissions on your sheet.

### Deploying the web application
1. Create a file with the following code, which can also be found in the `Dockerfile.streamlit` fie:
```
    FROM python:3.9

    #Create resources_dir
    RUN apt-get update && apt-get install -y \
        curl \
        unzip
    RUN curl https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M/download --output /src/utils/resources_dir.zip --create-dirs
    RUN unzip /src/utils/resources_dir.zip -d /src/utils/
    RUN curl https://delicias.dia.fi.upm.es/nextcloud/index.php/s/JCarxYnnReHPwbP/download --output /src/utils/resources_dir/ZAMIA_Fluency_Score/en_large_model.binary --create-dirs

    #Install requirements and run the webapp
    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt

    COPY ./src /src
    WORKDIR /src
    EXPOSE 8501
    ENTRYPOINT ["streamlit", "run", "webapp.py"]
```
2. Build the image as `qa-webapp/streamlit-ui`:
```
    $ docker build --pull --rm -f "Dockerfile.streamlit" -t qa-webapp/streamlit-ui-:latest "." <
```

3. Create a docker-compose.yml file with the following code, which can also be found in the repository as `docker-compose.yml`:
```
    version: "3.9"
    services:

    web:
        image: "qa-webapp/streamlit-ui"
        ports:
        - "8501:8501"
        restart: on-failure
        depends_on:
        - mongodb
        links:
        - "mongodb:db"
        env_file:
        - .env

    mongodb:
        image: "mongo"
        ports:
        - "27017:27017"
        restart: on-failure
        volumes:
        - ./src/utils:/db
```
4. Set the Environment Variables up on the .env file. An example is provided below, and you can find a thorough explanation of these variables in the [Documentation](https://www.overleaf.com/read/ggqhsgrcjhgf), Chapter 3.6.4 (Chapter 3 Section 6 SubSection 4):
```
    EQA_SERVICE_URL="http://localhost:8000"
    EQA_SERVICE_ROUTINGS=""
    WORKSHEET=" "
    WORKSHEET_ID=" "
    SPREADSHEET="Validation"
    DEFAULT_NUMBER_OF_ANSWERS=1
    MULTIPLE_ANSWERS_JSON = "False"
```
5. Deploy the application by running the container:
```
    $ docker-compose up
```
Now, you should be able to access the Web Interface from the direction `localhost:8000`