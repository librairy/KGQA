FROM huggingface/transformers-tensorflow-cpu:4.6.1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python3 -m spacy_entity_linker "download_knowledge_base"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY *.py /app/
COPY application/ /app/application/

WORKDIR /app

RUN wget https://delicias.dia.fi.upm.es/nextcloud/index.php/s/qNoezAoNSWnzzto/download -O /app/resources.zip
RUN unzip resources.zip 

ENTRYPOINT ["python3"]
CMD ["manage.py","runprodserver"]
