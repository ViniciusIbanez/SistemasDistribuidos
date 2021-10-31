FROM python:3.8
COPY ["app.py",\      
      "orchestrator.py",\
      "requirements.txt",\
      "./opt/app/"]

COPY ./helpers ./opt/app/helpers
COPY ./model ./opt/app/model

WORKDIR /opt/app
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "./app.py"]