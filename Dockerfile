FROM python:3.6.6-slim

VOLUME ./:app/

COPY . /app/

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9999:9999
ENTRYPOINT python api.py 9999

# CMD ['api.py']