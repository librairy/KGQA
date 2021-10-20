FROM huggingface/transformers-tensorflow-cpu:4.6.1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY *.py /app/
COPY application/ /app/application/

WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["manage.py","runprodserver"]
