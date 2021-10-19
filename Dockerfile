FROM python:3.9.7
COPY *.py /app/
COPY *.txt /app/
COPY application /app/application
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py"]
